from google import genai
from google.genai import types

import dotenv
import json

dotenv.load_dotenv()

input_dict = {
  "question": "Việc chẩn đoán trong các nghiên cứu Dịch tễ học thường là: "
                "A. Xác định một trường hợp mắc bệnh; "
                "B. Xác định một hiện tượng sức khỏe/cộng đồng; "
                "C. Xác định nguyên nhân làm xuất hiện và lan tràn bệnh/cộng đồng; "
                "D. Nghiên cứu một hiện tượng sức khỏe/cộng đồng; "
                "E. Xác định kết quả của chương trình can thiệp. ",
  
  "chunks-top-k": [
    {
      "id_chunk": 1,
      "page": 12,
      "texts": "Dịch tễ học là một ngành khoa học nghiên cứu về sức khỏe và bệnh tật trong cộng đồng với phạm vi rất rộng. Một trong những mục tiêu quan trọng của dịch tễ học là mô tả các mô hình bệnh tật theo thời gian, địa điểm và đối tượng, từ đó xây dựng các giả thuyết khoa học nhằm xác định các yếu tố nguy cơ liên quan. Trong nhiều tình huống nghiên cứu thực tế, các nhà dịch tễ học thường quan tâm đến việc thu thập dữ liệu từ các cá nhân, hộ gia đình và quần thể nhằm đánh giá mức độ mắc bệnh, phân bố bệnh theo tuổi, giới, môi trường sống hoặc hành vi. Tuy nhiên, không phải mọi loại hình nghiên cứu đều hướng đến toàn bộ cộng đồng; có một số nghiên cứu tập trung sâu vào đặc điểm của từng cá nhân, chẳng hạn như nghiên cứu trường hợp – chứng. Do đó, đối tượng nghiên cứu có thể thay đổi tùy theo mục tiêu nghiên cứu cụ thể, nhưng nhìn chung dữ liệu thu thập ban đầu vẫn bắt nguồn từ từng cá nhân riêng lẻ."
    },

    {
      "id_chunk": 2,
      "page": 18,
      "texts": "Đối tượng trung tâm của nghiên cứu dịch tễ học không phải là từng cá nhân riêng lẻ mà là các hiện tượng sức khỏe xảy ra trong quần thể. Dịch tễ học xem cộng đồng là đơn vị nghiên cứu chính, trong đó các hiện tượng như tỷ lệ mắc bệnh, tỷ lệ tử vong, mô hình phân bố bệnh, sự lan truyền của dịch, hoặc các trạng thái sức khỏe khác được theo dõi và phân tích. Việc nghiên cứu các hiện tượng sức khỏe của cộng đồng cho phép các nhà khoa học đưa ra kết luận có ý nghĩa rộng hơn, không bị giới hạn bởi đặc điểm của một cá nhân. Chính vì vậy, trong các giáo trình dịch tễ học hiện đại, khái niệm “hiện tượng sức khỏe/cộng đồng” thường được mô tả là đối tượng nghiên cứu quan trọng nhất, phản ánh cách tiếp cận mang tính quần thể thay vì cá nhân. Nhờ xem cộng đồng là đối tượng chính, dịch tễ học có thể đánh giá xu hướng bệnh tật, tìm ra yếu tố nguy cơ, dự báo dịch và đề xuất biện pháp can thiệp ở quy mô lớn."
    },

    {
      "id_chunk": 3,
      "page": 22,
      "texts": "Trong quá trình nghiên cứu dịch tễ học, các nhà nghiên cứu thường phải thực hiện nhiều bước quan trọng như xác định vấn đề sức khỏe, đưa ra câu hỏi nghiên cứu, lựa chọn thiết kế nghiên cứu phù hợp và phân tích dữ liệu thu thập được. Một trong các bước đó là đánh giá nguyên nhân gây bệnh, chẳng hạn như yếu tố môi trường, vi sinh vật, hành vi, hoặc các điều kiện xã hội – kinh tế. Đánh giá nguyên nhân là phần quan trọng vì nó giúp xác định các tác nhân dẫn đến bệnh và hiểu rõ cơ chế xuất hiện hoặc lan tràn của chúng. Mặc dù vậy, đánh giá nguyên nhân lại không phải là đối tượng nghiên cứu chính mà chỉ là một phần trong quy trình triển khai nghiên cứu. Do đó, khi xây dựng mô hình khoa học hoặc triển khai điều tra, nhà nghiên cứu cần phân biệt rõ giữa ‘đối tượng nghiên cứu’ và ‘mục tiêu phân tích’ để tránh nhầm lẫn khái niệm."
    }
  ]
}


client = genai.Client()

def search_answer(input_data):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config = types.GenerateContentConfig(
        thinking_config = types.ThinkingConfig(thinking_budget=1),
        system_instruction = (
                "Bạn là trợ lý cá nhân của tôi\n"
                "Nhiệm vụ của bạn: nhận câu hỏi và danh sách các đoạn văn bản (chunks-top-k), "
                "sau đó suy luận để đưa ra câu trả lời chính xác nhất dựa trên dữ liệu được cung cấp.\n\n"

                "QUY TẮC BẮT BUỘC:\n"
                "- Chỉ được trả lời dựa trên dữ liệu trong các 'chunks-top-k'.\n"
                "- Không được bịa thông tin, không được tự suy luận vượt quá nội dung trong chunks.\n"
                "- Nếu không có đủ dữ kiện để trả lời, bắt buộc trả về:\n"
                "  bot-answer: 'Không đủ dữ kiện'\n"
                "  last-choice: 'Không đủ dữ kiện'"
                "  quote-from: []\n\n"

                "CẤU TRÚC INPUT:\n"
                "- question: nội dung câu hỏi.\n"
                "- chunks-top-k: danh sách các đoạn văn bản chứa:\n"
                "    id_chunk (int), page (int), texts (string).\n\n"

                "CẤU TRÚC OUTPUT (JSON):\n"
                "{\n"
                "  'question': lặp lại câu hỏi đầu vào,\n"
                "  'list-choice': Tự lập danh sách lựa chọn của câu hỏi đưa vào nếu có\n"
                "  'bot-answer': câu trả lời của bạn nếu có (hoặc 'Không đủ dữ kiện'),\n"
                "  'last-choice': câu trả lời cuối cùng của bạn theo A, B, C, D hoặc văn bản "
                " nếu có (hoặc 'Không đủ dữ kiện'), \n"
                "  'quote-from': danh sách các trích dẫn liên quan trực tiếp.\n" \
                "gồm 'id_chunk', 'page', 'texts'"
                "}\n\n"

                "LƯU Ý:\n"
                "- Chỉ trích dẫn những câu, đoạn văn bản có liên quan trực tiếp vào 'texts'.\n"
                "- Không tự thêm trích dẫn ngoài dữ liệu.\n"
            )
        ),
        contents=json.dumps(input_data, ensure_ascii=False),
    )

    return response

# print(response.text)