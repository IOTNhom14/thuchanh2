import pika
import json
import sys

AMQP_URL = "amqps://edyjsave:eAvCbSvcllDVRa-Vx8l-AtfPwVRumSnS@gerbil.rmq.cloudamqp.com/edyjsave"
QUEUE_NAME = "sensor_data_queue"

def callback(ch, method, properties, body):
    try:
        data = json.loads(body.decode('utf-8'))
        
        device_id = data.get("device_id", "Unknown")
        temperature = data.get("temperature", 0.0)
        humidity = data.get("humidity", 0.0)
        timestamp = data.get("timestamp")
        
        # In ra mã thiết bị, nhiệt độ, độ ẩm
        print(f"Device: {device_id}")
        print(f"Temperature: {temperature}")
        print(f"Humidity: {humidity}")
        # Hiển thị thời gian gửi (phần mở rộng)
        if timestamp:
            print(f"Timestamp: {timestamp}")
        
        # Kiểm tra ngưỡng cảnh báo
        if temperature > 35:
            print("CANH BAO: Nhiet do cao")
        if humidity < 40:
            print("CANH BAO: Do am thap")
            
        print("-" * 30)
        
    except Exception as e:
        print(f"Lỗi xử lý dữ liệu: {e}")

def main():
    params = pika.URLParameters(AMQP_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME)

    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback,
        auto_ack=True
    )

    print(f"Đang lắng nghe queue '{QUEUE_NAME}' trên CloudAMQP (Nhấn Ctrl+C để thoát)...\n")
    print("-" * 30)
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nĐã dừng chương trình Consumer.")
        sys.exit(0)