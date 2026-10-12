import time
import sys
from datetime import datetime
import pika

# ==========================================================
# CẤU HÌNH RABBITMQ BROKER
# ==========================================================
# Mặc định kết nối tới RabbitMQ cục bộ hoặc broker dùng chung
RABBITMQ_HOST = "localhost"
RABBITMQ_PORT = 5672
RABBITMQ_USER = "guest"
RABBITMQ_PASS = "guest"
QUEUE_NAME = "iot_lab_queue"

# ==========================================================
# THÔNG TIN SINH VIÊN & THÔNG ĐIỆP
# ==========================================================
STUDENT_NAME = "Nguyen Cong Hai Nam"
STUDENT_ID = "B23DCCN583"  # Mã sinh viên
GREETING = "Xin chao tu ung dung Python AMQP"

def create_connection():
    """Tạo kết nối và channel tới RabbitMQ broker."""
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    parameters = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        credentials=credentials,
        connection_attempts=3,
        retry_delay=2
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    # Khởi tạo queue (nếu chưa tồn tại)
    channel.queue_declare(queue=QUEUE_NAME, durable=False)
    return connection, channel

def send_single_message(channel):
    """Gửi 1 message đơn lẻ theo đúng yêu cầu đề bài."""
    payload = f"{GREETING} - {STUDENT_ID} - {STUDENT_NAME}"
    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=payload.encode("utf-8")
    )
    now_str = datetime.now().strftime("%H:%M:%S")
    print(f"[{now_str}] Đã gửi thành công message vào queue '{QUEUE_NAME}':")
    print(f"  Nội dung: {payload}")
    print("-" * 60)

def send_continuous_messages(channel, interval=3):
    """Phần mở rộng: Gửi nhiều message liên tiếp định kỳ cho đến khi dừng bằng Ctrl+C."""
    print(f"-> Chế độ mở rộng: Gửi liên tiếp mỗi {interval} giây.")
    print("Nhấn Ctrl+C để dừng chương trình bất cứ lúc nào.\n")
    
    count = 1
    while True:
        # Nội dung message chứa thông tin sinh viên kèm số thứ tự
        payload = f"{GREETING} - {STUDENT_ID} - {STUDENT_NAME} (Message #{count})"
        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=payload.encode("utf-8")
        )
        now_str = datetime.now().strftime("%H:%M:%S")
        print(f"[{now_str}] Đã gửi message #{count} vào queue '{QUEUE_NAME}':")
        print(f"  Nội dung: {payload}")
        print("-" * 60)
        
        count += 1
        time.sleep(interval)

def main():
    print("=" * 60)
    print("CHƯƠNG TRÌNH PRODUCER - BÀI 1: GỬI MESSAGE QUA AMQP QUEUE")
    print(f"Broker: {RABBITMQ_HOST}:{RABBITMQ_PORT}")
    print(f"Queue: {QUEUE_NAME}")
    print(f"Sinh viên: {STUDENT_NAME} - MSV: {STUDENT_ID}")
    print("=" * 60)

    try:
        print(f"Đang kết nối tới RabbitMQ Broker '{RABBITMQ_HOST}:{RABBITMQ_PORT}'...")
        connection, channel = create_connection()
        print("-> Kết nối thành công và đã khởi tạo queue!\n")
    except Exception as e:
        print(f"\n[ERROR] Không thể kết nối tới RabbitMQ broker: {e}")
        print("[GỢI Ý] Hãy đảm bảo RabbitMQ server đang chạy (ví dụ: brew services start rabbitmq hoặc docker run -d -p 5672:5672 rabbitmq:3-management).")
        sys.exit(1)

    try:
        # Nếu truyền tham số --single thì gửi 1 lần, mặc định chạy chế độ liên tiếp (phần mở rộng)
        if len(sys.argv) > 1 and sys.argv[1] == "--single":
            print("Chế độ: Gửi 1 message đơn lẻ.")
            send_single_message(channel)
        else:
            send_continuous_messages(channel, interval=3)

    except KeyboardInterrupt:
        print("\n[INFO] Đã nhận tín hiệu dừng từ người dùng (Ctrl+C).")
    except Exception as e:
        print(f"\n[ERROR] Đã xảy ra lỗi trong quá trình gửi: {e}")
    finally:
        if connection and connection.is_open:
            print("Đang đóng kết nối RabbitMQ...")
            connection.close()
            print("Đã ngắt kết nối an toàn. Kết thúc chương trình Producer.")

if __name__ == "__main__":
    main()
