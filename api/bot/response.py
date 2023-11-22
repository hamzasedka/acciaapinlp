import pandas as pd

class Response:

    def __init__(self) -> None:
        self.sigle_df = pd.read_csv('./Data/sigles.csv')
        self.ents_to_have = {
            'document': ['component', 'documentType', 'serialNumber'],
            'définition': ['sigle'],
            'état': ['serialNumber'],
            'matériel': ['serialNumber', 'infoType']
        }

    # def get_response(self, intention, ents, dom):
    #     return self.switcher(intention, ents, dom)

    def get_ents_information(self, intention, ents):
        ents_missing = []
        ents_present = []
        ents_to_have = self.ents_to_have[intention]
        if ents:
            for ent in ents_to_have:
                if ent in ents.keys():
                    if ents[ent]:
                        ents_present.append(ent)
                    else:
                        ents_missing.append(ent)
                else:
                    ents_missing.append(ent)
        else:
            ents_missing = ents_to_have

        return ents_missing, ents_present

    def switcher(self, intention, ents, dom):
        if intention == 'définition':
            return self.definition_resp(ents, dom)
        elif intention == 'document':
            return self.document_resp(ents)
        else:
            return {"response": "Cette réponse n'est pas implémentée pour le moment"}

    def definition_resp(self, ents, dom):
        if ents:
            sigle = [k for k, v in ents.items() if v == 'SIGLE']
        else:
            sigle = None
        if sigle:
            if not dom:
                response = self.definition_resp_sigle_not_dom(sigle[0])
            else:
                response = self.definition_resp_sigle_and_dom(sigle[0], dom)
        else:
            response = {"response": "De quoi souhaitez-vous la définition ?"}

        return response

    def definition_resp_sigle_not_dom(self, sigle):
        dom = pd.unique(self.sigle_df[self.sigle_df['Sigle'] == sigle]['Domaine'].values)
        if len(dom) > 1:
            return {"domaines possibles": list(dom)}
        else:
            return self.definition_resp_sigle_and_dom(sigle, dom[0])

    def definition_resp_sigle_and_dom(self, sigle, dom):
        df =self.sigle_df[(self.sigle_df['Sigle'] == sigle) & (self.sigle_df['Domaine'] == dom)]
        definition = df['Définition'].values

        return {"définition":list(definition)}

    def document_resp(self, ents):
        missing_ents = self.check_missing_ents(['COMPOSANT', 'SERIAL_NUMBER', 'DOCUMENT'], ents)
        if missing_ents:
            response = {"entitites_missing": missing_ents}
        else:
            response = 'entitities completed'

        return response
    
    @staticmethod
    def check_missing_ents(ents_to_have, ents):

        if ents:
            missing_ents = []
            for ent in ents_to_have:
                if ent not in ents.values():
                    missing_ents.append(ent)
        else:
            missing_ents = ents_to_have

        return missing_ents
