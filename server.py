import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from event import Event
from event_online import EventOnline

ev_online = EventOnline('Live of the Python')
ev2_online = EventOnline('Live of the Javascript')
ev3_online = EventOnline('Live of the Go')
ev = Event('Python Class', 'Rio de Janeiro')
events = [ev_online, ev2_online, ev3_online, ev]


class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('header-test', 'test-header')
            self.end_headers()
            data = f"""
            <html>
                <head>
                    <title>Olá mundo!</title>
                </head>
                <body>
                    <p>Test our HTTP Server!</p>
                    <p>Directory: {self.path}</p>
                </body>
            </html>
            """.encode()
            self.wfile.write(data)
        elif self.path == '/events' or self.path == '/event':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()

            events_html = ''

            for ev in events:
                events_html += f"""
                            <tr>
                                <th>{ev.id}</th>
                                <td>{ev.name}</td>
                                <td><a href="#" title="{ev.name}">{ev.local}</a>
                                </td>
                            </tr>"""  # noqa
            data = f"""
            <html>
                <head>
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">
                    <title>Events!</title>
                </head>
                <body>
                    <table class="table is-striped">
                        <thead>
                        <tr>
                            <th>id</th>
                            <th>Event</th>
                            <th>link</th>
                        </tr>
                        </thead>
                        <tbody>                        
                            {events_html}
                        </tbody>
                    </table>
                </body>
            </html>            
            """.encode()  # noqa
            self.wfile.write(data)
        elif self.path == '/api/events':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            list_dict_events = []
            for ev in events:
                list_dict_events.append({
                    'id': ev.id,
                    'name': ev.name,
                    'local': ev.local
                })

            data = json.dumps(list_dict_events).encode()
            self.wfile.write(data)


server = HTTPServer(('localhost', 8000), SimpleHandler)
server.serve_forever()
