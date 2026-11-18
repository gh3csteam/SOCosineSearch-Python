from data_collection.data_dump import DataBase
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss


class Search:
    def __init__(self):
        self.dimensions = 384
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    
    def loadDB(self):
        db = DataBase()
        cur = db.cur
        print("loading database")
        embbedings = cur.execute("SELECT id, url, embedding FROM question WHERE is_answered").fetchall()

        db_mappings= [{"db_id": row[0], "db_url": row[1]} for row in embbedings]

        raw_embeddings = [row[2] for row in embbedings]
        np_emb = np.array(raw_embeddings).astype("float32")
        np_emb = np_emb.reshape(-1, 384)
        faiss.normalize_L2(np_emb)

        dimensions = 384
        index = faiss.IndexFlatIP(dimensions)
        index.add(np_emb)
        return [index, db_mappings]

    def search(self, user_search):
        index, db_mappings = self.loadDB()
        model = self.model
        q_emb = np.array(model.encode(user_search)).astype("float32")
        q_emb = q_emb.reshape(-1, 384)
        faiss.normalize_L2(q_emb)

        D, I = index.search(q_emb, k=5)
        
        for score, axis in zip(D, I[0]):
            if axis.any() == -1:
                continue  
            
            matched_data = db_mappings[axis]
            return matched_data
        