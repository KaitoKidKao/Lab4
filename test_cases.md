# Test Cases cho Agent TravelBuddy


## 1. Tool `search_flights` (Tìm kiếm chuyến bay)
**Test Case 1.1 - Tuyến bay phổ biến**
- **User:** "Tìm cho tôi vé máy bay từ Hà Nội đi Hồ Chí Minh."
- **Kỳ vọng:** Agent gọi tool `search_flights(origin="Hà Nội", destination="Hồ Chí Minh")` và trả về danh sách các chuyến bay (Vietnam Airlines, VietJet, Bamboo...), lịch trình bay và giá cả tương ứng.

**Test Case 1.2 - Tuyến bay ngược / Không tồn tại trực tiếp**
- **User:** "Tôi muốn bay từ Đà Nẵng ra Hà Nội."
- **Kỳ vọng:** Agent gọi `search_flights(origin="Đà Nẵng", destination="Hà Nội")`. Tuyến này trong DataBase chỉ có chiều (`Hà Nội` -> `Đà Nẵng`), do đó hàm sẽ tự đảo ngược (reverse) và báo với user rằng "Không tìm thấy trực tiếp, nhưng có chuyến chiều ngược lại...".

---

## 2. Tool `search_hotels` (Tìm khách sạn)
**Test Case 2.1 - Có giới hạn mức giá**
- **User:** "Tôi muốn thuê phòng khách sạn ở Đà Nẵng, giá mềm gọn dưới 500k/đêm."
- **Kỳ vọng:** Agent gọi tool `search_hotels(city="Đà Nẵng", max_price_per_night=500000)`. Tool sẽ lọc ra các khách sạn chuẩn như *Memory Hostel* (250.000₫) hay *Christina's Homestay* (350.000₫).

**Test Case 2.2 - Yêu cầu phi thực tế (Vượt khả năng đáp ứng)**
- **User:** "Có khách sạn nào ở Hồ Chí Minh rẻ hơn 100k/đêm không?"
- **Kỳ vọng:** Agent gọi tool `search_hotels(city="Hồ Chí Minh", max_price_per_night=100000)`. Vì kết quả lọc ra bị rỗng, Agent sẽ thông báo cho khách là không có khách sạn với mức giá trên và yêu cầu tăng ngân sách.

---

## 3. Tool `calculate_budget` (Tính toán ngân sách)
**Test Case 3.1 - Trong phạm vi ngân sách**
- **User:** "Mình có 10 triệu, đã mất 2.800.000đ mua vé bay khứ hồi và 3.500.000đ cho resort. Báo cáo lại cho mình."
- **Kỳ vọng:** Agent gọi tool `calculate_budget(total_budget=10000000, expenses="vé bay khứ hồi:2800000, resort:3500000")`. Agent trả về bảng chi phí được định dạng và báo cáo số dư là `3.700.000₫`.

**Test Case 3.2 - Âm / Vượt quá ngân sách**
- **User:** "Tôi có khoảng 3 triệu đi Phú Quốc. Nhưng đã đi Vietnam Airlines 2.100.000đ và ở Sol by Meliá hết 1.500.000đ."
- **Kỳ vọng:** Agent gọi tool `calculate_budget(total_budget=3000000, expenses="Vietnam Airlines:2100000, Sol by Meliá:1500000")`. Tổng chi phí là `3.600.000₫`, Agent sẽ lấy kết quả từ tool để hiển thị rủi ro âm ngân sách `600.000₫` và yêu cầu người dùng thay đổi lịch trình.

---

## 4. Tool `check_flight_details` (Thông tin hành lý & ghế trống)
**Test Case 4.1 - Kiểm tra hạng ghế economy hãng truyền thống**
- **User:** "Hạng economy của Vietnam Airlines thì mang được bao nhiêu kg hành lý?"
- **Kỳ vọng:** Agent gọi tool `check_flight_details(airline="Vietnam Airlines", flight_class="economy")`. Trả lời rằng khách có tùy chọn xách tay, ký gửi (7kg xách tay + 23kg ký gửi) và báo cáo số lượng ghế còn trống ngẫu nhiên từ tool.

**Test Case 4.2 - Kiểm tra hãng hàng không giá rẻ (LCC)**
- **User:** "Nếu đi VietJet hạng business thì có được ký gửi không? Cờn nhiều ghế không?"
- **Kỳ vọng:** Agent gọi tool `check_flight_details(airline="VietJet", flight_class="business")`, thông báo hành khách được cung cấp 10kg xách tay và 30kg ký gửi theo code mô phỏng.

---

## 5. Tool `book_flight` (Chốt đặt vé ảo)
**Test Case 5.1 - Cung cấp đồng thời mọi thông tin**
- **User:** "Tôi quyết định chốt chuyến bay Vietnam Airlines lúc 06:00 nhé. Tên tôi là Cristiano Ronaldo."
- **Kỳ vọng:** Agent đã có đủ input và có lời đồng tình => Gọi tool `book_flight(airline="Vietnam Airlines", departure="06:00", passenger_name="Cristiano Ronaldo")`. Agent tiếp nhận kết quả (mã PNR như `AB1C2D`) và chúc mừng khách hàng.

**Test Case 5.2 - Sự kiện thiếu thông tin (Trigger logic phòng thủ)**
- **User:** "Cho mình đặt vé hạng Business của Vietnam Airlines khởi hành lúc 14:00 đi."
- **Kỳ vọng:** Theo Rules trong thẻ `<rules>`, Agent KHÔNG được gọi `book_flight` nếu thiếu tên hành khách. Lệnh API Tool sẽ không chạy. Thay vì đó, Agent phản hồi dạng: "Dạ vâng, để tiến hành vé em cần thêm Tên Hành Khách của anh/chị ạ!".

---

## 6. Tool `manage_booking` (Quản lý - Xem và Hủy vé)
**Test Case 6.1 - Xem lại vé đã đặt**
- **User:** "Bạn kiểm tra lại giúp tôi vé máy bay mã VJ1ABX xem tên đúng chưa?"
- **Kỳ vọng:** Agent gọi tool `manage_booking(booking_code="VJ1ABX", action="check")` và in ra thông tin chi tiết tên hành khách, hãng, giờ bay đang được lưu vào Database ảo `BOOKED_TICKETS`.

**Test Case 6.2 - Hủy thao tác (Trigger Cancel)**
- **User:** "Tôi có việc bận nên hãy hủy giúp tôi vé mang mã VJ1ABX đi nhé."
- **Kỳ vọng:** Agent tiếp tục gọi tool `manage_booking(booking_code="VJ1ABX", action="cancel")` để lật trạng thái hệ thống và thông báo Hủy vé thành công. Khi xem lại vé sẽ có status là "Cancelled".
