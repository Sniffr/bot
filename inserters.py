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


def escape_string(value):
    """ Escape special characters in the string for SQL insertion """
    if isinstance(value, str):
        return value.replace("'", "''").replace("\\", "\\\\")
    return value


# Read the CSV file
try:
    df = pd.read_csv('output_file_dedup.csv', quoting=csv.QUOTE_ALL)
except Exception as e:
    print(f"Error reading CSV file: {e}")
    exit(1)

insert_scripts = []

for index, row in df.iterrows():
    try:
        # Apply escaping to each field
        first_name = escape_string(row['Owner First Name'])
        last_name = escape_string(row['Owner Last Name'])
        email = escape_string(row['Owner Email'])
        password = escape_string(row['Password'])
        facility_name = escape_string(row['Facility_Name'])
        registration_number = escape_string(row['Registration_Number'])
        # street = escape_string(row['Street'])

        # Insert script for users table
        users_insert = f"INSERT INTO users (id, first_name, last_name, email, password, phone, user_type, status, mail_verified, phone_verified) VALUES ({row['user_id']}, '{first_name}', '{last_name}', '{email}', '{password}', '07{random.randint(10000000, 99999999)}', 'OWNER', 'VERIFIED', 0, 0);"
        insert_scripts.append(users_insert)

        # Insert script for business table
        business_insert = f"INSERT INTO business (id, owner_id, name, country, pharmacode, status, type, currency, test, address) VALUES ({row['business_id']}, {row['user_id']}, '{facility_name}', 'KENYA', '{registration_number}', 'VERIFIED', 'PHARMACY', 'KES', 1, '');"
        insert_scripts.append(business_insert)

        # Insert script for branch table
        branch_insert = f"INSERT INTO branch (id, name, address, main, business_id) VALUES ({row['branch_id']}, 'Main Branch', '', 0, {row['business_id']});"
        insert_scripts.append(branch_insert)
    except Exception as e:
        print(f"Error processing row {index}: {e}")

# Save the scripts to a file
try:
    with open('insert_scripts.sql', 'w') as file:
        for script in insert_scripts:
            file.write(script + "\n")
except Exception as e:
    print(f"Error writing to file: {e}")
