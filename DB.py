import os
import psycopg2
from datetime import datetime, date,timezone,timedelta
from linebot.models.responses import Content

DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a yuanzai1').read()[:-1]

# connect to database
#conn   = psycopg2.connect(DATABASE_URL, sslmode='require')
#cursor = conn.cursor()

# create a table
#create_table_query = '''
#    CREATE TABLE test_table(
#    userid  VARCHAR  PRIMARY KEY,
#    time    TIMESTAMP );
#'''
#execute query
#cursor.execute(create_table_query)
#conn.commit()

#cursor.close()
#conn.close()

# 插入資料
#records = ('Uad6ef6c5ff973a4fdbce4101732f1be8', '2022-8-12 11:00:00')
#table_columns = '(userid, time)'
#postgres_insert_query = f"""INSERT INTO test_table {table_columns} VALUES (%s, %s);"""

#cursor.execute(postgres_insert_query, records)
#conn.commit()

#count = cursor.rowcount
#print(count, "Record inserted successfully into database")
'''
postgres_select_query = f"""SELECT * FROM test_table"""

cursor.execute(postgres_select_query)
rows = cursor.fetchall()

for row in rows:  # 將讀到的資料全部print出來
   print("Data_row = (%s, %s)" %(str(row[0]), str(row[1])))
'''
dt7 = datetime.utcnow().replace(tzinfo=timezone.utc)
dt8 = dt7.astimezone(timezone(timedelta(hours=8)))
timenow = dt8.strftime("%Y-%m-%d %H:%M:%S")

def prepare_record(msg):
    text_list = msg.split('\n')   

    record_list = []

    for i in text_list[1:]:
        temp_list = i.split(" ")

        userid   = temp_list[0]

        record = (userid, str(datetime.strptime(timenow, "%Y-%m-%d %H:%M:%S")))
        record_list.append(record)
        
    return record_list

#插入資料
def insert_record(record_list):
    DATABASE_URL = os.environ["DATABASE_URL"]
    
    conn   = psycopg2.connect(DATABASE_URL, sslmode="require")
    cursor = conn.cursor()

    table_columns = "(userid, time)"
    postgres_insert_query = f"""INSERT INTO test_table {table_columns} VALUES (%s,%s)"""

    try:
        cursor.executemany(postgres_insert_query, record_list)
    except:
        cursor.execute(postgres_insert_query, record_list)
    
    conn.commit()

    # 要回傳的文字
    message = f"{cursor.rowcount}筆資料成功匯入資料庫囉"

    cursor.close()
    conn.close()

    return message

#查詢資料
def select_record():
    DATABASE_URL = os.environ["DATABASE_URL"]

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    postgres_select_query = f"""SELECT * FROM test_table ORDER BY id"""

    cursor.execute(postgres_select_query)
    record = str(cursor.fetchall())

    content = ""
    record = record.split("),")

    for number, r in enumerate(record):
        content += f"第{number+1}筆資料\n{r}\n"

    cursor.close()
    conn.close()

    return content