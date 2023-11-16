import sqlite3
import os
import datetime
from pathlib import Path


class user_Request():

    def __init__(self):

        self._statement = """
            CREATE TABLE IF NOT EXISTS input_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                input_text TEXT
            )
        """

    def check_set_db(self):
        current_date = datetime.date.today().strftime("%Y-%m-%d")
        path = Path(f"DB/{current_date}")

        if path.is_dir():
            current_path = path / "requests.db"
            return current_path
        else:
            # folder_path = os.path.join("DB", current_date)
            os.makedirs(path, exist_ok=True)
            db_path = os.path.join(path, "requests.db")

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(self._statement)
            conn.commit()

            # conn.close()
            # cursor.close()

            current_path = path/"requests.db"
            return current_path

    def insert_user(self, request):
        request = request[0]

        current_path = self.check_set_db()
        self.data_table = sqlite3.connect(current_path)
        self.cursor = self.data_table.cursor()

        self.cursor.execute("INSERT INTO input_log VALUES (?, ?, ?)",
                            (request["id"], request["timestamp"], request["input_text"]))

        self.data_table.commit()
        print("value inserted")

        self.cursor.close()
        self.data_table.close()


#clients = user_Request()

# data = [{"id" : 2, "timestamp" : "2002-12-12","input_text" : "Hello, This is Sahas" }]

# data2 = [{"id" : 3, "timestamp" : "2002-11-12","input_text" : "ml project : fastapi server" }]

#data3 = [{"id": 4, "timestamp": "2002-11-12",
#          "input_text": "ml project : fastapi server"}]

#data4 = [{"id": 5, "timestamp": "2002-11-12",
#          "input_text": "ml project : fastapi server"}]


#clients.insert_user(data4)
# clients.fetch_table()
