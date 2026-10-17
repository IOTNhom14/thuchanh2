# BÁO CÁO THỰC HÀNH: LẬP TRÌNH PYTHON VỚI GIAO THỨC AMQP (CLOUDAMQP)

---

## 1. BROKER SỬ DỤNG
- **Dịch vụ Broker:** CloudAMQP (RabbitMQ as a Service)
- **Giao thức:** AMQPS (AMQP 0-9-1 có mã hóa bảo mật SSL/TLS qua cổng 5671)
- **AMQP URL:** 
  ```text
  amqps://edyjsave:eAvCbSvcllDVRa-Vx8l-AtfPwVRumSnS@gerbil.rmq.cloudamqp.com/edyjsave
  ```
- **Thư viện Python:** `pika` (Cài đặt: `pip install pika`)

---

## 2. CÁCH CHẠY TỪNG CHƯƠNG TRÌNH

> **Quy tắc:** Luôn chạy các chương trình **Consumer / Monitor** trước để sẵn sàng lắng nghe, sau đó mới chạy **Producer / Sensor** để phát message.

---

### BÀI 1: Gửi và nhận message cơ bản qua queue

1. **Khởi động Consumer (lắng nghe queue liên tục):**
   ```bash
   python3 "Bài 1. Gửi và nhận message cơ bản qua queue/consumer_bai1.py"
   ```
2. **Khởi động Producer (gửi message vào queue):**
   - **Chế độ mở rộng (mặc định gửi liên tiếp mỗi 3 giây, dừng bằng Ctrl+C):**
     ```bash
     python3 "Bài 1. Gửi và nhận message cơ bản qua queue/producer_bai1.py"
     ```
   - **Chế độ gửi 1 message đơn lẻ:**
     ```bash
     python3 "Bài 1. Gửi và nhận message cơ bản qua queue/producer_bai1.py" --single
     ```

---

### BÀI 2: Mô phỏng cảm biến IoT gửi dữ liệu môi trường

1. **Khởi động Monitoring Consumer:**
   Mở terminal thứ nhất:
   ```bash
   python3 "Bài 2. Mô phỏng cảm biến IoT gửi dữ liệu môi trường/monitor_consumer_bai2.py"
   ```
2. **Khởi động Sensor Producer:**
   Mở terminal thứ hai:
   ```bash
   python3 "Bài 2. Mô phỏng cảm biến IoT gửi dữ liệu môi trường/sensor_producer_bai2.py"
   ```

---

### BÀI 3: Mô phỏng hệ thống điều phối cảnh báo IoT với direct exchange

1. **Khởi động Warning Consumer (chỉ nhận cảnh báo mức `warning`):**
   Mở terminal thứ nhất:
   ```bash
   python3 "Bài 3. Mô phỏng hệ thống điều phối cảnh báo IoT với exchange/warning_consumer_bai3.py"
   ```
2. **Khởi động Critical Consumer (chỉ nhận cảnh báo mức `critical`):**
   Mở terminal thứ hai:
   ```bash
   python3 "Bài 3. Mô phỏng hệ thống điều phối cảnh báo IoT với exchange/critical_consumer_bai3.py"
   ```
3. **Khởi động Alert Producer (phát các cảnh báo `info`, `warning`, `critical`):**
   Mở terminal thứ ba:
   ```bash
   python3 "Bài 3. Mô phỏng hệ thống điều phối cảnh báo IoT với exchange/alert_producer_bai3.py"
   ```

---

## 3. KẾT QUẢ ĐẠT ĐƯỢC

### 1. Kết quả Bài 1 (Queue: `iot_lab_queue`)
- **Producer Output:**
  ```text
  ============================================================
  CHƯƠNG TRÌNH PRODUCER - BÀI 1: GỬI MESSAGE QUA AMQP QUEUE
  Broker: CloudAMQP (gerbil.rmq.cloudamqp.com)
  Queue: iot_lab_queue
  Sinh viên: Nguyen Cong Hai Nam - MSV: B23DCCN583
  ============================================================
  Đang kết nối tới CloudAMQP Broker...
  -> Kết nối thành công và đã sẵn sàng queue!

  -> Chế độ mở rộng: Gửi liên tiếp mỗi 3 giây.
  Nhấn Ctrl+C để dừng chương trình bất cứ lúc nào.

  [14:05:18] Đã gửi message #1 vào queue 'iot_lab_queue':
    Nội dung: Xin chao tu ung dung Python AMQP - B23DCCN583 - Nguyen Cong Hai Nam (Message #1)
  ------------------------------------------------------------
  [14:05:21] Đã gửi message #2 vào queue 'iot_lab_queue':
    Nội dung: Xin chao tu ung dung Python AMQP - B23DCCN583 - Nguyen Cong Hai Nam (Message #2)
  ------------------------------------------------------------
  ```
