import csv

general_dict = {}

with open("test.csv", "r") as test:
    content = csv.DictReader(test, fieldnames = ["name", "age"])
    for row in content:
        general_dict[row['name']] = row['age']

print(general_dict)

insert_name = "Hannah"
insert_age = 3

with open("test.csv", "a") as test:
    writer = csv.DictWriter(test, fieldnames = ["name", "age"])
    writer.writerow({"name" : insert_name, "age" : insert_age})
