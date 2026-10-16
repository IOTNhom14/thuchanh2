import pika
from datetime import datetime

# Cấu hình địa chỉ RabbitMQ Broker (Sửa lại nếu dùng IP broker chung của lớp)
BROKER_HOST = 'localhost'
EXCHANGE_NAME = 'iot_alert_exchange'
QUEUE_NAME = 'critical_queue'
ROUTING_KEY = 'critical'

def callback(ch, method, properties, body):
    message = body.decode('utf-8')
    # In ra màn hình theo đúng định dạng yêu cầu đầu ra của đề bài
    output = f"[{QUEUE_NAME}] Da nhan: {message}"
    print(output)
    
    # Phần mở rộng: Ghi log cảnh báo ra file
    with open("alert_logs.txt", "a", encoding="utf-8") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] {output}\n")

def main():
    # 1. Kết nối tới RabbitMQ broker
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=BROKER_HOST))
    channel = connection.channel()

    # 2. Khai báo direct exchange tên iot_alert_exchange
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct')

    # 3. Tạo queue tên critical_queue
    channel.queue_declare(queue=QUEUE_NAME)

    # 4. Bind queue với exchange bằng routing key 'critical'
    channel.queue_bind(
        exchange=EXCHANGE_NAME,
        queue=QUEUE_NAME,
        routing_key=ROUTING_KEY
    )

    print(f"[*] Đang chờ cảnh báo mức '{ROUTING_KEY}' tại [{QUEUE_NAME}]. Nhấn Ctrl+C để thoát.")

    # 5. Lắng nghe và nhận message
    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback,
        auto_ack=True
    )

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\nĐã dừng Critical Consumer.")
        channel.stop_consuming()
    finally:
        connection.close()

if __name__ == '__main__':
    main()