from ..request_checking.views import accia_bot, user_request_model
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, make_response
from http import HTTPStatus

explain_namespace = Namespace('ModelAnalysis', 
    description='a namespace that conatins all functionalities related to the models explanation (XAI)')

@explain_namespace.route('/intention')
class IntentionExplain(Resource):

    @explain_namespace.expect(user_request_model)
    @jwt_required(optional=True)
    def post(self):
        """
            Explain the model choice for the intention.
        """

        data = request.get_json()
        user_request = data.get('text')

        html_plot = accia_bot.get_shap_plot(user_request)

        response = make_response(html_plot)
        response.headers.set('Content-Type', 'text/html')

        return response

@explain_namespace.route('/criticity')
class ExplainCriticity(Resource):

    @explain_namespace.expect(user_request_model)
    @jwt_required(optional=True)
    def post(self):
        """
            Explain the model choice for the criticity.
        """
        data = request.get_json()
        user_request = data.get('text')

        htlm_plot = accia_bot.get_crit_shap_plot(user_request)

        response = make_response(htlm_plot)
        response.headers.set('Content-Type', 'text/html')

        return response
