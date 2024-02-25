from DB_class import DB
from email_info import data

"""
firstore DB에 챕터이름의 콜렉션, 학회원들 이름 문서로 등록해주는 코드
"""

chapter = "ch07"

db = DB(chapter, None)

name_list = data.values()

for name in name_list:
    db.register_name(name)