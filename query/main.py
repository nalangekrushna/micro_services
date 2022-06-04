import os, uuid, requests
from flask import Flask, request, Response

from query import Query
query_object = {}


app = Flask(__name__)
PORT = 4002
POSTS = {}

@app.route("/health")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/events', methods=["POST"] )
def events() :
    event = request.get_json()
    print('Event Received - inside Query')
    print(event)
    if event.get('type') == 'PostCreated' :
        q = Query(id=event['id'],title=event['title'])
        query_object[event['id']] = q
    elif event.get('type') == 'CommentCreated' :
        if event['postId'] in query_object :
            q = query_object[event['postId']]
            q.update_comments(event['content'])
        else :
            print('Something went wrong. Postid not found while adding a comment to it.')
    else :
        print('something went wrong inside query-main.py. Event type didnot match to any available options.')
        print(event)
    # {'type': 'CommentCreated', 'current_comment_id': '351', 'postId': '901e', 'content': [{'1ec': 'first comment 2'}, {'351': 'first comment 1'}]}
    # {'type': 'PostCreated', 'id': '901e', 'title': 'second try'}
    return Response('OK',status=200,mimetype='text/plain')

if __name__ == '__main__' :
    print(f'Listening on port {PORT}')
    routes = ['%s' % rule for rule in app.url_map.iter_rules()]
    print(routes)
    os.environ['FLASK_ENV'] = 'development' 
    app.run(debug=True,port=PORT)  