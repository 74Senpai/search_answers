from sentence_transformers import SentenceTransformer
from utils.db_manager import DBManager 
import argparse

print("Nạp model trích xuất đặc trưng văn bản...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Nạp model trích xuất đặc trưng văn bản thành công.")
print("Kết nối tới cơ sở dữ liệu ...")
db_mn = DBManager()
print("Kết nối tới cơ sở dữ liệu thành công")
db_mn.init_tables()

# from utils.input_processing import parse_chunks_data
# chunks_vectors_batch = db_mn.fetch_batch(0, 2)
# data = parse_chunks_data(chunks_vectors_batch)
# print(f"id_vector: {data[1]['id_vector']} ")

parser = argparse.ArgumentParser(
    description="Tool quản lý documents và tìm câu trả lời từ document có sẵn"
)

parser.add_argument(
    "--file-path",
    type=str,
    help="Đường dẫn tới file nếu muốn sử dụng file"
)

# Loại hành động
parser.add_argument(
    "--type-action",
    type=str,
    required=True,
    choices=["add-document", "cleanup-db", "search-file", "search-single"],
    help=(
        "Loại hành động bạn muốn thực hiện:\n"
        "  add-document   : Lưu document mới vào database\n"
        "  cleanup-db     : Xóa toàn bộ database\n"
        "  search-file    : Tìm câu trả lời từ file\n"
        "  search-single  : Tìm câu trả lời riêng lẻ từ input questions"
    )
)

parser.add_argument(
    "--questions",
    type=str,
    nargs="+",
    help="Danh sách câu hỏi (dùng cho search-single)"
)

args = parser.parse_args()

if args.type_action == "add-document":
    from pypdf import PdfReader
    from utils import data_processing as ips
    import json

    if not args.file_path:
        raise ValueError("Bạn cần cung cấp --file-path để thêm document")

    reader = PdfReader(args.file_path)
    doc_len = len(reader.pages)
    befor_chunk_txt = ""

    for i in range(doc_len):
        page = reader.pages[i]
        page_num = page.page_number + 1
        texts = page.extract_text()

        page_chunks = ips.get_texts_chunks(
            texts=texts,
            size=250,
            befor_chunk_txt=befor_chunk_txt,
            overlap_ratio=0.3
        )
        befor_chunk_txt = page_chunks[-1] if page_chunks else ""

        for chunk_i, chunk in enumerate(page_chunks):
            embedding = model.encode(chunk)
            embedding_str = json.dumps(embedding.tolist()) 
            if embedding.shape[0] == 0:
                print(f"Page {page_num} | Chunk {chunk_i}: Embedding failed !!!")
            else:
                print(f"Page {page_num} | Chunk {chunk_i}: Embedding successful")
                print("Insert chunk to database ...")
                db_mn.insert_chunk(page=page_num, texts=chunk, embedding_vectors=embedding_str)

            print(chunk[:20])

elif args.type_action == "cleanup-db":
    confirm = input("Bạn có chắc muốn xóa toàn bộ database? (y/n): ").strip().lower()
    if confirm == "y":
        db_mn.cleanup_db()
        print("Database đã được xóa.")
    else:
        print("Hủy thao tác xóa database.")

elif args.type_action == "search-single":
    questions = args.questions
    if not questions:
        print("Bạn cần thêm câu hỏi để tiến hành tìm câu trả lời.")
        exit()

    from utils.data_processing import parse_chunks_data, find_top_k_chunk, generate_input_for_ai
    from utils.ai_analysis import search_answer

    top_chunks = {f"question-{i}": [] for i in range(len(questions))}

    last_id = 0
    chunks_vectors_batch = db_mn.fetch_batch(last_id, 500)

    while chunks_vectors_batch:
        print(f"Process batch start by {last_id}")
        chunks_vectors = parse_chunks_data(chunks_vectors_batch)

        for i, question in enumerate(questions):

            merged_vectors = chunks_vectors.copy()
            if top_chunks[f"question-{i}"]:
                merged_vectors.extend(top_chunks[f"question-{i}"])

            input_vector = model.encode(question)

            top_k_batch = find_top_k_chunk(
                model=model,
                input_vector=input_vector,
                chunks_data=merged_vectors,
                top_k=5
            )

            top_chunks[f"question-{i}"] = top_k_batch

        last_id = chunks_vectors[-1]["id_vector"]
        chunks_vectors_batch = db_mn.fetch_batch(last_id, 500)

    res = search_answer(generate_input_for_ai(questions=questions, top_k_chunk=top_chunks))
    print(res.text)



