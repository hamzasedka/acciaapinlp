from pymongo import MongoClient
import gridfs
from dotenv import load_dotenv
import os
import certifi
import pandas as pd

load_dotenv()

try:
    conn = MongoClient(os.environ.get('MONGO_DB_URI'), tlsCAFile=certifi.where())
    print('Connected')
except:
    print("Error")

db = conn['accia-nuc-def']
fs = gridfs.GridFS(db)

# # Replace the file path with your own file path
# with open('Data\\sigles.csv', 'rb') as f:
#     file_id = fs.put(f, filename='sigle.csv')

# print('File uploaded with ID:', file_id)

# Retrieve sigle.csv
file = fs.find_one({"filename": "sigle.csv"})
df = pd.read_csv(file)

print(df[df.duplicated(subset=['Sigle', 'Domaine'], keep=False)].iloc[240:])