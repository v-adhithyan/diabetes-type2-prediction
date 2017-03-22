import csv

with open("input.csv", "rb") as input_file:
    reader = csv.DictReader(input_file)
    for row in reader:
        print row['age']
