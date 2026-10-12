# BÁO CÁO THỰC HÀNH: LẬP TRÌNH PYTHON VỚI GIAO THỨC AMQP


---

## 1. BROKER SỬ DỤNG
- **Broker:** RabbitMQ
- **Host:** `localhost` (127.0.0.1) hoặc IP của broker dùng chung
- **Port:** `5672` (cổng giao thức AMQP mặc định)
- **Tài khoản / Mật khẩu:** `guest` / `guest`
- **Queue sử dụng cho Bài 1:** `iot_lab_queue`
- **Thư viện kết nối:** `pika` (Cài đặt: `pip install pika`)

*(Lưu ý: Nếu chạy RabbitMQ cục bộ, có thể khởi động qua Homebrew `brew services start rabbitmq` hoặc Docker `docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management`)*

---

## 2. CÁCH CHẠY TỪNG CHƯƠNG TRÌNH

### Bài 1: Gửi và nhận message cơ bản qua queue (kèm phần mở rộng)

> **Lưu ý:** Luôn khởi động **Consumer** trước để sẵn sàng lắng nghe queue, sau đó mới khởi động **Producer**.

#### Bước 1: Chạy Consumer (lắng nghe liên tục)
Mở terminal thứ nhất và chạy:
```bash
python3 "Bài 1. Gửi và nhận message cơ bản qua queue/consumer_bai1.py"
```
- Chương trình sẽ kết nối broker, khởi tạo queue `iot_lab_queue` và duy trì lắng nghe liên tục cho đến khi người dùng nhấn `Ctrl+C`.

#### Bước 2: Chạy Producer (gửi message vào queue)
Mở terminal thứ hai và chạy:

- **Chế độ mở rộng (Gửi liên tiếp nhiều message mỗi 3 giây):**
  ```bash
  python3 "Bài 1. Gửi và nhận message cơ bản qua queue/producer_bai1.py"
  ```
  Producer sẽ tự động gửi thông điệp kèm số thứ tự định kỳ mỗi 3 giây cho đến khi dừng bằng `Ctrl+C`.

- **Chế độ gửi 1 message đơn lẻ:**
  ```bash
  python3 "Bài 1. Gửi và nhận message cơ bản qua queue/producer_bai1.py" --single
  ```

---

## 3. KẾT QUẢ ĐẠT ĐƯỢC

### Output thực tế phía Producer:
```text
============================================================
CHƯƠNG TRÌNH PRODUCER - BÀI 1: GỬI MESSAGE QUA AMQP QUEUE
Broker: localhost:5672
Queue: iot_lab_queue
Sinh viên: Nguyen Cong Hai Nam - MSV: B23DCCN583
============================================================
Đang kết nối tới RabbitMQ Broker 'localhost:5672'...
-> Kết nối thành công và đã khởi tạo queue!

-> Chế độ mở rộng: Gửi liên tiếp mỗi 3 giây.
Nhấn Ctrl+C để dừng chương trình bất cứ lúc nào.

[14:05:18] Đã gửi message #1 vào queue 'iot_lab_queue':
  Nội dung: Xin chao tu ung dung Python AMQP - B23DCCN583 - Nguyen Cong Hai Nam (Message #1)
------------------------------------------------------------
[14:05:21] Đã gửi message #2 vào queue 'iot_lab_queue':
  Nội dung: Xin chao tu ung dung Python AMQP - B23DCCN583 - Nguyen Cong Hai Nam (Message #2)
------------------------------------------------------------
```

### Output thực tế phía Consumer:
```text
============================================================
CHƯƠNG TRÌNH CONSUMER - BÀI 1: LẮNG NGHE MESSAGE TỪ AMQP QUEUE
Broker: localhost:5672
Lắng nghe queue: iot_lab_queue
============================================================
Đang kết nối tới RabbitMQ Broker 'localhost:5672'...
-> Kết nối thành công tới broker!
-> Đã sẵn sàng lắng nghe trên queue 'iot_lab_queue'.
Đang chờ nhận message... (Nhấn Ctrl+C để dừng chương trình)
============================================================

Da nhan message: Xin chao tu ung dung Python AMQP - B23DCCN583 - Nguyen Cong Hai Nam (Message #1)
Thoi gian nhan: 14:05:18
------------------------------------------------------------
Da nhan message: Xin chao tu ung dung Python AMQP - B23DCCN583 - Nguyen Cong Hai Nam (Message #2)
Thoi gian nhan: 14:05:21
------------------------------------------------------------
```

### Đánh giá theo yêu cầu đề bài:
1. **Kết nối broker:** Kết nối thành công tới RabbitMQ qua giao thức AMQP (`pika.BlockingConnection`).
2. **Gửi và nhận message:** 
   - Producer gửi message chứa đúng họ tên, mã sinh viên và lời chào: `Xin chao tu ung dung Python AMQP - B23DCCN583 - Nguyen Cong Hai Nam`.
   - Consumer nhận đúng queue `iot_lab_queue`, hiển thị chuẩn định dạng `Da nhan message: ...` và `Thoi gian nhan: HH:MM:SS`.
3. **Phần mở rộng:**
   - **Producer:** Gửi liên tiếp nhiều message có đánh số thứ tự định kỳ mỗi 3s.
   - **Consumer:** Duy trì lắng nghe liên tục đến khi dừng bằng `Ctrl+C`, xử lý dọn dẹp và ngắt kết nối an toàn.