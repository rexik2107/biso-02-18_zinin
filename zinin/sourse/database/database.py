import sqlite3
import traceback
import random

from log import logger

class date_base:

    def __init__(self, db_name):
        self.db_name = db_name

    def checkTableExists(self, tb_name):
        try:
            sqlite_connection = sqlite3.connect(str(self.db_name))
            cursor = sqlite_connection.cursor()
            cursor.execute("""
                select count(*) from '{0}'
                """.format(tb_name.replace('\'', '\'\'')))
            cursor.close()
            return True
        except Exception:
            print("Ошибка при работе с sqlite: ", traceback.format_exc())
            cursor.close()
            return False



    def create_users(self):
        if not self.checkTableExists("users"):
            try:
                sqlite_connection = sqlite3.connect(str(self.db_name))
                sqlite_create_table_query = '''CREATE TABLE users
                (
                    id integer PRIMARY KEY,
                    username VARCHAR(20),
                    password VARCHAR(32),
                    admin INTEGER 
                );'''
                cursor = sqlite_connection.cursor()
                cursor.execute(sqlite_create_table_query)
                sqlite_connection.commit()
                cursor.close()


            except Exception:
                print("Ошибка при работе с sqlite: ", traceback.format_exc())
                if sqlite_connection:
                    sqlite_connection.close()

    def insert_users(self, username, password, admin=0):
        if not self.checkTableExists("users"):
            self.create_users()
        try:
            if not self.check_users(username):
                sqlite_connection = sqlite3.connect(str(self.db_name))
                cursor = sqlite_connection.cursor()
                cursor.execute("INSERT INTO users(username, password, admin) VALUES(?,?, ?)", (username, password, admin))
                sqlite_connection.commit()
                cursor.close()
                return True
            else:
                return False

        except Exception:
            print("Ошибка при работе с sqlite: ", traceback.format_exc())
            if sqlite_connection:
                sqlite_connection.close()
            return False

    def check_users(self, username):
        if not self.checkTableExists("users"):
            self.create_users()
        try:
            sqlite_connection = sqlite3.connect(str(self.db_name))
            cursor = sqlite_connection.cursor()
            cursor.execute("SELECT id, password FROM users WHERE username = ?", (username,))
            data = cursor.fetchone()
            if data is None:
                return False
            sqlite_connection.commit()
            cursor.close()
            return data
        except Exception:
            print("Ошибка при работе с sqlite: ", traceback.format_exc())
            if sqlite_connection:
                sqlite_connection.close()
            return False

    def check_users_adm(self, username):
        if not self.checkTableExists("users"):
            self.create_users()
        try:
            sqlite_connection = sqlite3.connect(str(self.db_name))
            cursor = sqlite_connection.cursor()
            cursor.execute("SELECT id, admin FROM users WHERE username = ?", (username,))
            data = cursor.fetchone()
            if data is None:
                return False
            sqlite_connection.commit()
            cursor.close()
            return data[1]
        except Exception:
            print("Ошибка при работе с sqlite: ", traceback.format_exc())
            if sqlite_connection:
                sqlite_connection.close()
            return False


class date_base_mongo:

    def __init__(self, client, **kwargs):
        self.mongo_db = kwargs.get("mongo_db")
        self.client = client
        self.db = self.client[self.mongo_db]


    def insert_user(self, username):
        collection = self.db["chats"]
        collection.insert_one({"name": username})

    def get_chats(self):
        collection = self.db["chats"]
        result = collection.find({})
        sl = []
        for i in result:
            # slprint(i)
            sl.append({"name": i["name"], "message": i["message"]})
            #return str(i)
        return sl


    def send_message(self, username, text):
        #self.insert_user(username)
        collection = self.db["chats"]
        collection.insert_one({"name": username, "message": text})
        return






    def insert_users(self, username, password, admin=0):
        collection = self.db["users"]
        ran = random.randint(100, 9999999999)
        result = collection.find_one({"username": username})
        if result is None:
            collection.insert_one({"user_id": ran, "username": username, "password": password, "admin": admin})
            return True
        else:
            collection.insert_one({"user_id": ran, "username": username, "password": password, "admin": admin})
        return True

    def check_users(self, username):
        collection = self.db["users"]
        result = collection.find_one({"username": username})
        if result:
            return result
        return False

    def add_kwargs(self, collection_name, **kwargs):
        collection = self.db[collection_name]
        result = collection.find_one(kwargs)
        if result is None:
            collection.insert_one(kwargs)
            return True
        return False

    def add_files(self, pdf, commercy_proposal_id):
        collection = self.db["pdf_files"]
        result = collection.find_one({"commercy_proposal_id": str(commercy_proposal_id)})
        if result is None:
            collection.insert_one(pdf)
            return True
        return False

    def check_files(self, commercy_proposal_id):
        collection = self.db["pdf_files"]
        result = collection.find_one({"commercy_proposal_id": str(commercy_proposal_id)})
        return result

    def get_files(self):
        collection = self.db["pdf_files"]
        spis = []
        for i in collection.find({}):
            spis.append({"id": i["commercy_proposal_id"], "date_create": i["date_create"]})
        return spis

    def add_document_for_people(self, **kwargs):
        number = kwargs.get("number")
        fio = kwargs.get("fio")
        date_create = kwargs.get("date_create")
        link = kwargs.get("link")

        collection = self.db["document_for_people"]
        result = collection.find_one({"number": str(number)})
        if result is None:
            collection.insert_one({"number": str(number),
                                   "fio": str(fio),
                                   "date_create": date_create,
                                   "link": str(link)})
            return True
        return False


    def count_document_commercy_proposal(self, **kwargs):
        collection = self.db["pdf_files"]
        result = collection.find(kwargs)
        if result:
            result = len(list(result))
            return result
        else:
            return 0

    def count_document_for_people(self, **kwargs):
        collection = self.db["document_for_people"]
        result = collection.find(kwargs)
        result = len(list(result))
        return result

    # создание заказчика
    def add_customer(self, **kwargs):
        collection = self.db["customer"]
        result = collection.find_one({"user_id": kwargs.get("user_id")})
        if result is None:
            collection.insert_one(kwargs)
            return True

        return False

    # создание заказа
    def add_order(self, **kwargs):
        collection = self.db["order"]
        result = collection.find_one({"order_id": kwargs.get("order_id")})
        if result is None:
            collection.insert_one(kwargs)
            return True
        return False

    # получение информации о заказе
    def get_order(self, order_id):
        collection = self.db["order"]
        result = collection.find_one({"order_id": kwargs.get("order_id")})
        if result is not None:
            return result
        return False

    # получение всех заказов
    def get_order_all(self, flag=False):
        collection = self.db["order"]
        result = collection.find({})
        res = []
        for i in result:
            if flag and i["archive"]:
                res.append(i)
            else:
                res.append(i)
        return result






# if __name__ == '__main__':
#     g = database("test4")
#     g.create_users()
    #g.insert_users("admin4", "rtgggbff")
    # print(g.check_users("admin4"))

