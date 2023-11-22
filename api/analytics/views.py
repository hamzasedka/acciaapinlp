from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from ..models.requests import Request
from http import HTTPStatus

from ..request_checking.views import request_understood_model

analytics_namespace = Namespace('analytics', description="A namespace to retrieive data for analysis purposes")

@analytics_namespace.route('/requests')
class AllRequests(Resource):

    @analytics_namespace.marshal_with(request_understood_model)
    @jwt_required()
    def get(self):
        """
            Retrieve all requests contained in database
        """
        requests = Request.query.all()
        
        return requests, HTTPStatus.OK

@analytics_namespace.route('/requests/<int:user_id>')
class UserRequests(Resource):

    def get(self, user_id):
        """
            Retrieve all requests from a particular user
        """
        pass