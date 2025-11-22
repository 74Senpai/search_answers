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

*Ngoài ra, hệ thống còn sự dụng một số thư viện có sẵn để hỗ trợ thao tác trên giao diện dòng lệnh
cũng như một số công việc khác*

