import pandas as pd

class User:
     
    def __init__(self, user_id):
        self.users_df = pd.read_csv('profil_utilisateurs.csv', encoding='utf-8')
        self.user_id = int(user_id)
        row_user = self.users_df[self.users_df['id'] == self.user_id]
        self.name = row_user['prenom'].values[0]
        self.last_name = row_user['nom'].values[0]
        self.full_name = ' '.join([self.name, self.last_name])
        self.pro_status = row_user['statut_pro'].values[0]
        self.expertise = row_user['niveau_expertise'].values[0]
    
    def __str__(self):
        return (f"Utilisateur : {self.full_name}\nStatut professionnel : {self.pro_status}\nNiveau d'expertise : {self.expertise}")
        