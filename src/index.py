from sentence_transformers import SentenceTransformer
from utils.db_manager import DBManager 
import argparse
import json
import config

CHUNK_SIZE = config.chunk_size
CHUNK_OVERLAY = config.chunk_overlay


print("Nạp model trích xuất đặc trưng văn bản...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Nạp model trích xuất đặc trưng văn bản thành công.")
print("Kết nối tới cơ sở dữ liệu ...")
db_mn = DBManager()
print("Kết nối tới cơ sở dữ liệu thành công")
db_mn.init_tables()

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
            size=CHUNK_SIZE,
            befor_chunk_txt=befor_chunk_txt,
            overlap_ratio=CHUNK_OVERLAY
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
    from utils.data_processing import answer_questions, cleaning_answers
    res = answer_questions(model=model, questions=questions)
    answers = cleaning_answers(res.text)
    for answer in answers:
        print(
            f"Câu hỏi : {answer['question']}\n"
            f"Các lựa chọn : {answer['list-choice']}\n"
            f"Bot-chọn : {answer['last-choice']}\n"
            f"Bot lập luận : {answer['bot-answer']}\n"
            f"Trích dẫn:\n"
        )
        for chunk in answer["quote-from"]:
            print(f"Trang : {chunk['page']}")
            print(f"Trích đoạn : {chunk['texts']}\n")





