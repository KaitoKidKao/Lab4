from langchain_core.tools import tool
import random
import string

# Database giả lập lưu trữ vé đã book trong phiên làm việc
BOOKED_TICKETS = {}
# MOCK DATA - Dữ liệu giả lập hệ thống du lịch
# Lưu ý: Giá cả có logic (VD: cuối tuần đắt hơn, hạng cao hơn đắt hơn)
# Sinh viên cần đọc hiểu data để debug test cases.

AIRLINE_POLICIES_DB = {
    "vietnam airlines": {
        "economy": "7kg xách tay + 23kg ký gửi",
        "business": "14kg xách tay + 32kg ký gửi"
    },
    "vietjet air": {
        "economy": "7kg xách tay (Không bao gồm ký gửi)",
        "business": "10kg xách tay + 30kg ký gửi"
    },
    "bamboo airways": {
        "economy": "7kg xách tay (Không bao gồm ký gửi)",
        "business": "10kg xách tay + 30kg ký gửi"
    }
}

FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"flight_code": "VN101", "airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1_450_000, "class": "economy", "seats_left": 4},
        {"flight_code": "VN102", "airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business", "seats_left": 2},
        {"flight_code": "VJ201", "airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890_000, "class": "economy", "seats_left": 15},
        {"flight_code": "QH301", "airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy", "seats_left": 8},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"flight_code": "VN103", "airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2_100_000, "class": "economy", "seats_left": 10},
        {"flight_code": "VJ202", "airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy", "seats_left": 5},
        {"flight_code": "VJ203", "airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy", "seats_left": 20},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"flight_code": "VN104", "airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1_600_000, "class": "economy", "seats_left": 7},
        {"flight_code": "VJ204", "airline": "VietJet Air", "departure": "07:30", "arrival": "09:40", "price": 950_000, "class": "economy", "seats_left": 12},
        {"flight_code": "QH302", "airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1_300_000, "class": "economy", "seats_left": 9},
        {"flight_code": "VN105", "airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_200_000, "class": "business", "seats_left": 1},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"flight_code": "VN106", "airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_300_000, "class": "economy", "seats_left": 16},
        {"flight_code": "VJ205", "airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780_000, "class": "economy", "seats_left": 3},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"flight_code": "VN107", "airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy", "seats_left": 0},
        {"flight_code": "VJ206", "airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650_000, "class": "economy", "seats_left": 25},
    ],
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Sala Danang Beach", "stars": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê", "rating": 4.3},
        {"name": "Fivitel Danang", "stars": 3, "price_per_night": 650_000, "area": "Sơn Trà", "rating": 4.1},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250_000, "area": "Hải Châu", "rating": 4.6},
        {"name": "Christina's Homestay", "stars": 2, "price_per_night": 350_000, "area": "An Thượng", "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3_500_000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Sol by Meliá", "stars": 4, "price_per_night": 1_500_000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort", "stars": 3, "price_per_night": 800_000, "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel", "stars": 2, "price_per_night": 200_000, "area": "Dương Đông", "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2_800_000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1_400_000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550_000, "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room", "stars": 2, "price_per_night": 180_000, "area": "Quận 1", "rating": 4.6},
    ],
}

@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.
    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    - destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')
    Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
    Nếu không tìm thấy tuyến bay, trả về thông báo không có chuyến.
    """
    flights = FLIGHTS_DB.get((origin, destination))
    if not flights:
        # Thử tra ngược
        flights_reverse = FLIGHTS_DB.get((destination, origin))
        if flights_reverse:
            return f"Không tìm thấy chuyến bay trực tiếp từ {origin} đi {destination}. Tuy nhiên có chuyến bay chiều ngược lại, bạn có muốn xem không?"
        return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."

    result = f"Danh sách chuyến bay từ {origin} đi {destination}:\n"
    for idx, f in enumerate(flights, 1):
        price_str = f"{f['price']:,}".replace(",", ".")
        result += f"{idx}. [{f['flight_code']}] Hãng {f['airline']} ({f['class']}): Bay lúc {f['departure']}, đến lúc {f['arrival']}. Giá: {price_str}₫. (Còn {f['seats_left']} ghế)\n"
    return result

@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.
    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price_per_night: giá tối đa mỗi đêm (VNĐ), mặc định không giới hạn
    Trả về danh sách khách sạn phù hợp với tên, số sao, giá, khu vực, rating.
    """
    hotels = HOTELS_DB.get(city)
    if not hotels:
        return f"Không tìm thấy dữ liệu khách sạn tại {city}."
    
    # Lọc theo max_price_per_night
    filtered_hotels = [h for h in hotels if h["price_per_night"] <= max_price_per_night]
    
    if not filtered_hotels:
        return f"Không tìm thấy khách sạn tại {city} với giá dưới {max_price_per_night:,}₫/đêm. Hãy thử tăng ngân sách."
        
    # Sắp xếp theo rating giảm dần
    filtered_hotels.sort(key=lambda x: x["rating"], reverse=True)
    
    result = f"Danh sách khách sạn tại {city} phù hợp:\n"
    for idx, h in enumerate(filtered_hotels, 1):
        price_str = f"{h['price_per_night']:,}".replace(",", ".")
        result += f"{idx}. {h['name']} ({h['stars']} sao) - Rating: {h['rating']}/5. Khu vực: {h['area']}. Giá: {price_str}₫/đêm\n"
    return result

