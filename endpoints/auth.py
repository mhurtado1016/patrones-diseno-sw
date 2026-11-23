from flask import request
from flask_restful import Resource

import config


class AuthenticationResource(Resource):
    def post(self):
        body = request.get_json(silent=True) or {}
        if (body.get("username") == config.DEMO_USERNAME
                and body.get("password") == config.DEMO_PASSWORD):
            return {"token": config.DEMO_TOKEN}, 200
        return {"message": "unauthorized"}, 401
