# Công cụ hỗ trợ tìm kiếm câu trả lời từ tài liệu
---

## Mô tả.
Đây là công cụ được tạo ra nhằm hỗ trợ trả lời các câu hỏi lý thuyết đơn giản.
Sử dụng khả năng suy luận của Model AI Gemini để hỗ trợ tìm đáp án dựa trên tài liệu
được người dùng đưa vào cơ sở dữ liệu.
Về mặt lý thuyết, chỉ cần câu hỏi hợp lệ về mặt ngữ nghĩa và có trong cơ sở dữ liệu, 
công cụ có thể hỗ trợ tìm ra đáp án dựa trên những đoạn văn bản có sự tương đồng về mặt 
ngữ nghĩa nhất với câu hỏi. 

### Điểm khác biệt.
- Điểm đặc biệt của công cụ là chỉ cho phép suy luận và trả lời dựa trên tài liệu được đưa vào,
hạn chế tối đa việc tự động thêm, tạo, dự đoán thông tin khi không tìm thấy thông tin tin cậy như
các Model AI phổ biến.
- Có nguồn trích dẫn giới hạn ở vị trí của trang và đoạn trích dẫn văn bản ngắn.

### Hạn chế.
- Sự chính xác và cấu trúc của tài liệu đưa vào có thể chưa chuẩn đối với các
dữ liệu liên quan tới bảng, các công thức toán học, hình học đặc biệt, dữ liệu hình ảnh.
- Độ chính xác với các câu hỏi có dữ liệu bị khiếm khuyết trong quá trình thêm vào cơ sở dữ liệu
là chưa cao.
- Còn khó khăn trong các câu hỏi đòi hỏi phân tích cao, có tập dữ liệu trải dài xuyên suốt tài liệu

### Công cụ hỗ trợ
1. Gemini AI API.
- `Gemini AI` là một mô hình trí tuệ nhân tạo của google, đặc biệt với phiển bản từ 2.5 trở lên,
khả năng suy luận được thêm vào với các tùy chọn và đặc biệt là API miễn phí là lý do `Gemini` được 
đưa bào sử dụng trong dự án này. Vài trò của `Gemini` là dựa trên các văn bản đưa vào tiến hành suy luận
và trả về dữ liệu mong đợi theo định dạng có sẵn.
    + Tài liệu tham khảo : https://ai.google.dev/gemini-api/docs/

2. Sentence transformer.
- `sentence_transformer` là một mô hình trích xuất đặc trưng của văn bản(text embedding) thành một mảng
`vectors` với các hàm tiện ích hỗ trợ cho việc so sánh độ tương đồng giữ 2 đoạn văn bản. Trong dự án
`sentence_transformer` chính thành phần quan trọng nhất giúp tìm ra các đoạn văn bản có độ tương đồng cao 
nhất với câu hỏi đưa vào để hệ thống có thể tạo yêu cầu cho `Gemini` phân tích.
- `sentence_transformer` giúp giảm tải công việc của `Gemini` đáng kể so với trước tuy nhiên đánh đổi lại là hiệu năng khi khởi chạy cũng như dung lượng dành cho Model là khá lơn tuy nhiên sơ với việc tiêu tốn 
`token` và `rate limit` là có lợi hơn.
    + Tài liệu tham khảo : https://www.sbert.net/docs/sentence_transformer/usage/usage.html

3. pypdf.
- `pypdf` là thư viện hỗ trợ thao tác với tài liệu định dạng `PDF`, đa số tài liệu, giáo trình 
hiện nay đều sử dụng định dạng này. Thư viện hỗ trợ trích xuất văn bản từ tài liệu, đây là bộ phận 
`data entrys` của hệ thống này.
    + Tài liệu tham khảo : https://www.geeksforgeeks.org/python/working-with-pdf-files-in-python/

4. SQLite.
- `SQLite` là cơ sở dữ liệu được chọn lần này, điểm nổi bật của `SQLite` trong dự án này là sự đơn 
giản và người dùng có thể kiểm soát hoàn toàn dữ liệu của mình.
    + Tài liệu tham khảo : https://sqlite.org/quickstart.html

5. Pandas
- `Pandas` là một thư viện xử lý dữ liệu mạnh mẽ. Trong dự án, `pandas` hỗ trợ trích xuất các câu hỏi có cấu
trúc từ tài liệu excel cũng như hỗ trợ tạo và lưu kết quả xử lý vào file excel.
    + Tài liệu tham khảo : https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html

*Ngoài ra, hệ thống còn sự dụng một số thư viện có sẵn để hỗ trợ thao tác trên giao diện dòng lệnh
cũng như một số công việc khác*

### Hướng dẫn cài đặt.
#### ***Yêu cầu***
+ ***Nền tảng : windows, linux, macos***
+ ***Đã cài đặt `python`***
+ ***Có tối thiểu 1.1GB bộ nhớ còn trống***

