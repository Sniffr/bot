import csv
import os


def generate_sql_from_csv(csv_file_path, output_sql_file):
    # SQL script header with system variable handling
    sql_script = """
-- Store the original value of sql_require_primary_key
SET @original_sql_require_primary_key = @@sql_require_primary_key;

-- Temporarily disable the sql_require_primary_key restriction
SET SESSION sql_require_primary_key = 0;

-- Create a temporary table to hold the CSV data
CREATE TEMPORARY TABLE temp_csv (
    auto_number INT,
    itemcode VARCHAR(50),
    itemname VARCHAR(255),
    categoryname VARCHAR(50),
    unitname_abbreviation VARCHAR(50)
);

-- Insert the CSV data into the temporary table
INSERT INTO temp_csv (auto_number, itemcode, itemname, categoryname, unitname_abbreviation) VALUES
"""

    # Read CSV and generate batch INSERT values
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip header row
        values = []
        for row in csv_reader:
            # Escape single quotes in the data
            escaped_row = [item.replace("'", "''") for item in row]
            values.append(
                f"({escaped_row[0]}, '{escaped_row[1]}', '{escaped_row[2]}', '{escaped_row[3]}', '{escaped_row[4]}')")

    # Join all values with commas and add to the SQL script
    sql_script += ",\n".join(values) + ";\n"

    # Add the search, stock check, and price information query
    sql_script += """
-- Perform the search, stock check, and price information query
SELECT 
    csv.itemcode,
    csv.itemname,
    p.id AS product_id,
    p.name AS product_name,
    p.brand AS product_brand,
    CASE 
        WHEN p.id IS NOT NULL THEN 'Found'
        ELSE 'Not Found'
    END AS product_status,
    COALESCE(stock_count.branches_in_stock, 0) AS branches_in_stock,
    COALESCE(price_info.lowest_selling_price, 0) AS lowest_selling_price,
    COALESCE(price_info.highest_selling_price, 0) AS highest_selling_price
FROM 
    temp_csv csv
LEFT JOIN 
    products p ON LOWER(csv.itemname) = LOWER(p.name) OR LOWER(csv.itemname) = LOWER(p.brand)
LEFT JOIN 
    (
        SELECT 
            product_id, 
            COUNT(DISTINCT branch_id) AS branches_in_stock
        FROM 
            stock
        WHERE 
            quantity > 0
        GROUP BY 
            product_id
    ) stock_count ON p.id = stock_count.product_id
LEFT JOIN 
    (
        SELECT
            product_id,
            MIN(selling_price) AS lowest_selling_price,
            MAX(selling_price) AS highest_selling_price
        FROM
            stock
        GROUP BY
            product_id
    ) price_info ON p.id = price_info.product_id
ORDER BY 
    csv.auto_number;

-- Clean up: Drop the temporary table
DROP TEMPORARY TABLE temp_csv;

-- Restore the original value of sql_require_primary_key
SET SESSION sql_require_primary_key = @original_sql_require_primary_key;
"""

    # Write the SQL script to a file
    with open(output_sql_file, 'w') as sql_file:
        sql_file.write(sql_script)

    print(f"SQL script has been generated and saved to {output_sql_file}")


# Usage
csv_file_path = 'Drugs and consumables.csv'  # Your CSV file path
output_sql_file = 'product_search_stock_and_price_check.sql'

generate_sql_from_csv(csv_file_path, output_sql_file)