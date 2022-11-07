from flask import Flask, abort, jsonify  # make_response

from event import Event
from event_online import EventOnline

app = Flask(__name__)

ev_online = EventOnline('Live of the Python')
ev2_online = EventOnline('Live of the Javascript')
ev3_online = EventOnline('Live of the Go')
ev = Event('Python Class', 'Rio de Janeiro')
events = [ev_online, ev2_online, ev3_online, ev]


@app.route('/')
def index():
    return "<h1>Flask's run!</h1>"


@app.route('/api/events')
def list_events():
    events_dict = []
    for ev in events:
        events_dict.append(ev.__dict__)
    return jsonify(events_dict)


@app.errorhandler(404)
def dont_found(error):
    data_error = {"error": str(error)}
    return (jsonify(data_error), 404)


@app.route('/api/events/<int:id>/')
# 127.0.0.1/api/eventos/id:int
def detail_event(id):
    for ev in events:
        if ev.id == id:
            return jsonify(ev.__dict__)

    abort(404, 'Event not found')
