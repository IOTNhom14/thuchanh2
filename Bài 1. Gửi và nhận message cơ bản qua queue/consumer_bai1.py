import sys
from datetime import datetime
import pika

# ==========================================================
# CẤU HÌNH CLOUDAMQP BROKER
# ==========================================================
AMQP_URL = "amqps://edyjsave:eAvCbSvcllDVRa-Vx8l-AtfPwVRumSnS@gerbil.rmq.cloudamqp.com/edyjsave"
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
    print("Broker: CloudAMQP (gerbil.rmq.cloudamqp.com)")
    print(f"Lắng nghe queue: {QUEUE_NAME}")
    print("=" * 60)

    params = pika.URLParameters(AMQP_URL)

    try:
        print("Đang kết nối tới CloudAMQP Broker...")
        connection = pika.BlockingConnection(params)
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
        print("[GỢI Ý] Hãy kiểm tra kết nối Internet và URL CloudAMQP.")
    finally:
        try:
            if 'connection' in locals() and connection.is_open:
                print("Đang đóng kết nối CloudAMQP...")
                connection.close()
                print("Đã ngắt kết nối an toàn. Kết thúc chương trình Consumer.")
        except Exception:
            pass

if __name__ == "__main__":
    main()
