import random
import pandas as pd
import csv

# from pymongo import MongoClient
#
# connection_string = "mongodb://archer:malingu@ac-r0bcexe-shard-00-00.h5wj3us.mongodb.net:27017,ac-r0bcexe-shard-00-01.h5wj3us.mongodb.net:27017,ac-r0bcexe-shard-00-02.h5wj3us.mongodb.net:27017/?ssl=true&replicaSet=atlas-gvmkrc-shard-0&authSource=admin&retryWrites=true&w=majority"
# client = MongoClient(connection_string)
# db = client['JungoUsers']
# collection = db['users']
#
# users = collection.find()
# df = pd.read_csv('jungo_business.csv', quoting=csv.QUOTE_ALL)
# # Connect to MongoDB
# client = MongoClient(connection_string)
# email_list = df['pharmacode'].tolist()
#
# # # files = collection.delete_many({"Registration_Number": {"$nin": email_list}})
# # print(files.deleted_count, " documents deleted.")
#
# schedules = db['schedules']
#
# files = schedules.delete_many({})
# print(files.deleted_count, " documents deleted.")



try:
    df = pd.read_csv('Result_7_with_New_Emails.csv')
except Exception as e:
    print(f"Error reading CSV file: {e}")
    exit(1)

insert_scripts = []

for index, row in df.iterrows():
    try:
        # Apply escaping to each field

        old_email = escape_string(row['Emails'])
        new_email = escape_string(row['Emails'])


        # Insert script for users table
    except Exception as e:
        print(f"Error processing row {index}: {e}")

# Save the scripts to a file
try:
    with open('insert_scripts.sql', 'w') as file:
        for script in insert_scripts:
            file.write(script + "\n")
except Exception as e:
    print(f"Error writing to file: {e}")
