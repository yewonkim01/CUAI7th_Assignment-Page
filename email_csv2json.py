"""
이름, 이메일 정보 담긴 csv 파일 json으로 변환해주는 코드
"""

import csv
import json

json_data = {}
set_data = set()

with open('BASIC_email.csv', 'r', encoding='UTF-8') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        name = row['\ufeff이름'] #이름 앞에 자꾸 이상한 문자가 붙어요
        email = row['이메일']
        json_data[email] = name
        set_data.add(email)
#print(set_data)


with open('BASIC_email.json', 'w', encoding = 'UTF-8') as json_file:
    json.dump(json_data, json_file, ensure_ascii=False)

    #ensure_ascii 안하면 이름 이상한 문자로 출력됨