#### Các bước cài đặt và sử dụng
1. Tải thư mục dự án bằng `git` hoặc tải file nén của dự án xuống.
- Đối với `git`
  ```bash
    git clone https://github.com/74Senpai/search_answers.git
    ```
- Hoặc truy cập https://github.com/74Senpai/search_answers để lấy file nén của dự án

2. Ở thư mục gốc của dự án mở giao diện dòng lệnh và tiến hành cài đặt các thư viện cần thiết.
```bash
pip install -r requirements.txt
```
> [!TIP]
> Nên tạo thư mục venv để tránh xung đột thư viện

3. Tạo têp `.env` ở thư mục gốc dự án và truyền `GEMINI_API_KEY` của bạn vào.
***Nếu chưa có `GEMINI_API_KEY` xem lại các công cụ hỗ trợ và truy cập tài liệu hướng dẫn của Google.`***

4. Tiến hành cấu hình các đường dẫn và các thông tin cần thiết ở `config.py`
5. Tiến hành trích xuất và lưu tài liệu vào cơ sở dữ liệu bằng dòng lệnh.
***Đảm bảo bạn ở thư mục gốc của dự án***
```bash
python src/index.py --type-action=add-document --file-path=duong-dan-toi-file-tai-lieu
```
6. Tiến hành tìm đáp án bằng giao diện dòng lệnh.
- Tìm bằng câu hỏi trực tiếp
```bash
python src\index.py --type-action=search-single --questions "Câu hỏi 1" "Câu hỏi 2"
```
***Lưu ý:*** có thể hỏi nhiều câu cùng lúc nhưng phải đảm bảo mỗi câu được bọc trong cặp 
dấu nháy kép `" "` và mỗi câu cách nhau một khoảng trắng.

- Tìm bằng file excel câu hỏi
```bash
python src\index.py --type-action=search-file --file-path=duong-dan-toi-file-cau-hoi
```
***Lưu ý:*** file câu hỏi phải là file excel và có cấu trúc câu hỏi theo hàng rõ ràng, hợp lệ,
tên file nên để không dấu không khoảng trắng.
- Tìm hiểu thêm các tùy chọn
```bash
python src\index.py --help
```

### Hướng phát triển.
***Dự án đang trong quá trình phát triển phiên bản tiếp theo, để tăng nhanh tiến độ, vui lòng liên hệ tôi.***
Dự án có thể phát triển theo 2 hướng chính và một hướng mở rộng:
1.Phát triển theo hướng cá nhân hóa.
- Phát triển để lưu trữ cho tất cả tài liệu, kiến thức, thông tin của người dùng đưa vào, xem hệ thống như một công cụ lưu trữ thông minh, trả lời nhanh các thông tin người dùng đưa vào trước đó và truy xuất nguồn gốc.

2. Phát triển theo hướng cộng đồng.
- Triển khai backe-end tập trung dữ liệu của một cộng đồng nhất định, tổng hợp kiến thức, thông tin có trong cộng đồng,
  chia sẻ thông tin giữa những người trong cộng đồng.

3. Phát triển hệ thống tạo câu hỏi dựa trên tài liệu đưa vào.
- Tiến hành tạo câu hỏi dựa trên văn bản đưa vào để hỗ trợ trong việc học tập và hệ thống hóa kiến thức. Tuy nhiên, thách thức về độ tin cậy của câu hỏi cũng như câu trả lời, độ hữu ích của câu hỏi và việc tạo câu hỏi liên quan tới hệ thống kiến thức sâu rộng là một thách thức cực lớn.
  
Lưu ý chung:
- Cả 3 cách tiếp cận trên đều yêu cầu hiệ thống hiện tại phát triển thân thiện hơn về UI-UX, đa dạng dữ liệu I/O
cơ chế truy xuất nguồn gốc và cơ sở dữ liệu quan hệ rộng hơn. cũng như triển khai API để tốc độ khởi động cũng như dung lượng giảm xuống thấp nhất.
Cũng như một model có hiệu năng và giới hạn tốt hơn.


> [!NOTE]
> Đối với `Gemini` miễn phí, cần hạn chế các câu hỏi và nội dung không liên quan để giảm tiêu tốn tài nguyên giới hạn.
> Cần chú ý `rate limit` và `token` tránh phát sinh các chi phí không cần thiết.

> [!WARNING]
> Công cụ chỉ hỗ trợ lựa chọn đáp án cho là đúng nhất dựa theo dữ liệu.
> Cần có tư duy phản biện và kiểm chứng lại câu trả lời.
> Không để lộ các thông tin trong file `.env`.

> [!CAUTION]
> Mọi lỗi liên quan tới logic nghiệp vụ vui lòng phản hồi hoặc tạo `git issues` để được khắc phục sớm nhất.
