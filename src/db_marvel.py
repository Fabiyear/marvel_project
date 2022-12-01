import os
import logging
import mysql.connector
from sqlalchemy import create_engine
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class DbMarvel:
    def __init__(self):
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.host = os.getenv('DB_HOST')
        self.mydb = mysql.connector.connect(user=self.user, password=self.password, host=self.host, port="3306", database='dbmrv')

    def status_table(self, table, total_items):
        try:
            query = f"SELECT * FROM {table} ORDER BY ID_SEQ DESC LIMIT 1"
            cur = self.mydb.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            self.mydb.commit()
            logging.info(f"table {table} already exists, checking all of the values [...]")
            try:
                tup = [row[0] for row in rows], \
                      [row[4] for row in rows], \
                      [row[5] for row in rows]
                list_vlue = [', '.join(map(str, x)) for x in tup]

                id_seq = int(list_vlue[0])
                offset = int(list_vlue[1])
                index = int(list_vlue[2])

                db_total = offset + index

                if total_items <= db_total + 1:
                    load_parameters = ("OK")
                else:
                    if index == 99:
                        index = 0
                        offset = offset + 100
                    else:
                        index = index + 1
                    offset = offset
                    id_seq = id_seq + 1
                    logging.info(f"process restarting to {table}: id_seq: {id_seq} offset: {offset} index: {index}")
                    load_parameters = ("NOK", id_seq, offset, index)
            except:
                logging.info(f"empty table {table}, starting proccess to load")
                id_seq = 1
                offset = 0
                index = 0

                load_parameters = ("NOK", id_seq, offset, index)
        except:
            logging.info(f"table {table} not found, starting process to create table...")
            id_seq = 1
            offset = 0
            index = 0
            load_parameters = ("START", id_seq, offset, index)


        return load_parameters

    def create_table(self, type):
        try:

            mysql_create_query = f"CREATE TABLE {type} (id_seq INT, name VARCHAR(255), id_marvel INT, type VARCHAR(40), offset_1 INT, index_1 INT)"

            cursor = self.mydb.cursor()
            cursor.execute(mysql_create_query)
            self.mydb.commit()
            logging.info(f"table {type} created successfully")
            cursor.close()
        except mysql.connector.Error as error:
            logging.error("failed to create table {}".format(error))

        return None

    def insert_table(self, id_seq, name, id_marvel, type, offset, index):
        df = pd.DataFrame([[id_seq, name, id_marvel, type, offset, index]], columns=['id_seq', 'name', 'id_marvel', 'type', 'offset_1', 'index_1'])
        engine = create_engine(f"mysql://{self.user}:{self.password}@{self.mydb._host}/{self.mydb.database}")
        #total_df = df[df.columns[0]].count()
        try:
            write = df.to_sql(name=type, con=engine, if_exists='append', index=False)
            logging.info(f"insert row successfully into {type} table")
        except:
            logging.error(f"failed to insert into {type} table")


        return write
    def insert_table_obt(self, type):
        mysql_insert_query = f"INSERT INTO one_big_table (id, name, type) SELECT id_marvel, name, type FROM {type}"
        cursor = self.mydb.cursor()
        cursor.execute(mysql_insert_query)
        self.mydb.commit()
        cursor.close()
        return cursor