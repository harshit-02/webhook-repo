from flask import Blueprint, json, request ,render_template,jsonify,abort
from app.extensions import mongo
from datetime import datetime
webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')


@webhook.route('/')
def index():
    data=mongo.db.github.find()
    print(data)    

    return render_template('index.html',data=data)
@webhook.route('/api')
def api():
    return {'harshit':{'status':'ok'}}


@webhook.route('/receiver', methods=["POST"])
def receiver():
    if request.headers['Content-Type'] == 'application/json':
        action=request.headers.get('X-GitHub-Event')
        if action == "ping":
            return jsonify({'msg': 'Ok'})
        if action == "push":
            info=request.get_json()
            
            print(type(info))
            if info['commits'][0]['distinct'] == True:
                
                requestId=info['commits'][0]["id"]
                author=info['commits'][0]["author"]["name"]
                timeStamp=info['commits'][0]["timestamp"]
                # timeStamp=datetime.strptime(timeStamp,"%Y-%m-%dT%H:%M:%SZ").strftime('%Y-%m-%d %I:%M:%S %p')
                toBranch=info['ref']
                toBranch=toBranch.split('/')
                toBranch=toBranch[2]
                mongo.db.github.insert({
                    'request_id':requestId,
                    'author':author,
                    'timestamp':timeStamp,
                    'action':action,
                    'tobranch':toBranch
                })

                
                return jsonify({'msg': 'Ok'}), 200
        if action == "pull_request":
            info=request.get_json()
            status=info['action']
            if status=='opened':
                requestId=info['pull_request']['id']
                author=info['pull_request']['head']['label']
                author=author.split(':')
                author=author[0]
                fromBranch=info['pull_request']['head']['ref']
                toBranch=info['pull_request']['base']['ref']
                timeStamp=info['pull_request']['created_at']
                timeStamp=datetime.strptime(timeStamp,"%Y-%m-%dT%H:%M:%SZ").strftime('%Y-%m-%d %I:%M:%S %p')
                mongo.db.github.insert({
                    'request_id':requestId,
                    'author':author,
                    'action':action,
                    'status':status,
                    'timestamp':timeStamp,
                    'frombranch':fromBranch,
                    'tobranch':toBranch
                })
                return jsonify({'msg': 'Ok'}), 200
                
            if status =='closed':
                if info['pull_request']['merged'] == True :
                    
                    requestId=info['pull_request']['id']
                    author=info['pull_request']['head']['label']
                    author=author.split(':')
                    author=author[0]
                    fromBranch=info['pull_request']['head']['ref']
                    toBranch=info['pull_request']['base']['ref']
                    timeStamp=info['pull_request']['created_at']
                    timeStamp=datetime.strptime(timeStamp,"%Y-%m-%dT%H:%M:%SZ").strftime('%Y-%m-%d %I:%M:%S %p')
                    mongo.db.github.insert({
                        'request_id':requestId,
                        'status':status,
                        'merged':True,
                        'author':author,
                        'action':action,
                        'timestamp':timeStamp,
                        'frombranch':fromBranch,
                        'tobranch':toBranch
                    })

                if info['pull_request']['merged'] == False:
                    requestId=info['pull_request']['id']
                    author=info['pull_request']['head']['label']
                    author=author.split(':')
                    author=author[0]
                    fromBranch=info['pull_request']['head']['ref']
                    toBranch=info['pull_request']['base']['ref']
                    timeStamp=info['pull_request']['created_at']
                    timeStamp=datetime.strptime(timeStamp,"%Y-%m-%dT%H:%M:%SZ").strftime('%Y-%m-%d %I:%M:%S %p')
                    mongo.db.github.insert({
                        'request_id':requestId,
                        'merged':False,
                        'author':author,
                        'action':action,
                        'timestamp':timeStamp,
                        'frombranch':fromBranch,
                        'tobranch':toBranch
                    })
                return jsonify({'msg': 'Ok'}), 200

    return abort(400)
                
                
                
                


                        
