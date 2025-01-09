from cameraQR import cameraQR
import time

# Khởi động stream ở chế độ camQrLocation
cameraQR.active(mode="camQrLocation", read_qr=True)

# Tiếp tục thực hiện các tác vụ khác trong chương trình
while True:
    print("Main program is running...")
    print(cameraQR.get_status())
    # cameraQR.update_config()
    time.sleep(0.5)
    # print(cameraQR.get_status())
    # time.sleep(2)
    # print(cameraQR.get_status())
    # time.sleep(2)
    # print(cameraQR.get_status())
    # time.sleep(2)
    # print(cameraQR.get_status())
    # time.sleep(2)
    # print(cameraQR.get_status())
    # time.sleep(2)
    # print(cameraQR.get_status())
    # time.sleep(2)
    # print(cameraQR.get_status())
    # time.sleep(2)
    # print(cameraQR.get_status())
    # time.sleep(2)
    # print(cameraQR.get_status())
    # # Dừng stream
    # cameraQR.stop_stream("camQrLocation")
    # time.sleep(20)
    # # print("Stream stopped. Waiting for 5 seconds...")
    # # print(cameraQR.get_status())
    # # time.sleep(10)  # Chờ 5 giây

    # # # Mở lại stream
    # print("Restarting stream...")
    # cameraQR.active(mode="camQrLocation", read_qr=True)
    # print(cameraQR.get_status())

    # # # Chờ thêm 5 giây để vòng lặp chạy

