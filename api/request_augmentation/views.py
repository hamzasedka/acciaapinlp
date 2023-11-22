from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from http import HTTPStatus
from ..bot.response import Response

accia_response = Response()

request_augmentation_namespace = Namespace('Checking', 
    description='a namespace that contains all functionalities that check for missing informations in the request')

check_entities_model = request_augmentation_namespace.model(
    'EntityChecker',{
        'entities':fields.Raw(description='The entities contained in the request', required=True),   
    }
)


@request_augmentation_namespace.route('/DocumentEntities')
class EntityCheckDocument(Resource):

    @request_augmentation_namespace.expect(check_entities_model)
    @jwt_required(optional=True)
    def post(self):
        """
            Check if there are any missing entities in the request with intention=document
        """
        data = request.get_json()
        ents = data.get('entities')

        ents_missing, ents_present = accia_response.get_ents_information('document', ents)
        if ents_missing:
            is_complete = False
        else:
            is_complete = True

        return {"entities_missing": ents_missing,
                            "entities_present": ents_present,
                            'is_complete': is_complete}, HTTPStatus.OK

@request_augmentation_namespace.route('/DefinitionEntities')
class EntityCheckDefinition(Resource):

    @request_augmentation_namespace.expect(check_entities_model)
    @jwt_required(optional=True)
    def post(self):
        """
            Check if there are any missing entities in the request with intention=définition
        """
        data = request.get_json()
        ents = data.get('entities')

        ents_missing, ents_present = accia_response.get_ents_information('définition', ents)
        if ents_missing:
            is_complete = False
        else:
            is_complete = True

        return {"entities_missing": ents_missing,
                            "entities_present": ents_present,
                            'is_complete': is_complete}, HTTPStatus.OK
    
@request_augmentation_namespace.route('/EtatEntities')
class EntityCheckEtat(Resource):

    @request_augmentation_namespace.expect(check_entities_model)
    @jwt_required(optional=True)
    def post(self):
        """
            Check if there are any missing entities in the request with intention=état
        """
        data = request.get_json()
        ents = data.get('entities')

        ents_missing, ents_present = accia_response.get_ents_information('état', ents)
        if ents_missing:
            is_complete = False
        else:
            is_complete = True

        return {"entities_missing": ents_missing,
                            "entities_present": ents_present,
                            'is_complete': is_complete}, HTTPStatus.OK
    
@request_augmentation_namespace.route('/MaterielEntities')
class EntityCheckMateriel(Resource):

    @request_augmentation_namespace.expect(check_entities_model)
    @jwt_required(optional=True)
    def post(self):
        """
            Check if there are any missing entities in the request with intention=matériel
        """
        data = request.get_json()
        ents = data.get('entities')

        ents_missing, ents_present = accia_response.get_ents_information('matériel', ents)
        if ents_missing:
            is_complete = False
        else:
            is_complete = True

        return {"entities_missing": ents_missing,
                            "entities_present": ents_present,
                            'is_complete': is_complete}, HTTPStatus.OK