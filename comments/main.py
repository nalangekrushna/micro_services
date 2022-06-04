from crypt import methods
import os, uuid, requests
from flask import Flask, request, Response

app = Flask(__name__)
PORT = 4001
post_id_comments = {}


@app.route("/health")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/posts/<id>/comments', methods=[ "GET", "POST" ] )
def comments(id) :
    if request.method == 'POST' :
        comment_id = uuid.uuid4().hex[:3]
        json_data = request.get_json('content')
        
        temp = {comment_id:json_data['content']}
        # {'comment_id':'value'}
        if id in post_id_comments :
            post_id_comments[id].append(temp)
        else :
            post_id_comments[id] = [temp]
        requests.post(url='http://localhost:4005/events',
            json={ 'type':'CommentCreated', 'current_comment_id':comment_id, 'postId':id, 'content':post_id_comments[id] } 
        )
        return Response(post_id_comments, status=201, mimetype='application/json')
    else : 
        if id in post_id_comments :
            return {id:post_id_comments[id]}
        else :
            return f'no data found for given id : {id}'

@app.route('/events', methods=["POST"] )
def events() :
    event = request.get_json()
    print('Event Received - inside Comments')
    print(event)
    return Response('OK',status=200,mimetype='text/plain')

if __name__ == '__main__' :
    print(f'Listening on port {PORT}')
    routes = ['%s' % rule for rule in app.url_map.iter_rules()]
    print(routes)
    os.environ['FLASK_ENV'] = 'development' 
    app.run(debug=True,port=PORT)  
    