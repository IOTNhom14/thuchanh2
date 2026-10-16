import pika
import time

# Cấu hình địa chỉ RabbitMQ Broker (Sửa lại nếu dùng IP broker chung của lớp)
BROKER_HOST = 'localhost'
EXCHANGE_NAME = 'iot_alert_exchange'

def main():
    # 1. Kết nối tới RabbitMQ broker
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=BROKER_HOST))
    channel = connection.channel()

    # 2. Tạo direct exchange tên iot_alert_exchange
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct')

    # 3. Danh sách các cảnh báo mẫu với 3 mức: info, warning, critical
    alerts = [
        ("info", "He thong cam bien hoat dong binh thuong info"),
        ("warning", "Nhiet do phong may vuot nguong warning"),
        ("critical", "Cam bien kho lanh mat ket noi critical")
    ]

    print("--- BẮT ĐẦU GỬI CẢNH BÁO TỚI EXCHANGE ---")
    for routing_key, message in alerts:
        # Gửi message vào exchange kèm theo routing_key tương ứng
        channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key=routing_key,
            body=message.encode('utf-8')
        )
        print(f"[x] Đã gửi (routing_key='{routing_key}'): {message}")
        time.sleep(1)

    # 4. Đóng kết nối
    connection.close()
    print("--- HOÀN TẤT GỬI CẢNH BÁO ---")

if __name__ == '__main__':
    main()