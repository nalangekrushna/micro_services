import os, uuid, requests
from flask import Flask, request, Response

app = Flask(__name__)
PORT = 4005
POSTS = {}

@app.route("/health")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/events", methods=[ "POST" ] )
def events() :
    id = uuid.uuid4().hex[:4]
    event = request.get_json()
    print('event occured in event bus')
    print(event)
    requests.post(url='http://localhost:4000/events', json=event)             # posts
    requests.post(url='http://localhost:4001/events', json=event)            # comments
    requests.post(url='http://localhost:4002/events', json=event)             # query service to get all comments for given post
    return Response('OK', status=200, mimetype='text/plain')

if __name__ == '__main__' :
    print(f'Listening on port {PORT}')
    routes = ['%s' % rule for rule in app.url_map.iter_rules()]
    print(routes)
    os.environ['FLASK_ENV'] = 'development' 
    app.run(debug=True,port=PORT)  
    