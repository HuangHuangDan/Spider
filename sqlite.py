import sqlite3

conn = sqlite3.connect("test.db")

c = conn.cursor()
# sql = '''
# create table company(
#     id int primary key not null,
#     name text not null,
#     age int not null
# );
# '''
sql1 = '''insert into company(id, name, age)
values(1, 'zhang', 10)
values(3, 'zhao', 15)
'''
sql2 = '''insert into company(id, name, age)
values(2, 'li', 20)
'''

# c.execute(sql1)
# c.execute(sql2)
sql3 = "select id, name, age from company"
cursor = c.execute(sql3)
for row in cursor:
    print('id = ', row[0])
    print('name = ', row[1])
    print('age = ', row[2],"\n")


conn.commit()
conn.close()

print("open successfully")
