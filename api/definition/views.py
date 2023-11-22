from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from pymongo import MongoClient
import gridfs
from dotenv import load_dotenv
import os
import certifi
import pandas as pd

load_dotenv()

# Connect to database and retrieve sigle.csv
try:
    conn = MongoClient(os.environ.get('MONGO_DB_URI'), tlsCAFile=certifi.where())
except:
    print("Could not connect to MongoDB.")

db = conn['accia-nuc-def']
fs = gridfs.GridFS(db)

# Retrieve sigle.csv
file = fs.find_one({"filename": "sigle.csv"})
definitions = pd.read_csv(file)


definition_namespace = Namespace('Definition', description='a namespace that contains all functionalities related to the intention "définition"')

# Replace this with your own model
definition_model = definition_namespace.model('Definition', {
    'definitions': fields.List(fields.Nested(definition_namespace.model('DefinitionFields', {
        'sigle': fields.String(required=True, description='The sigle'),
        'domaine': fields.String(required=True, description='The domain of the definition'),
        'definition': fields.String(required=True, description='The definition')
    })), required=True, description='List of definitions')
})

@definition_namespace.route('/<sigle>')
class Definition(Resource):
    @definition_namespace.doc('get_definition')
    @definition_namespace.marshal_with(definition_model)
    def get(self, sigle):
        result = definitions.loc[definitions['Sigle'] == sigle, ['Sigle', 'Domaine', 'Définition']] \
                           .rename(columns={'Sigle': 'sigle', 'Domaine': 'domaine', 'Définition': 'definition'}) \
                           .to_dict('records')
        if result:
            return {'definitions': result}
        else:
            definition_namespace.abort(404, message=f"Definition of '{sigle}' doesn't exist")

@definition_namespace.route('/<sigle>/<domaine>')
class Definition(Resource):
    @definition_namespace.doc('get_definition')
    @definition_namespace.marshal_with(definition_model)
    def get(self, sigle, domaine):
        result = definitions.loc[(definitions['Sigle'] == sigle) & (definitions['Domaine'].str.lower() == domaine.lower()), 
                                 ['Sigle', 'Domaine', 'Définition']] \
                           .rename(columns={'Sigle': 'sigle', 'Domaine': 'domaine', 'Définition': 'definition'}) \
                           .to_dict('records')
        if result:
            return {'definitions': result}
        else:
            definition_namespace.abort(404, message=f"Definition of '{sigle}' in domain '{domaine}' doesn't exist")



