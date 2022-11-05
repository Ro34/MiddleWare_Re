import sqlite3
conn = sqlite3.connect('mission.db')





table_name = 'ServicesResourcesTable'
select_name = 'GPU_ESTIMATE'
update_value = "'aaa'"
update_condition_key='ID'
update_condition_value = '1'

def dict_factory(cursor, row):
  # 将游标获取的数据处理成字典返回
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d
# conn.row_factory = dict_factory()
c = conn.cursor()





c.execute("SELECT *  FROM " +table_name + " WHERE " + update_condition_key + " =?",(update_condition_value))
print(c.description)
a = dict_factory(c,c.fetchone())
print("#########3")
print(a)
print(a['ID'])

# # for r in c.fetchall():
# #     a = dict(r)
# d={}
# a = c.fetchall()
# for row in a:

#     print(f"{row['companyid']}, {row['name']}, {row['address']}.")
# print("#########3")
# print(a)
# print(type(a))
# print(1)
# c.close()
# conn.commit()