import random
import pandas as pd
import csv

def escape_string(value):
    """ Escape special characters in the string for SQL insertion """
    if isinstance(value, str):
        return value.replace("'", "''").replace("\\", "\\\\")
    return value

# Read the CSV file
try:
    df = pd.read_csv('nai_pharma .csv', quoting=csv.QUOTE_ALL)
except Exception as e:
    print(f"Error reading CSV file: {e}")
    exit(1)

insert_scripts = []

for index, row in df.iterrows():
    try:
        # Apply escaping to each field
        first_name = escape_string(row['First Name'])
        last_name = escape_string(row['Last Name'])
        email = escape_string(row['Emails'])
        password = escape_string(row['Password'])
        facility_name = escape_string(row['Facility_Name'])
        registration_number = escape_string(row['Registration_Number'])
        street = escape_string(row['Street'])

        # Insert script for users table
        users_insert = f"INSERT INTO users (id, first_name, last_name, email, password, phone, user_type, status, mail_verified, phone_verified) VALUES ({row['user_id']}, '{first_name}', '{last_name}', '{email}', '{password}', '07{random.randint(10000000, 99999999)}', 'OWNER', 'VERIFIED', 0, 0);"
        insert_scripts.append(users_insert)

        # Insert script for business table
        business_insert = f"INSERT INTO business (id, owner_id, name, country, pharmacode, status, type, currency, test, address) VALUES ({row['business_id']}, {row['user_id']}, '{facility_name}', 'KENYA', '{registration_number}', 'VERIFIED', 'PHARMACY', 'KES', 1, '{street}');"
        insert_scripts.append(business_insert)

        # Insert script for branch table
        branch_insert = f"INSERT INTO branch (id, name, address, main, business_id) VALUES ({row['branch_id']}, 'Main Branch', '{street}', 0, {row['business_id']});"
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
