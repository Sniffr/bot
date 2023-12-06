import pandas as pd

# Load the CSV file
file_path = 'updated_business_profiles.csv' # Replace with your CSV file path
data = pd.read_csv(file_path)

# Remove duplicates based on a specific column
# Replace 'your_column_name' with the name of the column you want to check for duplicates
data = data.drop_duplicates(subset='Facility_Name')

# Save the result to a new CSV file
output_file_path = 'output_file_dedup.csv' # Replace with your desired output file path
data.to_csv(output_file_path, index=False)
