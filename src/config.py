import dotenv
from pydantic import BaseModel, Field
from typing import List, Optional

dotenv.load_dotenv()

# Cấu hình cơ sở dữ liệu
db_path = r"Z:\my_tools\search_answers\data\docs_data.db"

# Cấu hình xử lý, lưu dữ liệu
## Kích thước mỗi đoạn văn bản
chunk_size = 250
## Tỉ lệ trùng lặp nội dung (0 -> 1)
chunk_overlay = 0.3
## Số lượng dữ liệu xử lý mỗi lần
chunk_data_process_batch = 500
## Số lượng văn bản liên quan 
top_k = 10
## Số lượng câu hỏi tối đa mỗi batch
question_batch_limit = 20
## Output excel path
exl_path = r"Z:\my_tools\search_answers\output\answers_output.xlsx"


# Cấu hình làm việc với Gemini
gemini_model = "gemini-2.5-flash"
rate_limit_per_minute = 10
rate_limit_per_day = 250
token_limit_per_minute = 250000

thinking_budget = 1024

# Gen by Gemini
system_introduct = """
### VAI TRÒ
Bạn là một trợ lý AI chuyên nhiệm vụ "Hỏi - Đáp dựa trên dữ liệu thực".

### NHIỆM VỤ
Phân tích danh sách văn bản (`chunks-top-k`) để trả lời **danh sách các câu hỏi** (`questions`) trong `INPUT`.

### QUY TẮC BẮT BUỘC
1. **Dữ liệu:** Chỉ dùng thông tin từ `chunks-top-k`. Không bịa đặt.
2. **Output:** Trả về định dạng JSON khớp với schema `AnswerResponse`.
3. **Số lượng:** Input có bao nhiêu câu hỏi thì Output phải có bấy nhiêu câu trả lời.
4. **Trích dẫn:** Nếu không tìm thấy thông tin, `bot_answer` là "Không đủ dữ kiện" và `quote_from` để rỗng [].
5. **Trắc nghiệm:** Nếu câu hỏi có các lựa chọn (A, B, C...), hãy tách chúng vào list_choice và xác định đáp án đúng nhất cho last_choice`.'

### VÍ DỤ MINH HỌA (BATCH PROCESSING)

**Input:**
[
    {
      "question":  "Câu hỏi 1: Nguyên nhân sự kiện X?",
      "chunks-top-k": [
        {"name_document": "Doc A", "page": 1, "texts": "Nguyên nhân X là lỗi phần mềm."}
      ]
    },
    {
      "question":  "Câu hỏi 2: Hậu quả sự kiện X là gì?",
      "chunks-top-k": [
          {"name_document": "Doc B", "page": 2, "texts": "Hậu quả X là mất kết nối."}
        ]
    }
]

**Output:**
{
  "results": [
      {
        "question": "Câu hỏi 1: Nguyên nhân sự kiện X?",
        "list_choice": [],
        "bot_answer": "Nguyên nhân là do lỗi phần mềm.",
        "last_choice": "Lỗi phần mềm",
        "quote_from": [
            { "name_document": "Doc A", "page": 1, "texts": "Nguyên nhân X là lỗi phần mềm." }
        ]
      },
      {
        "question": "Câu hỏi 2: Hậu quả sự kiện X là gì?",
        "list_choice": [],
        "bot_answer": "Hậu quả là mất kết nối.",
        "last_choice": "Mất kết nối",
        "quote_from": [
            { "name_document": "Doc B", "page": 2, "texts": "Hậu quả X là mất kết nối." }
        ]
      }
  ]
}
"""

class Quote(BaseModel):
  name_document: str = Field(description="Tên tài liệu trích dẫn")
  page: int = Field(description="Trang trích dẫn")
  texts: str = Field(description="Nội dung đoạn trích dẫn")

class Answer(BaseModel):
  question: str = Field(description="Câu hỏi")
  list_choice: List[str] = Field(description="Danh sách các câu trả lời của câu hỏi")
  bot_answer: str = Field(description="Câu trả lời của model")
  last_choice: str = Field(description="Lựa chọn cuối cùng của model")
  quote_from: List[Quote]
     
class AnswerResponse(BaseModel):
  results: List[Answer] = Field(description="Danh sách các câu trả lời tương ứng với các câu hỏi đầu vào")