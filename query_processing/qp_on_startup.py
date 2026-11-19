from sentence_transformers import SentenceTransformer
from data_collection.data_dump import DataBase


def proceed_unencoded():
    db = DataBase()
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    records = db.unencoded()
    if not records or records == []:
        print('all vectors filled')
        db.closeconn()
        return
    sentences = [(model.encode(i[1]).tolist(), i[0]) for i in records]
    querry = ("UPDATE question SET embedding = ? WHERE ID = ?;")
    db.updateOne(query=querry, value=sentences)
    db.closeconn()