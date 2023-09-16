import flask
import json
from flask import request, jsonify
from llm import get_initial_training_plan, get_updated_training_plan


from gcalendar import get_gc_service, get_gc_events

from whoopy import WhoopClient
from user_model import User
from response_model import ResponseModel


def create_app():

    app = flask.Flask(__name__)

    global event_dict, gc_service, tokens_dict, setup_dict, user_messages, user_profile, llm_responses, is_setup

    event_dict = {}
    gc_service = None
    tokens_dict = {}
    setup_dict = {}
    user_messages = []
    user_profile = User()
    llm_responses = []
    is_setup = False


    @app.route("/")
    def hello_world():
        return "Hello, World!"


    @app.route("/whoop", methods=["POST", "GET"])
    def whoop():
        json_data = request.json()

        print(request.headers)

        print(json_data)

        ev_id = json_data.get("id", "")
        ev_tye = json_data.get("type", "")

        if ev_tye == "workout.update":
            wc = WhoopClient(tokens_dict["whoop"])
            workout = wc.get_workout_by_id(ev_id)
            print(workout)
            # trigger LLM Update

        return "Hello, World4!"


    @app.route("/calupdates", methods=["POST", "GET"])
    def calupdates():
        json_data = request.data.decode("utf-8")

        print(request.headers)

        print(json_data)

        updated_evs = get_updated_events()
        print(updated_evs)
        # trigger LLM Update

        return "Hello, World2!"


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
        global setup_dict, user_profile, llm_responses, tokens_dict, is_setup

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

        if 'whoop' in tokens_dict and tokens_dict['whoop'] != '':
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
        response = ResponseModel(get_initial_training_plan(user_profile))
        print(response.__dict__)
        llm_responses.append(response)

        is_setup = True

        return "Hello, Setup!"


    @app.route("/adapt", methods=["POST"])
    def receive_adapt():
        global user_messages, llm_responses

        json_data = request.json
        print(json_data)

        if "text" in json_data:
            user_messages.append(json_data["text"])

        if len(llm_responses) == 0:
            print("SHIT HAPPENED! NO EXISTING TRAINING PLAN AVAILABLE")
            print("Generating initial training plan...")
            llm_responses.append(get_initial_training_plan(user_profile))
        else:
            last_user_message = user_messages[-1] if len(user_messages) > 0 else ""
            last_response = llm_responses[-1]
            print("Updating training plan...")
            response = ResponseModel(get_updated_training_plan(user_profile=user_profile, user_message=last_user_message, last_response=last_response))
            print(response.__dict__)
            llm_responses.append(response)
        return "Hello, Adapt!"


    @app.route("/setup-test", methods=["GET", "POST"])
    def receive_setup_test():
        global setup_dict, user_profile, llm_responses
        print("Generating initial training plan...")
        response = ResponseModel(get_initial_training_plan(user_profile))
        print(response.__dict__)
        llm_responses.append(response)
        return "Hello, Setup Test!"



    @app.route("/adapt-test", methods=["GET", "POST"])
    def receive_adapt_test():
        global llm_responses

        user_messages = ["My knee hurts!"]

        if len(llm_responses) == 0:
            print("SHIT HAPPENED! NO EXISTING TRAINING PLAN AVAILABLE")
            print("Generating initial training plan...")
            llm_responses.append(get_initial_training_plan(user_profile))
        else:
            last_user_message = user_messages[-1] if len(user_messages) > 0 else ""
            last_response = llm_responses[-1]
            print(last_response)
            print(last_response.get_trainings_plan())
            print("Updating training plan...")
            response = ResponseModel(get_updated_training_plan(user_profile=user_profile, user_message=last_user_message, last_response=last_response))
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
        global gc_service, event_dict

        gc_service = get_gc_service()
        gc_events = get_gc_events(gc_service)

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



    load_tokens()
    init_events()


    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0")
