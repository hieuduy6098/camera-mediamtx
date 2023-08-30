import cv2
import os
import time
from config import *
from datetime import datetime

"""
- parameter:
    id: station camera id 
    string_time: thời gian "20230816114858"
- output: status
    0: lỗi
    1: thành công
    2: ko tồn tại đường dẫn source video lưu lâu dài
    3: camera lỗi không lưu video mới
"""
# chụp ảnh
def capture(id, link_rtsp):
    try:
        cap = cv2.VideoCapture(link_rtsp)
        # Check if the stream was successfully opened.
        if not cap.isOpened():
            print(f"Failed to open RTSP stream: {link_rtsp}")
            return 0, ""
        ret, frame = cap.read()

        # kiểm tra đường dẫn output tồn tại chưa, nếu chưa -> tạo
        if os.path.exists(capture_path+id) == False:
            os.makedirs(capture_path+id)

        # Lưu frame dưới dạng JPG

        string_time = datetime.now().strftime("%Y%m%d%H%M%S")
        file = capture_path+id+ f"/{string_time}.jpg"
        cv2.imwrite(file, frame)
        cap.release()
        return 1, file

    except:
        print(f"lỗi xử lý capture")
        return 0, ""

# quay video
def record(id, link_rtsp):
    try:
        cap = cv2.VideoCapture(link_rtsp)
        # Check if the stream was successfully opened.
        if not cap.isOpened():
            print(f"Failed to open RTSP stream: {link_rtsp}")
            return 0, ""
        start_record = datetime.now()
        str_start_record = start_record.strftime("%Y%m%d%H%M%S")
        # Tạo một đối tượng VideoWriter để ghi đoạn cắt
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        video = record_path+id+"/"+ f"{str_start_record}.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if os.path.exists(record_path+id) == False:
            os.makedirs(record_path+id)
        writer = cv2.VideoWriter(video, fourcc, fps, (width, height))

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            now = datetime.now()
            if (now - start_record).total_seconds() >= 30:
                break
            writer.write(frame)
        cap.release()
        writer.release()

        return 1, ""
    except:
        print(f"lỗi xử lý quay video")
        return 0, ""
    
# record("cam1","rtsp://admin:BanRia123@banriaxatran.dssddns.net:5002/cam/realmonitor?channel=1&subtype=0")
# capture("cam1","20230816115105")
