import sqlite3

class Clients():

    def __init__(self, table):
        self.db_name = table
        self.data_table = sqlite3.connect(self.db_name)
        self.cursor = self.data_table.cursor()

        create_table_query = """
                CREATE TABLE IF NOT EXISTS users (
                    Keys TEXT PRIMARY KEY,
                    Name TEXT,
                    Ip_address TEXT,
                    Usage INTEGER
                )
                """
        self.cursor.execute(create_table_query) 
        self.data_table.commit()
        self.cursor.close()
        self.data_table.close()



    def insert_user(self, request):
        request = request[0]
        self.data_table = sqlite3.connect(self.db_name)
        self.cursor = self.data_table.cursor()

        self.cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (request["Keys"], request["Name"], request["ip_address"], 1))
        print("value inserted")
        self.data_table.commit()
      
        self.cursor.close()
        self.data_table.close()
        

    def update_usage(self, request):
        request = request[0]
        self.data_table = sqlite3.connect(self.db_name)
        self.cursor = self.data_table.cursor()

        self.cursor.execute("UPDATE users SET Usage = Usage + 1 WHERE Keys = ?", (request["Keys"],))        
        self.data_table.commit()

        self.cursor.close()
        self.data_table.close()
    

        


    def fetch_table(self):
        self.data_table = sqlite3.connect(self.db_name)
        self.cursor = self.data_table.cursor()

        self.cursor.execute("SELECT * FROM users")
        print(self.cursor.fetchall())

        self.cursor.close()
        self.data_table.close()


