# ✈️ TravelBuddy - AI Travel Agent

**TravelBuddy** là một ứng dụng Trợ lý Du lịch Thông minh (AI Agent) hoạt động trên Terminal, được xây dựng bằng kiến trúc **LangGraph** và sức mạnh xử lý ngôn ngữ mô hình **Gemini-2.5-Flash** (Google GenAI). 

Hệ thống có khả năng tương tác tự nhiên với người dùng bằng tiếng Việt, thiết lập đồ thị trạng thái có bộ nhớ (Memory Checkpointer) và có quyền gọi nhiều chức năng nghiệp vụ (Tools) như tra cứu, phân tích tài chính và quản lý trọn gói quy trình đặt vé.

---

## 🌟 Chức Năng Chính

TravelBuddy sở hữu bộ 6 Công cụ (Tools) mạnh mẽ bao gồm:
1. **Tìm kiếm chuyến bay (`search_flights`)**: Tra cứu lịch trình, giờ bay, giá tiền, số ghế trống dựa trên DataBase.
2. **Tìm kiếm khách sạn (`search_hotels`)**: Tra cứu chỗ ở theo mức giá tối đa, lọc theo sao và tự động xếp hạng rating.
3. **Quản lý ngân sách (`calculate_budget`)**: Tự động tính toán chi ly sổ sách, kiểm tra độ rủi ro thâm hụt tiền túi của khách hàng.
4. **Kiểm tra hành lý (`check_flight_details`)**: Xuất thông tin chính sách hành lý tiêu chuẩn của từng hãng bay riêng biệt.
5. **Đặt vé thông minh (`book_flight`)**: Cấp phát mã PNR thành công chỉ khi AI thu thập đủ thông tin hành khách.
6. **Hủy/Xem trước vé (`manage_booking`)**: Quản lý vòng đời tấm vé đã ảo đã chốt trên hệ thống bộ nhớ.

> **⚠️ Hệ thống rào chắn (Guardrails):** Model được tinh chỉnh bằng System Prompt nghiêm ngặt, từ chối trả lời mọi câu hỏi nằm ngoài phạm vi du lịch Việt Nam (như Toán học, Logic, Coding, v.v.).

---

## 🛠 Yêu Cầu Cài Đặt

1. **Python**: Đảm bảo máy tính đã cài đặt Python 3.9 trở lên.
2. **Cài đặt thư viện**: Môi trường yêu cầu các gói trong tệp `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
   *(Bao gồm: langchain, langchain-openai, langgraph, python-dotenv, langchain-google-genai, rich)*

3. **Cấu hình API Key**:
   - Sao chép nội dung tệp `.env.example` thành tệp `.env`.
   - Lấy API Key từ Google AI Studio và kết nối nó vào tham số:
     ```env
     GEMINI_API_KEY=AIzaSy...
     ```

---

## 🚀 Khởi Chạy Ứng Dụng

Chạy dự án trên Terminal bằng lệnh sau:
```bash
python agent.py
```

- Gõ thông điệp bằng tiếng Việt có dấu. Agent sẽ tự động suy nghĩ và kích hoạt Tool phù hợp. 
- Để thoát chương trình an toàn, hãy gõ `quit` hoặc `exit`.
- *Lưu ý: Mọi giao dịch đặt vé đều diễn ra vào mô phỏng lưu trữ trong RAM, và sẽ bị reset khi bạn tắt Server Terminal.*

---

## 📑 Tài Liệu Đi Kèm
* `test_cases.md`: Các câu lệnh chuẩn để người dùng nhập thử.
* `test_result.md`: Báo cáo Log Terminal minh chứng thực tế các Tool đã vận hành tốt ra sao.
* `Assignment.md`: Yêu cầu kỹ thuật chi tiết của bài Lab.
