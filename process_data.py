import csv
import os

# Input files
input_files = [
    'data/daily_sales_data_0.csv',
    'data/daily_sales_data_1.csv',
    'data/daily_sales_data_2.csv'
]

# Output file
output_file = 'output.csv'

# Process the data
all_rows = []

for file in input_files:
    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Filter for pink morsel only
            if row['product'].strip().lower() == 'pink morsel':
                # Calculate sales (price * quantity)
                price = float(row['price'].replace('$', ''))
                quantity = int(row['quantity'])
                sales = price * quantity
                
                # Create output row
                all_rows.append({
                    'sales': sales,
                    'date': row['date'],
                    'region': row['region']
                })

# Write output file
with open(output_file, 'w', newline='') as f:
    fieldnames = ['sales', 'date', 'region']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_rows)

print(f"Processed {len(all_rows)} pink morsel transactions")
print(f"Output written to {output_file}")