@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
    Tham số:
    - total_budget: tổng ngân sách ban đầu (VNĐ)
    - expenses: chuỗi mô tả các khoản chi, mỗi khoản cách nhau bởi dấu phẩy, định dạng 'tên khoản:số tiền' (VD: 'vé_máy_bay:890000,khách_sạn:650000')
    Trả về bảng chi tiết các khoản chi và số tiền còn lại.
    Nếu vượt ngân sách, cảnh báo rõ ràng số tiền thiếu.
    """
    try:
        if not expenses.strip():
            return "Chưa có khoản chi phí nào."
            
        items = expenses.split(",")
        total_expense = 0
        expense_details = ""
        
        for item in items:
            name, amount_str = item.split(":")
            name = name.strip()
            amount = int(amount_str.strip())
            total_expense += amount
            amount_fmt = f"{amount:,}".replace(",", ".")
            expense_details += f"- {name}: {amount_fmt}₫\n"
            
        remaining = total_budget - total_expense
        total_budget_fmt = f"{total_budget:,}".replace(",", ".")
        total_expense_fmt = f"{total_expense:,}".replace(",", ".")
        remaining_fmt = f"{abs(remaining):,}".replace(",", ".")
        
        result = "Bảng chi phí:\n" + expense_details
        result += f"Tổng chi: {total_expense_fmt}₫\n"
        result += f"Ngân sách: {total_budget_fmt}₫\n"
        
        if remaining < 0:
            result += f"Vượt ngân sách {remaining_fmt}₫! Cần điều chỉnh."
        else:
            result += f"Còn lại: {remaining_fmt}₫"
            
        return result
        
    except Exception as e:
        return "Lỗi format chuỗi expenses. Vui lòng sử dụng định dạng 'tên:số tiền,tên:số tiền'."

@tool
def check_flight_details(airline: str, flight_class: str) -> str:
    """
    Kiểm tra thông tin chi tiết hành lý quy định của một hãng bay và hạng vé.
    Tham số:
    - airline: Tên hãng bay (VD: Vietnam Airlines, VietJet Air)
    - flight_class: Hạng vé (economy, business)
    """
    airline_key = airline.lower()
    flight_class = flight_class.lower().strip()
    
    policies = AIRLINE_POLICIES_DB.get(airline_key)
    if not policies:
        # Thử tìm gần đúng
        for k in AIRLINE_POLICIES_DB.keys():
            if k in airline_key or airline_key in k:
                policies = AIRLINE_POLICIES_DB[k]
                break
                
    if not policies:
        return f"Không tìm thấy thông tin hành lý trong cơ sở dữ liệu (AIRLINE_POLICIES_DB) cho hãng {airline}."
        
    baggage_info = policies.get(flight_class)
    if not baggage_info:
        return f"Không có thông tin cho hạng {flight_class} của hãng {airline_key.title()}."
    
    return f"Thông tin Hãng {airline_key.title()} hạng {flight_class} được trích xuất từ DataBase:\n- Quy định hành lý: {baggage_info}"

@tool
def book_flight(airline: str, departure: str, passenger_name: str) -> str:
    """
    Giả lập đặt vé máy bay và tạo mã PNR. Yêu cầu truyền đúng tên khách hàng.
    Tham số:
    - airline: Hãng bay (VD: Vietnam Airlines)
    - departure: Giờ bay khởi hành
    - passenger_name: Tên hành khách. (Tuyệt đối phải thu thập thông tin này trước)
    """
    if not passenger_name:
        return "Lỗi: Không được bỏ trống tên hành khách. Hãy hỏi người dùng tên của họ."
        
    pnr = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    BOOKED_TICKETS[pnr] = {
        "airline": airline,
        "departure": departure,
        "passenger_name": passenger_name,
        "status": "Confirmed"
    }
    
    return f"Đã xuất vé thành công! Mã đặt chỗ (PNR) của quý khách {passenger_name} là: {pnr}"

@tool
def manage_booking(booking_code: str, action: str) -> str:
    """
    Quản lý vé đã đặt bằng mã PNR.
    Tham số:
    - booking_code: Mã PNR (VD: VJ99X2)
    - action: Hành động ('check' để xem vé, 'cancel' để hủy vé)
    """
    booking_code = booking_code.upper()
    if booking_code not in BOOKED_TICKETS:
        return f"Không tìm thấy vé nào với mã {booking_code} trong hệ thống."
        
    ticket = BOOKED_TICKETS[booking_code]
    
    if action == "cancel":
        ticket["status"] = "Cancelled"
        return f"Vé {booking_code} của hành khách {ticket['passenger_name']} đã bị Hủy."
    elif action == "check":
        return f"Thông tin vé {booking_code}:\n- Hành khách: {ticket['passenger_name']}\n- Chuyến bay: {ticket['airline']} lúc {ticket['departure']} \n- Trạng thái: {ticket['status']}"
    else:
        return "Action không hợp lệ. Chỉ chấp nhận 'check' hoặc 'cancel'."

