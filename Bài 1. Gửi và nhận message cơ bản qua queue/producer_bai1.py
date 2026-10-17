import time
import sys
from datetime import datetime
import pika

# ==========================================================
# CẤU HÌNH CLOUDAMQP BROKER
# ==========================================================
AMQP_URL = "amqps://edyjsave:eAvCbSvcllDVRa-Vx8l-AtfPwVRumSnS@gerbil.rmq.cloudamqp.com/edyjsave"
QUEUE_NAME = "iot_lab_queue"

# ==========================================================
# THÔNG TIN SINH VIÊN & THÔNG ĐIỆP
# ==========================================================
STUDENT_NAME = "Nguyen Cong Hai Nam"
STUDENT_ID = "B23DCCN583"  # Mã sinh viên
GREETING = "Xin chao tu ung dung Python AMQP"

def create_connection():
    """Tạo kết nối và channel tới CloudAMQP broker."""
    params = pika.URLParameters(AMQP_URL)
    connection = pika.BlockingConnection(params)
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
    print("Broker: CloudAMQP (gerbil.rmq.cloudamqp.com)")
    print(f"Queue: {QUEUE_NAME}")
    print(f"Sinh viên: {STUDENT_NAME} - MSV: {STUDENT_ID}")
    print("=" * 60)

    try:
        print("Đang kết nối tới CloudAMQP Broker...")
        connection, channel = create_connection()
        print("-> Kết nối thành công và đã sẵn sàng queue!\n")
    except Exception as e:
        print(f"\n[ERROR] Không thể kết nối tới CloudAMQP broker: {e}")
        print("[GỢI Ý] Hãy kiểm tra kết nối Internet và URL CloudAMQP.")
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
            print("Đang đóng kết nối CloudAMQP...")
            connection.close()
            print("Đã ngắt kết nối an toàn. Kết thúc chương trình Producer.")

if __name__ == "__main__":
    main()
