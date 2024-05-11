import csv

input_file = 'car_accident.csv'
column_change = '肇事地點'
target_row_index = 1

rows =[]
with open(input_file, newline='', encoding='utf-8') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		rows.append(row)

for row in rows:
	if row[column_change][3] != '區':
		print(row[column_change])
		row[column_change] = ''
	row[column_change] = row[column_change][:4] + '"'


fieldnames = rows[0].keys()
with open(input_file, 'w', newline='', encoding='utf-8') as csvfile:
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	writer.writerows(rows)