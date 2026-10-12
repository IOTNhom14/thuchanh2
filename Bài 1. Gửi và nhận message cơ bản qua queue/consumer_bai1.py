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

def on_message_received(ch, method, properties, body):
    """Callback được gọi mỗi khi nhận được message từ queue."""
    receive_time = datetime.now().strftime("%H:%M:%S")
    try:
        payload = body.decode("utf-8")
    except UnicodeDecodeError:
        payload = str(body)

    # Hiển thị đúng định dạng yêu cầu đầu ra của đề bài:
    print(f"Da nhan message: {payload}")
    print(f"Thoi gian nhan: {receive_time}")
    print("-" * 60)

    # Xác nhận đã xử lý message (acknowledgement)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    print("=" * 60)
    print("CHƯƠNG TRÌNH CONSUMER - BÀI 1: LẮNG NGHE MESSAGE TỪ AMQP QUEUE")
    print(f"Broker: {RABBITMQ_HOST}:{RABBITMQ_PORT}")
    print(f"Lắng nghe queue: {QUEUE_NAME}")
    print("=" * 60)

    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    parameters = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        credentials=credentials,
        connection_attempts=3,
        retry_delay=2
    )

    try:
        print(f"Đang kết nối tới RabbitMQ Broker '{RABBITMQ_HOST}:{RABBITMQ_PORT}'...")
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        print("-> Kết nối thành công tới broker!")

        # Đảm bảo queue tồn tại trước khi consume
        channel.queue_declare(queue=QUEUE_NAME, durable=False)

        # Phân phối công bằng: chỉ nhận 1 message tại một thời điểm
        channel.basic_qos(prefetch_count=1)

        # Đăng ký nhận message từ queue
        channel.basic_consume(
            queue=QUEUE_NAME,
            on_message_callback=on_message_received,
            auto_ack=False
        )

        print(f"-> Đã sẵn sàng lắng nghe trên queue '{QUEUE_NAME}'.")
        print("Đang chờ nhận message... (Nhấn Ctrl+C để dừng chương trình)")
        print("=" * 60 + "\n")

        # Chạy liên tục cho tới khi người dùng bấm Ctrl+C (phần mở rộng)
        channel.start_consuming()

    except KeyboardInterrupt:
        print("\n[INFO] Đã nhận tín hiệu dừng từ người dùng (Ctrl+C).")
        try:
            channel.stop_consuming()
        except Exception:
            pass
    except Exception as e:
        print(f"\n[ERROR] Không thể kết nối hoặc xảy ra lỗi: {e}")
        print("[GỢI Ý] Hãy đảm bảo RabbitMQ server đang chạy (ví dụ: brew services start rabbitmq hoặc docker run -d -p 5672:5672 rabbitmq:3-management).")
    finally:
        try:
            if 'connection' in locals() and connection.is_open:
                print("Đang đóng kết nối RabbitMQ...")
                connection.close()
                print("Đã ngắt kết nối an toàn. Kết thúc chương trình Consumer.")
        except Exception:
            pass

if __name__ == "__main__":
    main()
