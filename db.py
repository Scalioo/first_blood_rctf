import sqlite3 
from typing import Any, Dict, List

class database :
    def __init__(self , db_name: str):
        db = sqlite3.connect(db_name)
        db.execute("CREATE TABLE IF NOT EXISTS first_bloods (id INTEGER PRIMARY KEY AUTOINCREMENT, challenge_id TEXT, challenge_name TEXT , category TEXT , user TEXT)")
        self.db = db

    def fetch_first_bloods_from_db(self)->List[List[Any]]:
        fetched = self.db.execute("SELECT * FROM first_bloods").fetchall()
        bloods = []
        for chall in fetched :
            bloods.append({
                'id': chall[1],
                'name': chall[2],
                'category': chall[3],
                'first_blood': chall[4]
            }
            )
        return bloods

    def add_first_blood_to_db(self,challenge):
        self.db.execute(
                "INSERT INTO first_bloods (challenge_id,challenge_name, category ,user) VALUES (?,?,?, ?)",
                (challenge["id"], challenge["name"], challenge["category"] , challenge["first_blood"])
            )
        self.db.commit()


