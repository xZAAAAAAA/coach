import flask
import json
from flask import request

from gcalendar import get_gc_service, get_gc_events

from whoopy import WhoopClient
from user_model import User

app = flask.Flask(__name__)

event_dict = {}
gc_service = None
tokens_dict = {}
setup_dict = {}
user_messages = []
user_profile = User()


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

    return "Hello, World3!"


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
    global setup_dict, user_profile

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
        user_profile.height = measurements["height_meters"]

        user_profile.calc_fitness_level(wc.get_workouts())

    return "Hello, Setup!"


@app.route("/adapt", methods=["POST"])
def receive_adapt():
    global user_messages

    json_data = request.json
    print(json_data)

    if "text" in json_data:
        user_messages.append(json_data["text"])

    return "Hello, Adapt!"


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


if __name__ == "__main__":
    load_tokens()
    init_events()
    app.run(host="0.0.0.0")
