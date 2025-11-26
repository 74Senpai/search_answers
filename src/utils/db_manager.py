import sqlite3
from config import db_path

class DBManager:
    def __init__(self, db_path=db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.initialized = False

    def close_conn(self):
        if self.cursor:
            self.cursor.close()
        self.cursor = None
        if self.conn:
            self.conn.close()

    def restart_conn(self):
        self.cursor = self.conn.cursor()

    def _is_table_exists(self, table_name):
        self.cursor.execute("""
            SELECT name 
            FROM sqlite_master 
            WHERE type='table' AND name=?;
        """, (table_name,))
        return self.cursor.fetchone() is not None

    def init_tables(self):
        if not self._is_table_exists("documents"):
            self.cursor.execute("""
                CREATE TABLE documents (
                    id_document INTEGER PRIMARY KEY AUTOINCREMENT,
                    name_document VARCHAR(255) NOT NULL UNIQUE
                );
            """)

        if not self._is_table_exists("chunks_data"):
            self.cursor.execute("""
                CREATE TABLE chunks_data (
                    id_chunk INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_document INTEGER,
                    page INTEGER NOT NULL,
                    texts TEXT NOT NULL,
                    FOREIGN KEY(id_document) REFERENCES documents(id_document)
                );
            """)

        if not self._is_table_exists("chunks_vectors"):
            self.cursor.execute("""
                CREATE TABLE chunks_vectors (
                    id_vector INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_chunk INTEGER UNIQUE,
                    vector TEXT NOT NULL,
                    FOREIGN KEY(id_chunk) REFERENCES chunks_data(id_chunk)
                );
            """)

        self.conn.commit()
        self.initialized = True

    def insert_document(self, name_document:str):
        if not self.initialized:
            print("Please call init_tables() before inserting records.")
            return None
        insert_doc_query = """
            INSERT INTO documents (name_document)
            VALUES (?);
        """

        self.cursor.execute(insert_doc_query, (name_document,))
        new_doc_id = self.cursor.lastrowid
        if not new_doc_id:
            raise Exception("Không thể tạo được tham chiếu cho tài liệu")
        
        return new_doc_id


    def insert_chunk(self, id_doc:int, page, texts, embedding_vectors):
        if not self.initialized:
            print("Please call init_tables() before inserting records.")
            return None
        
        insert_chunk_query = """
            INSERT INTO chunks_data (id_document, page, texts)
            VALUES (?, ?, ?);
        """
        self.cursor.execute(insert_chunk_query, (id_doc, page, texts))
        
        new_chunk_id = self.cursor.lastrowid

        insert_vector_query = """
            INSERT INTO chunks_vectors (id_chunk, vector)
            VALUES (?, ?);
        """
        self.cursor.execute(insert_vector_query, (new_chunk_id, embedding_vectors))

        self.conn.commit()
        return new_chunk_id
    
    def fetch_batch(self, last_id=0, limit=500):
        self.cursor.execute(
            "SELECT id_vector, id_chunk, vector FROM chunks_vectors "
            "WHERE id_vector > ? ORDER BY id_vector LIMIT ?",
            (last_id, limit)
        )
        return self.cursor.fetchall()
    
    def find_chunk_text(self, id_chunk):
        query_chunks_text = """
            SELECT
                documents.name_document,
                chunks_data.page,
                chunks_data.texts
            FROM chunks_data 
            INNER JOIN documents ON documents.id_document = chunks_data.id_document
            WHERE id_chunk = ?
        """
        self.cursor.execute(query_chunks_text, (id_chunk,))

        return self.cursor.fetchone()

    def cleanup_db(self):
        self.cursor.execute("DROP TABLE IF EXISTS chunks_vectors;")
        self.cursor.execute("DROP TABLE IF EXISTS chunks_data;")
        self.cursor.execute("DROP TABLE IF EXISTS documents;")
