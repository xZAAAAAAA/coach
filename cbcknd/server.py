import flask
from flask import request, jsonify

from gcalendar import get_gc_service, get_gc_events

app = flask.Flask(__name__)

event_dict = {}
gc_service = None

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

