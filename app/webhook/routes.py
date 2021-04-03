from flask import Blueprint, json, request

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
def receiver():
    if request.headers['Content-Type'] == 'application/json':
        info=json.dumps(request.json)
        print(info)
        return {'harshit':'webhook'}, 200
