from flask import Flask, abort, json, jsonify, request  # make_response

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


@app.route('/api/events/')
def list_events():
    events_dict = []
    for ev in events:
        events_dict.append(ev.__dict__)
    return jsonify(events_dict)


@app.route('/api/events/', methods=['POST'])
def create_event():
    # parsing
    data = json.loads(request.data)
    name = data.get('name')
    local = data.get('local')

    # validation
    if not name:
        abort(400, 'Event name is required.')

    # created event
    if local:
        event = Event(name=name, local=local)
    else:
        event = EventOnline(name=name)

    events.append(event)

    return {
        'id': event.id,
        'url': f'/api/events/{event.id}/'
    }


@app.errorhandler(404)
def dont_found(error):
    data_error = {"error": str(error)}
    return (jsonify(data_error), 404)


def get_event_or_404(id):
    for ev in events:
        if ev.id == id:
            return ev
    abort(404, 'Event not found')


@app.route('/api/events/<int:id>/')
# 127.0.0.1/api/eventos/id:int
def detail_event(id):
    ev = get_event_or_404(id)
    return jsonify(ev.__dict__)


@app.route('/api/events/<int:id>/', methods=['DELETE'])
def delete_event(id):
    ev = get_event_or_404(id)
    events.remove(ev)
    return jsonify(id=id)


@app.route('/api/events/<int:id>/', methods=['PUT'])
def edit_event(id):

    # parsing
    data = request.get_json()
    name = data.get('name')
    local = data.get('local')

    # validation
    if not name:
        abort(400, 'Event name is required.')

    if not local:
        abort(400, 'Local name is required.')

    ev = get_event_or_404(id)
    ev.name = name
    ev.local = local

    return jsonify(ev.__dict__)


@app.route('/api/events/<int:id>/', methods=['PATCH'])
def edit_event_partial(id):

    # parsing
    data = request.get_json()
    # {} -> don't want actualized anything
    # {'name': ''} -> clear name -> don't can
    # {'name': 'Java class'}
    ev = get_event_or_404(id)
    if 'name' in data.keys():
        # Want edit the name
        name = data.get('name')
        if not name:
            abort(400, 'Name is required.')
        ev.name = name

    if 'local' in data.keys():
        local = data.get('local')
        if not local:
            abort(400, 'Local is required.')
        ev.local = local

    return jsonify(ev.__dict__)
