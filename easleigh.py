import csv


def generate_update_statements(csv_file):
    update_statements = []

    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            item_code = row['Item Code'].strip()
            stock_balance = row['Stock Balance'].strip().replace(',', '')  # Remove commas

            if item_code:
                if stock_balance == '-':
                    stock_balance = 0
                else:
                    try:
                        stock_balance = int(float(stock_balance))
                    except ValueError:
                        print(f"Skipping invalid stock balance for item code {item_code}: {stock_balance}")
                        continue

                update_statement = f"UPDATE products SET quantity = {stock_balance} WHERE product_code = '{item_code}';"
                update_statements.append(update_statement)

    return update_statements


# Usage
csv_file = 'StockReport-as-at-01Jul-NBO - rptStockandSalesValuationneo.rp.csv'
update_statements = generate_update_statements(csv_file)

# Print or execute the update statements
for statement in update_statements:
    print(statement)
    # If you want to execute the statements, you can use a database connection here
    # cursor.execute(statement)
    # connection.commit()