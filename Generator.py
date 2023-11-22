import pandas as pd
import pymongo

# Load CSV file
csv_file = 'nai_pharma .csv'  # Replace with your CSV file path
df = pd.read_csv(csv_file)

# MongoDB connection details
mongo_uri = ("mongodb://archer:malingu@ac-r0bcexe-shard-00-00.h5wj3us.mongodb.net:27017,"
                         "ac-r0bcexe-shard-00-01.h5wj3us.mongodb.net:27017,"
                         "ac-r0bcexe-shard-00-02.h5wj3us.mongodb.net:27017/?ssl=true&replicaSet=atlas-gvmkrc-shard-0"
                         "&authSource=admin&retryWrites=true&w=majority")
db_name = 'JungoUsers'  # Replace with your database name
collection_name = 'users'  # Replace with your collection name

# Connect to MongoDB
client = pymongo.MongoClient(mongo_uri)
db = client[db_name]
collection = db[collection_name]

# Fetch names from MongoDB
mongo_docs = collection.find({}, {'_id': 0, 'name': 1})
mongo_names = [doc['name'] for doc in mongo_docs]

# Filter DataFrame
filtered_df = df[~df['Facility_Name'].isin(mongo_names)]

# remove column named email
filtered_df = filtered_df.drop('Emails', axis=1)
# save to csv
filtered_df.to_csv('filtered.csv', index=False)