import time
import flask
import json
from flask import request, jsonify, session
from llm import get_initial_training_plan, get_updated_training_plan


from gcalendar import get_gc_service, get_gc_events, get_events_at_days, add_event, clear_coach_events

from whoopy import WhoopClient, activity_lookup
from user_model import User


def create_app():
    app = flask.Flask(__name__)

    app.secret_key = 'BAD_SECRET_KEY'


    global event_dict, gc_service, tokens_dict, setup_dict, user_messages, user_profile, llm_responses, is_setup, blocked_time_slots, last_calendar_update

    event_dict = {}
    gc_service = None
    tokens_dict = {}
    setup_dict = {}
    user_messages = []
    user_profile = User()
    llm_responses = []
    is_setup = False
    blocked_time_slots = {}
    last_calendar_update = 0

    @app.route("/")
    def hello_world():
        return "Hello, World!"

    @app.route("/whoop", methods=["POST", "GET"])
    def whoop():
        global llm_responses, blocked_time_slots
        json_data = request.json

        print(json_data)

        ev_id = json_data.get("id", "")
        ev_tye = json_data.get("type", "")

        if ev_tye == "workout.update":
            wc = WhoopClient(tokens_dict["whoop"])
            workout = wc.get_workout_by_id(ev_id)
            print(workout)
            # trigger LLM Update


            activity = activity_lookup[workout["sport_id"]]
            workout["sport_name"] = activity

            del workout["score_state"]
            del workout["sport_id"]

            whoop_update = {
                "update": "whoop training finished",
                "workout": workout
            }

            if len(llm_responses) > 0:
                last_response = llm_responses[-1]
                print("Updating training plan...")
                response = get_updated_training_plan(
                        user_profile=user_profile,
                        user_message="",
                        last_response=last_response,
                        whoop_update=whoop_update,
                        blocked_time_slots=blocked_time_slots
                )
                update_calendar(response)
                print(response.__dict__)
                llm_responses.append(response)

        return "Hello, World4!"


    # @app.route("/calupdates", methods=["POST", "GET"])
    # def calupdates():

    #     global llm_responses, blocked_time_slots, last_calendar_update

    #     if time.time() - last_calendar_update < 60:
    #         return ""

    #     updated_evs = get_updated_events()
    #     print(updated_evs)
    #     # trigger LLM Update

    #     if len(updated_evs) == 0:
    #         return ""

    #     # blocked_time_slots = get_events_at_days(gc_service)
    #     # if len(llm_responses) > 0:
    #     #     last_response = llm_responses[-1]
    #     #     print("Updating training plan...")
    #     #     response = get_updated_training_plan(
    #     #             user_profile=user_profile,
    #     #             user_message="",
    #     #             last_response=last_response,
    #     #             whoop_update={},
    #     #             blocked_time_slots=blocked_time_slots
    #     #     )
    #     #     print(response.__dict__)
    #     #     update_calendar(response)
    #     #     llm_responses.append(response)

    #     return "Hello, World2!"
    

    @app.route("/tokens", methods=["POST"])
    def receive_tokens():
        global tokens_dict

        json_data = request.json
        print(json_data)

        keys = ["whoop", "calendar"]
        for k in keys:
            tokens_dict[k] = ""
            if k in json_data:
                tokens_dict[k] = json_data[k]
            else:
                print("no token received for " + k)

        with open("c_w_tokens.json", "w") as fp:
            json.dump(tokens_dict, fp)

        return "Hello, Tokens!"

    
    @app.route("/setup", methods=["POST"])
    def receive_setup():
        global setup_dict, user_profile, llm_responses, tokens_dict, is_setup, blocked_time_slots

        user_profile.is_default = True
        # is_setup = False

        json_data = request.json
        print(json_data)

        setup_dict["sports"] = []
        setup_dict["objective"] = ""

        if "sports" in json_data:
            setup_dict["sports"] = json_data["sports"]
        if "objective" in json_data:
            setup_dict["objective"] = json_data["objective"]

        user_profile.sports = setup_dict["sports"]
        user_profile.training_objective = setup_dict["objective"]

        if "whoop" in tokens_dict and tokens_dict["whoop"] != "":
            wc = WhoopClient(tokens_dict["whoop"])

            user_profile.name = wc.get_profile()["first_name"]

            measurements = wc.get_body_measurement()
            user_profile.age = 30
            user_profile.weight = measurements["weight_kilogram"]
            user_profile.height = measurements["height_meter"]

            user_profile.calc_fitness_level(wc.get_workouts())
            user_profile.update_sleeps_scores(wc.get_sleeps())
            user_profile.update_recovery_scores(wc.get_recoveries())
            user_profile.is_default = False

            print("Loaded User Profile:", user_profile.to_dict())
        else:
            print("No Whoop Token available. Using default user profile.")

        print("Generating initial training plan...")
        response = get_initial_training_plan(user_profile, blocked_time_slots)
        update_calendar(response)
        print(response.__dict__)
        llm_responses.append(response)

        is_setup = True

        return "Hello, Setup!"
    

    @app.route("/adapt", methods=["POST"])
    def receive_adapt():
        global user_messages, llm_responses, blocked_time_slots

        json_data = request.json
        print(json_data)

        if "text" in json_data:
            user_messages.append(json_data["text"])

        if len(llm_responses) == 0:
            print("SHIT HAPPENED! NO EXISTING TRAINING PLAN AVAILABLE")
            print("Generating initial training plan...")
            response = get_initial_training_plan(user_profile, blocked_time_slots)
            update_calendar(response)
            llm_responses.append(response)
        else:
            last_user_message = user_messages[-1] if len(user_messages) > 0 else ""
            last_response = llm_responses[-1]
            print("Updating training plan...")
            response = get_updated_training_plan(
                    user_profile=user_profile,
                    user_message=last_user_message,
                    last_response=last_response,
                    whoop_update={},
                    blocked_time_slots=blocked_time_slots
            )
            print(response.__dict__)
            update_calendar(response)
            llm_responses.append(response)
        return "Hello, Adapt!"
    

    @app.route("/setup-test", methods=["GET", "POST"])
    def receive_setup_test():
        global setup_dict, user_profile, llm_responses
        print("Generating initial training plan...")
        blocked_time_slots = {
            "18.09.2023": ["0:00 - 13:00", "16:00 - 23:00"],
            "19.09.2023": ["0:00 - 12:00", "14:30 - 23:00"],
            "20.09.2023": ["0:00 - 11:00", "13:00 - 23:00"]
            }
        response = get_initial_training_plan(user_profile, get_initial_training_plan(user_profile))
        print(response.__dict__)
        update_calendar(response)
        llm_responses.append(response)
        return "Hello, Setup Test!"
    

    @app.route("/adapt-test", methods=["GET", "POST"])
    def receive_adapt_test():
        global llm_responses, blocked_time_slots

        user_messages = ["My knee hurts!"]

        if len(llm_responses) == 0:
            print("SHIT HAPPENED! NO EXISTING TRAINING PLAN AVAILABLE")
            print("Generating initial training plan...")
            response = get_initial_training_plan(user_profile, blocked_time_slots)
            update_calendar(response)
            llm_responses.append(response)
        else:
            last_user_message = user_messages[-1] if len(user_messages) > 0 else ""
            last_response = llm_responses[-1]
            print(last_response)
            print(last_response.get_trainings_plan())
            print("Updating training plan...")
            response = get_updated_training_plan(
                    user_profile=user_profile,
                    user_message=last_user_message,
                    last_response=last_response,
                    whoop_update={},
                    blocked_time_slots=blocked_time_slots
            )
            update_calendar(response)
            print(response.__dict__)
            llm_responses.append(response)
        return "Hello, Adapt Test!"


    @app.route("/state", methods=["POST", "GET"])
    def state():
        global llm_responses, user_profile, is_setup

        if not is_setup:
            return jsonify({})

        if len(llm_responses) == 0:
            with open("tp.json", "r") as fp:
                tp = json.load(fp)
        else:
            print(llm_responses[-1])
            print(type(llm_responses[-1]))
            print(llm_responses[-1].__dict__)
            print(llm_responses[-1].get_trainings_plan())
            tp = llm_responses[-1].__dict__

        if not user_profile.is_default:
            tp["user"] = user_profile.to_dict()

        return jsonify(tp)


    def load_tokens():
        global tokens_dict
        try:
            with open("c_w_tokens.json", "r") as fp:
                tokens_dict = json.load(fp)
        except Exception:
            print("no tokens file found")
            tokens_dict = {}


    def init_events():
        global gc_service, event_dict, blocked_time_slots

        gc_service = get_gc_service()
        gc_events = get_gc_events(gc_service)
        blocked_time_slots = get_events_at_days(gc_service)

        for event in gc_events:
            event_dict[event["id"]] = event


    def get_updated_events():
        global gc_service, event_dict

        gc_events = get_gc_events(gc_service)

        updated_events = []

        for event in gc_events:
            if event["id"] not in event_dict:
                updated_events.append(event)
                event_dict[event["id"]] = event
            elif event_dict[event["id"]]["updated"] != event["updated"]:
                updated_events.append(event)
                event_dict[event["id"]] = event

        return updated_events


    def update_calendar(response):
        global gc_service, last_calendar_update

        session["cal_enter"] = "xD"

        if time.time() - last_calendar_update < 60:
            return

        # Remove all workouts
        clear_coach_events(gc_service)

        # Add workouts
        for workout in response.workouts:
            add_event(
                service=gc_service,
                day_str=workout["date"],
                time_str=workout["start_time"],
                dur_str=str(workout["duration"]),
                title=workout["title"],
                decr=workout["summary"]
            )

        last_calendar_update = time.time()

        session["cal_exit"] = "free"


    load_tokens()
    init_events()

    return app


    


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0")