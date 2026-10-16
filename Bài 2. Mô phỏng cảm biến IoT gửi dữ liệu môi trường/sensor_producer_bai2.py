import pika
import json
import time
import random

AMQP_URL = "amqps://edyjsave:eAvCbSvcllDVRa-Vx8l-AtfPwVRumSnS@gerbil.rmq.cloudamqp.com/edyjsave"
QUEUE_NAME = "sensor_data_queue"

# Kết nối tới Cloud Broker qua URL
params = pika.URLParameters(AMQP_URL)
connection = pika.BlockingConnection(params)
channel = connection.channel()

# Tạo hoặc sử dụng queue sensor_data_queue
channel.queue_declare(queue=QUEUE_NAME)

print("Đã kết nối tới CloudAMQP Broker!")
print("Bắt đầu gửi dữ liệu mỗi 3 giây (Nhấn Ctrl+C để dừng)...\n")

try:
    while True:
        # Sinh ngẫu nhiên nhiệt độ và độ ẩm
        payload_dict = {
            "device_id": "sensor01",
            "temperature": round(random.uniform(20.0, 40.0), 1),
            "humidity": round(random.uniform(30.0, 80.0), 1)
        }
        
        message_json = json.dumps(payload_dict)
        
        # Gửi dữ liệu vào sensor_data_queue
        channel.basic_publish(
            exchange='',
            routing_key=QUEUE_NAME,
            body=message_json
        )
        
        print(f"Đã gửi: {message_json}")
        time.sleep(3)

except KeyboardInterrupt:
    print("\nĐã dừng chương trình Producer.")
finally:
    connection.close()