- **Consumer Output:**
  ```text
  ============================================================
  CHƯƠNG TRÌNH CONSUMER - BÀI 1: LẮNG NGHE MESSAGE TỪ AMQP QUEUE
  Broker: CloudAMQP (gerbil.rmq.cloudamqp.com)
  Lắng nghe queue: iot_lab_queue
  ============================================================
  Đang kết nối tới CloudAMQP Broker...
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

---

### 2. Kết quả Bài 2 (Queue: `sensor_data_queue`)
- **Sensor Producer Output:**
  ```text
  Đã kết nối tới CloudAMQP Broker!
  Bắt đầu gửi dữ liệu mỗi 3 giây (Nhấn Ctrl+C để dừng)...

  Đã gửi: {"device_id": "sensor01", "temperature": 36.4, "humidity": 38.9, "timestamp": "2026-10-17 18:45:10"}
  Đã gửi: {"device_id": "sensor01", "temperature": 28.2, "humidity": 65.4, "timestamp": "2026-10-17 18:45:13"}
  ```
- **Monitoring Consumer Output:**
  ```text
  Đang lắng nghe queue 'sensor_data_queue' trên CloudAMQP (Nhấn Ctrl+C để thoát)...
  ------------------------------
  Device: sensor01
  Temperature: 36.4
  Humidity: 38.9
  Timestamp: 2026-10-17 18:45:10
  CANH BAO: Nhiet do cao
  CANH BAO: Do am thap
  ------------------------------
  Device: sensor01
  Temperature: 28.2
  Humidity: 65.4
  Timestamp: 2026-10-17 18:45:13
  ------------------------------
  ```

---

### 3. Kết quả Bài 3 (Exchange: `iot_alert_exchange`)
- **Alert Producer Output:**
  ```text
  --- BẮT ĐẦU GỬI CẢNH BÁO TỚI EXCHANGE TRÊN CLOUDAMQP ---
  [x] Đã gửi (routing_key='info'): He thong cam bien hoat dong binh thuong info
  [x] Đã gửi (routing_key='warning'): Nhiet do phong may vuot nguong warning
  [x] Đã gửi (routing_key='critical'): Cam bien kho lanh mat ket noi critical
  --- HOÀN TẤT GỬI CẢNH BÁO ---
  ```
- **Warning Consumer Output:**
  ```text
  [*] Đang chờ cảnh báo mức 'warning' tại [warning_queue] trên CloudAMQP. Nhấn Ctrl+C để thoát.
  [warning_queue] Da nhan: Nhiet do phong may vuot nguong warning
  ```
- **Critical Consumer Output:**
  ```text
  [*] Đang chờ cảnh báo mức 'critical' tại [critical_queue] trên CloudAMQP. Nhấn Ctrl+C để thoát.
  [critical_queue] Da nhan: Cam bien kho lanh mat ket noi critical
  ```
- **File log ghi nhận (`alert_logs.txt`):**
  ```text
  [2026-10-17 18:50:02] [warning_queue] Da nhan: Nhiet do phong may vuot nguong warning
  [2026-10-17 18:50:03] [critical_queue] Da nhan: Cam bien kho lanh mat ket noi critical
  ```

---

### 4. Đánh giá tổng kết
- Toàn bộ 3 bài đều chạy đồng nhất trên **CloudAMQP**, đảm bảo kết nối qua Internet ổn định và bảo mật (AMQPS).
- Đáp ứng 100% các yêu cầu từ cấu trúc queue, direct exchange, routing key đến định dạng đầu ra.
- Hoàn thành các phần mở rộng: gửi tuần hoàn, thời gian gửi `timestamp`, ghi log file cảnh báo.