from pprint import pprint
import csv
import re

with open('phonebook_raw.csv', encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

for row in contacts_list[1:]:
    for index, item in enumerate(row):
        pattern = r'\s'
        result = item.strip()
        row[index] = result
        if 'доб.' in item:
            pattern = r'(\+7|8)\s?(\(?(\d{3})\)?)[^0-9]?(\d{3})[^0-9]?' \
                      r'(\d{2})[^0-9]?(\d+)\s?\(?доб.\s?(\d+)\)?'
            u = r'+7(\3)\4-\5-\6 доб.\7'
            result = re.sub(pattern, u, item)
            row[index] = result
        else:
            pattern = r'(\+7|8)\s?(\(?(\d{3})\)?)[^0-9]?(\d{3})[^0-9]?(\d{2})[^0-9]?(\d+)'
            u = r'+7(\3)\4-\5-\6'
            result = re.sub(pattern, u, item)
            row[index] = result

for row in contacts_list[1:]:
    for index, item in enumerate(row[:3]):
        pattern = r'\s'
        if item == '':
            del row[index]
        elif len(re.findall(pattern, item)) == 1:
            result = item.split(' ')
            row[index] = result[0]
            row[index + 1] = result[1]
            break
        elif len(re.findall(pattern, item)) == 2:
            result = item.split(' ')
            row[index] = result[0]
            row[index + 1] = result[1]
            row[index + 2] = result[2]
            break

repeat_list = []
for row in contacts_list[1:]:
    for row_ in contacts_list[contacts_list.index(row) + 1:]:
        if row[0] == row_[0] and row[1] == row_[1]:
            for index, item in enumerate(row):
                if item == '' and row_[index] != '':
                    row[index] = row_[index]
            repeat_list.append(row_)
for row in contacts_list[1:]:
    if row in repeat_list:
        contacts_list.remove(row)

with open("phonebook.csv", "w", encoding='utf-8', newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)
