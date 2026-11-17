import dotenv
import os
import httpx
import json
import duckdb
#https://api.stackexchange.com/2.3/questions?pagesize=100&order=desc&sort=activity&site=stackoverflow

dotenv.load_dotenv()
API_KEY = os.getenv("API_KEY")

class DataBase:
    def __init__(self):
        self.conn = duckdb.connect("database.db")
        self.cur = self.conn.cursor()
        self.initDb()

    def initDb(self):
        self.cur.execute("CREATE SEQUENCE IF NOT EXISTS seq_id START 1;")

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS question (
            id INTEGER PRIMARY KEY DEFAULT nextval('seq_id'), 
            title TEXT, 
            url TEXT, 
            is_answered BOOLEAN, 
            embedding DOUBLE
        )
        """)

    def closeconn(self):
        self.cur.close()
        self.conn.close()

    def fill_many(self, query, values):
        self.cur.executemany(query=query, parameters=values)
        self.conn.commit()

    def updateOne(self, query, value):
        self.cur.executemany(query, value)
        self.conn.commit()


    def unencoded(self) -> list[tuple]:
        try:
            unencoded_sentences = self.cur.execute("SELECT * FROM question WHERE embedding IS NULL").fetchall()
            return unencoded_sentences
        except duckdb.CatalogException as e:
            print(f"table does not exist{e}")
            return []


class SODumpClient:
    def __init__(self, url:str = "https://api.stackexchange.com/2.3/", key:str =API_KEY):
        self.client = httpx.Client(base_url=url)
        self.key = key

    def get_questions(self, params: str):


        r = self.client.get(f"questions?{params}&key={self.key}")
        questions = [
    {
        "title": item.get("title"),
        "url": item.get("link"),
        "answered": item.get("is_answered"),
    }
    for item in r.json()["items"]
]
        return questions

    def FillDB(self, params, db: DataBase):
        questions = self.get_questions(params=params)
        values = [(q["title"], q["url"], q["answered"]) for q in questions]

        querry = (f"INSERT INTO question (title, url, is_answered) VALUES (?, ?, ?)")
        db.fill_many(query=querry, values=values)

    def closeClient(self):
        self.client.close()
        

db = DataBase()
so_dump = SODumpClient()

def fill(iter: int = 100):
    n = 0 
    while(n< iter):
        n+=1
        print(n)
        so_dump.FillDB(params="pagesize=100&order=desc&sort=activity&site=stackoverflow", db=db)
        if(n>100):
            break
    db.closeconn()
    so_dump.closeClient()

