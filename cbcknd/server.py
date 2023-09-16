import flask
import json
from flask import request, jsonify

from gcalendar import get_gc_service, get_gc_events

app = flask.Flask(__name__)

event_dict = {}
gc_service = None
tokens_dict = {}
setup_dict = {}
user_messages = []


@app.route('/')
def hello_world():
        return 'Hello, World!'

@app.route('/calupdates', methods=['POST', "GET"])
def calupdates():
    json_data = request.data.decode('utf-8')

    print(request.headers)

    print(json_data)

    updated_evs = get_updated_events()

    print(updated_evs)

    return 'Hello, World2!'


@app.route('/tokens', methods=['POST'])
def receive_tokens():
    global tokens_dict
    json_data = json.loads(request.data.decode('utf-8'))
    print(json_data)

    keys = ["whoop", "calendar"]
    for k in keys:
        tokens_dict[k] = ""
        if k in json_data:
            tokens_dict[k] = json_data[k]
        else:
            print("no token received for " + k)
    return 'Hello, Tokens!'


@app.route('/setup', methods=['POST'])
def receive_setup():
    global setup_dict
    json_data = json.loads(request.data.decode('utf-8'))
    print(json_data)
    
    setup_dict["sports"] = []
    setup_dict["objective"] = ""

    if "sports" in json_data:
        setup_dict["sports"] = json_data["sports"]
    if "objective" in json_data:
        setup_dict["objective"] = json_data["objective"]

    return 'Hello, Setup!'


@app.route('/adapt', methods=['POST'])
def receive_adapt():
    global user_messages
    json_data = json.loads(request.data.decode('utf-8'))
    print(json_data)

    if "text" in json_data:
        user_messages.append(json_data["text"])

    return 'Hello, Adapt!'


def init_events():
     global gc_service, event_dict

     gc_service = get_gc_service()

     gc_events = get_gc_events(gc_service)

     for event in gc_events:
          event_dict[event['id']] = event

def get_updated_events():
    global gc_service, event_dict

    gc_events = get_gc_events(gc_service)

    updated_events = []

    for event in gc_events:
        if event['id'] not in event_dict:
            updated_events.append(event)
            event_dict[event['id']] = event
        elif event_dict[event['id']]['updated'] != event['updated']:
            updated_events.append(event)
            event_dict[event['id']] = event

    return updated_events


if __name__ == '__main__':
    init_events()
    app.run(host='0.0.0.0')

