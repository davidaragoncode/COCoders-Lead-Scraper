import csv

# opening the CSV file
with open('keywords.csv', mode ='r')as file:
# reading the CSV file
    csvFile = csv.reader(file)

    # displaying the contents of the CSV file
    list = [lines[0] for lines in csvFile]
    print(len(list))