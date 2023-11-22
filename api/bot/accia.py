from collections import Counter
import json
import pickle
import torch
import spacy
import re
import shap
import pandas as pd
import numpy as np
from googletrans import Translator

from transformers import CamembertTokenizer, CamembertForSequenceClassification
from IPython.core.display import HTML
import matplotlib.pyplot as plt
#from autocorrect import Speller

from .patterns import date_patterns, date_range_patterns, comp_patterns, doc_patterns, serial_numbers_pattern, event_pattern, informations_pattern, sigle_pattern, domaine_pattern
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from .Ent import Ent
from .months_mapper import months_map


class Accia:

    def __init__(self, transformer_model_path, crit_model_path):
        self.model = CamembertForSequenceClassification.from_pretrained('camembert-base', 
            num_labels = 11)
        self.model.load_state_dict(torch.load(f'./Models/{transformer_model_path}'))
        self.crit_model = CamembertForSequenceClassification.from_pretrained('camembert-base', 
            num_labels = 3)
        self.crit_model.load_state_dict(torch.load(f'./Models/{crit_model_path}'))
        with open("Models/labels_dict.json", 'r', encoding='utf-8') as f:
            self.labels = json.load(f)
        with open("Models/crit_le3.le", 'rb') as f:
            self.crit_le = pickle.load(f)
        self.init_spacy_ruler()

        self.tokenizer = CamembertTokenizer.from_pretrained("camembert-base")
        self.max_token_len = 128
        self.explainer = shap.Explainer(self.predict_shap, self.tokenizer, output_names=list(self.labels.keys()))
        self.crit_explainer = shap.Explainer(self.predict_crit_shap, self.tokenizer, output_names=self.crit_le.classes_)

        #self.spell = Speller(lang='fr')
        self.translator = Translator()
        

    def init_spacy_ruler(self):
        self.nlp = spacy.blank('fr')
        ruler = self.nlp.add_pipe('entity_ruler')
        ruler.add_patterns(date_patterns)
        ruler.add_patterns(date_range_patterns)
        ruler.add_patterns(comp_patterns)
        ruler.add_patterns(doc_patterns)
        ruler.add_patterns(serial_numbers_pattern)
        ruler.add_patterns(event_pattern)
        ruler.add_patterns(informations_pattern)
        ruler.add_patterns(sigle_pattern)
        ruler.add_patterns(domaine_pattern)
        
    def predict_intention(self, requests):
        '''Function that predicts the intention of a given request'''

        with torch.no_grad():
            self.model.eval()
            input_ids, attention_mask = self.preprocess(requests)
            retour = self.model(input_ids, attention_mask=attention_mask)
            label_value = torch.argmax(retour[0], dim=1)[0].item()
            self.predicted_label = list(self.labels.keys())[list(self.labels.values()).index(label_value)]
        
        return self.predicted_label

    def predict_criticity(self, requests):
        '''Function that predicts the criticity of a given request'''
        with torch.no_grad():
            self.crit_model.eval()
            input_ids, attention_mask = self.preprocess(requests)
            retour = self.crit_model(input_ids, attention_mask=attention_mask)
            
        return self.crit_le.inverse_transform(torch.argmax(retour[0], dim=1))[0]

    def predict_shap(self, requests):
        with torch.no_grad():
            self.model.eval()
            input_ids, attention_mask = self.preprocess(requests)
            retour = self.model(input_ids, attention_mask=attention_mask)
            
            return retour[0]

    def predict_crit_shap(self, requests):
        with torch.no_grad():
            self.crit_model.eval()
            input_ids, attention_mask = self.preprocess(requests)
            retour = self.crit_model(input_ids, attention_mask=attention_mask)
            
            return retour[0]

    def preprocess(self, requests):
        encoded_batch = self.tokenizer.batch_encode_plus(requests,
                                                    truncation=True,
                                                    pad_to_max_length=True,
                                                    return_attention_mask=True,
                                                    return_tensors = 'pt')
        return encoded_batch['input_ids'], encoded_batch['attention_mask']

    def get_shap_plot(self, request):
        shap_values = self.explainer([request])
        html = shap.plots.text(shap_values[0], display=False)
        return html

    def get_crit_shap_plot(self, request):
        shap_values = self.crit_explainer([request])
        html = shap.plots.text(shap_values[0], display=False)
        return html

    def most_frequent(List):
        occurence_count = Counter(List)
        return occurence_count.most_common(1)[0][0]
        

    def get_entities(self, request):

        doc = self.nlp(request)
        procesed_ents = []
        for ent in doc.ents:
            if ent.label_ == 'date':
                ent_processed = self.process_date_range(ent)
                procesed_ents.append(ent_processed)
            elif ent.label_ == 'dateRange':
                ent_processed = self.process_date(ent)
                procesed_ents.append(ent_processed)
            elif ent.label_ == 'sigle':
                if ent.text.isupper():
                    procesed_ents.append(ent)
            else:
                procesed_ents.append(ent)

        dict_ents = {}
        for ent in procesed_ents:
            dict_ents[ent.label_] = ent.text
        return dict_ents

    def process_date_range(self, ent):
        if 'depuis' in ent.text.lower():
            end_date = date.today()
            if 'hier' in ent.text.lower():
                start_date = end_date - timedelta(days=1)
            elif 'jour' in ent.text.lower():
                nb_jours = re.search('\d', ent.text)[0]
                start_date = end_date - timedelta(days=int(nb_jours))
            elif 'mois' in ent.text.lower():
                nb_month = re.search('\d', ent.text)[0]
                start_date = end_date + relativedelta(months=-int(nb_month))
            elif 'semaine' in ent.text.lower():
                nb_weeks = re.search('\d', ent.text)[0]
                start_date = end_date + relativedelta(weeks=-int(nb_weeks))
            elif re.search(r'\bans?\b', ent.text.lower()):
                print('IN')
                nb_years = re.search('\d', ent.text)[0]
                start_date = end_date + relativedelta(years=-int(nb_years)) 
            date_range = start_date.strftime("%d/%m/%Y") + ' - ' + end_date.strftime("%d/%m/%Y")
        ent_processed = Ent(date_range, ent.start_char, ent.end_char, ent.label_)

        return ent_processed

    def process_date(self, ent):
        date_str = ent.text
        if '/' not in date_str:
            for month, month_short in months_map.items():
                if month in ent.text:
                    date_str = date_str.replace(month, month_short)
            if re.search(r'\d{4}', date_str):
                date_obj = datetime.strptime(date_str, "%d %b %Y")
            else:
                date_str = datetime.strptime(date_str, "%d %b")
                date_obj = date_str.replace(year=date.today().year)
            ent_processed = Ent(date_obj.strftime("%d/%m/%Y"), ent.start_char, ent.end_char, ent.label_)
        else:
            if len(date_str) <= 5:
                date_obj = datetime.strptime(date_str, "%d/%m")
                date_obj = date_obj.replace(year=date.today().year)
            else:
                if len(date_str.split('/')[2]) > 2:
                    date_obj = datetime.strptime(date_str, "%d/%m/%Y")
                else:
                    date_obj = datetime.strptime(date_str, "%d/%m/%y")
            ent_processed = Ent(date_obj.strftime("%d/%m/%Y"), ent.start_char, ent.end_char, ent.label_)

        return ent_processed

    def get_criticity_level(self, request, intention):

        ''' Function that returns the level of criticity of the request, 
        using the intention and keywords'''

        if 'corriger' in intention or 'urgence' in request:
            return 'urgent'
        else:
            return 'standard'

    def get_def_sigle(self, ents, domaine):
        if not any('SIGLE' in sl for sl in ents):
            return "Aucun sigle correspondant trouvés"
        else:
            for ent in ents:
                if ent[1] == 'SIGLE':
                    sigle = ent[0]
            if not domaine:
                df =self.sigle_df[self.sigle_df['Sigle'] == sigle]
                if len(df) == 1:
                    if df['Domaine'].values == 'Sigles US':
                        need_trans, to_translate = self.needs_translation(df['Définition'].values[0])
                        if need_trans:
                            res = df['Définition'].values[0] + '\n' + 'Traduction proposée : '
                            res += self.translator.translate(to_translate, src='en', dest='fr').text
                            return res
                        else:
                            return df['Définition'].values[0]
                    else:
                        return df['Définition'].values[0]
                else:
                    domaines = [elt for elt in np.unique(df[['Domaine']].values)]
                    if len(domaines) == 1:
                        return self.get_def_sigle(ents, domaines[0])
                    else:
                        response = "De quel(s) domaine(s) parlez-vous ?\n"
                        for dom in domaines:
                            response += dom
                            response += '\n'
                        return response
            else:
                df = self.sigle_df[(self.sigle_df['Sigle'] == sigle) & (self.sigle_df['Domaine'] == domaine)]['Définition']
                if len(df) == 1:
                    if domaine == 'Sigles US':
                        need_trans, to_translate = self.needs_translation(df.values[0])
                        if need_trans:
                            res = df.values[0] + '\n' + 'Traduction proposée : '
                            res += self.translator.translate(to_translate, src='en', dest='fr').text
                            return res
                        else:
                            return df.values[0]
                    else:
                        return df.values[0]
                else:
                    return list(df.values)

    def needs_translation(self, definition):
        splitted = definition.split(' - ')
        if len(splitted) == 2:
            return (False, None)
        else:
            splitted = definition.split("=")
            if len(splitted) == 2:
                return (False, None)
            else:
                splitted = definition.split(",")
                if len(splitted) == 2:
                    return (False, None)
                else:
                    return (True, splitted[0].split(':')[1].strip())

    def check_missing_ents(self, intention, ents):

        ents_missing = []

        if intention == 'document':
            ents_needed = ['COMPOSANT', 'SERIAL_NUMBER', 'DOCUMENT']
            for ent in ents_needed:
                if not any(ent in sl for sl in ents):
                    ents_missing.append(ent)

        return ents_missing

    def get_response_document(self, missing_ents):
        if missing_ents:
            res = 'Veuillez précisez : \n'
            for ent in missing_ents:
                res += ("- " + ent + '\n')
        else:
            res = "Voici le document demandé"

        return res

            