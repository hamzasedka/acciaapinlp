from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from http import HTTPStatus
from ..models.requests import Request
from ..models.users import User
from  ..bot.accia import Accia
from ..bot.response import Response

accia_namespace = Namespace('LanguageAnalysis', 
    description='a namespace that conatins all functionalities related to the understanding of the request')

accia_bot = Accia('model_edf_1.pt', 'crit_model_3.pt')
accia_response = Response()

user_request_model = accia_namespace.model(
    'UserRequest',{
        "text": fields.String(description="Text of the input user request")
    }
)

request_for_response_model = accia_namespace.model(
    'RequestForResponse',{
        'intention':fields.String(description='The intent of the request', required=True),
        'entities':fields.Raw(description='The entities contained in the request'),
        'criticity':fields.String(description='The criticity of the request', required=True),
        'domaine':fields.String(description='The domain of the sigle', default="")      
    }
)

@accia_namespace.route('/inputDetails')
class RequestUnderstanding(Resource):

    @accia_namespace.expect(user_request_model)
    def post(self):
        """
            Get intention, entities and criticity of the request sent in.
        """
        data = request.get_json()
        user_request = data.get('text')

        entities = accia_bot.get_entities(user_request)
        intention = accia_bot.predict_intention([user_request])
        criticity_level = accia_bot.predict_criticity([user_request])

        response = {
            "intention": intention,
            "entities": entities,
            "criticity_level": criticity_level
        }

        return response, HTTPStatus.OK
        

    # @accia_namespace.expect(request_understood_model)
    # @accia_namespace.marshal_with(request_understood_model)
    # @jwt_required(optional=True)
    # def post(self):
    #     """
    #         Post the request and its understanding in the db
    #     """
        
    #     username = get_jwt_identity()
    #     data = accia_namespace.payload

    #     current_user = User.query.filter_by(username=username).first()

    #     new_request = Request(
    #         text = data['text'],
    #         intention= data['intention'],
    #         entities = data['entities'],
    #         criticity = data['criticity']
    #     )

    #     new_request.user = current_user
    #     new_request.save()

    #     return new_request, HTTPStatus.CREATED


@accia_namespace.route('/intention')
class Intention(Resource):

    @accia_namespace.expect(user_request_model)
    @jwt_required(optional=True)
    def post(self):
        """
            Get intention of the request sent in.
        """

        data = request.get_json()
        user_request = data.get('text')

        intention = accia_bot.predict_intention([user_request])

        return {"Intention": intention}, HTTPStatus.OK


@accia_namespace.route('/entities')
class Entities(Resource):

    @accia_namespace.expect(user_request_model)
    @jwt_required(optional=True)
    def post(self):
        """
            Get entities of the request sent in.
        """

        data = request.get_json()
        user_request = data.get('text')

        entities = accia_bot.get_entities(user_request)

        return {"entities": entities}, HTTPStatus.OK

@accia_namespace.route('/criticity')
class Criticity(Resource):

    @accia_namespace.expect(user_request_model)
    @jwt_required(optional=True)
    def post(self):
        """
            Get criticity of the request sent in.
        """

        data = request.get_json()
        user_request = data.get('text')

        criticity_level = accia_bot.predict_criticity([user_request])

        return {"criticity": criticity_level}, HTTPStatus.OK


