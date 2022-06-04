import os, uuid, requests
from flask import Flask, request, Response

app = Flask(__name__)
PORT = 4000
POSTS = {}

@app.route("/health")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/posts", methods=[ "GET", "POST" ] )
def posts() :
    if request.method == 'POST' :
        id = uuid.uuid4().hex[:4]
        json_data = request.get_json('title')
        POSTS[id] = json_data
        requests.post(url='http://localhost:4005/events', 
            json= {'type':'PostCreated', 
                 'id':id,'title':json_data['title']}
        )
        return Response(id, status=201, mimetype='application/json')
    else : 
        return POSTS

@app.route('/events', methods=["POST"] )
def events() :
    event = request.get_json()
    print('Event Received - inside Posts')
    print(event)
    return Response('OK',status=200,mimetype='text/plain')

if __name__ == '__main__' :
    print(f'Listening on port {PORT}')
    routes = ['%s' % rule for rule in app.url_map.iter_rules()]
    print(routes)
    os.environ['FLASK_ENV'] = 'development' 
    app.run(debug=True,port=PORT)  
    