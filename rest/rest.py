from flask import Flask, url_for, request, json, Response, jsonify
from functools import wraps
app = Flask(__name__)

@app.route('/')
def api_root():
    return 'Bem-Vindo'

@app.route('/articles')
def api_articles():
    return 'List of ' + url_for('api_articles')

@app.route('/articles/<articleid>')
def api_article(articleid):
    return 'You are reading ' + articleid

@app.route('/hellow')
def api_hello():
    if 'name' in request.args:
        return 'Hello ' + request.args['name']
    
    else:
        return 'Hello John Doe'

@app.route('/echo', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_echo():
    if request.method == "GET":
        return "ECHO: GET\n"
    elif request.method == 'POST':
        return "ECHO: POST\n"
    elif request.method == 'PATCH':
        return "ECHO: PATCH\n"
    elif request.method == 'PUT':
        return "ECHO: PUT\n"
    elif request.method == 'DELETE':
        return "ECHO: DELETE"

@app.route('/message', methods = ['POST'])
def api_message():
    if request.headers['Content-Type'] == 'text/plain':
        return "Text Message: " + request.data
    elif request.headers['Content-Type'] == 'application/json':
        return "JSON message: " + json.dumps(request.json)
    elif request.headers['Content-Type'] == 'application/octet-stream':
        f = open('./binary', 'wb')
        f.write(request.data)
        f.close()
        return 'Binary Message Write Success'
    else:
        return '415 Unsupported Media Type'

@app.route('/hello', methods = ['GET'])
def api_hello_get():
    data = {
        'hello': 'world',
        'number': '123'
    }
    js = json.dumps(data)
    resp = jsonify(data)
    resp.status_code = 200
    resp.headers['Link'] = 'http://davyc.com'
    return resp

@app.errorhandler(404)
def not_found(error = None):
    message = {
        'status': 404,
        'message': 'Not Found ' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

def check_auth(usr, password):
    return usr == 'admin' and password == 'secret'

def authenticate():
    message = {'message': "Authentication"}
    resp = jsonify(message)
    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'
    return resp

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return authenticate()
        elif not check_auth(auth.username, auth.password):
            return authenticate
        return f(*args, **kwargs)
    return decorated

@app.route('/protected')
@requires_auth
def protected():
    return 'You are authenticated'




if __name__ == '__main__':
    app.run(debug=True)
