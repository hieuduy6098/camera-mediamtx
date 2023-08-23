import cv2
import os
import time
from config import *

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
def capture(id, string_time):
    try:
        # Đường dẫn folder các video lưu lâu dài của camera
        input_video = source_path + id
        # kiểm tra xem đường đãn tồn tại ko, nếu không có -> 2
        if os.path.exists(input_video) == False:
            print(f"đường dẫn {input_video} không tồn tại")
            return 2, ""
        # lấy tất cả các file video trong đường đẫn, nếu ko có gì -> 3
        files = os.listdir(input_video)
        if len(files) == 0:
            return 3, ""
        # kiểm tra video cuối cùng có thời gian lớn hơn thời gian chụp không, nếu ko -> sleep đợi video mới
        files.sort(reverse=True)
        if int(files[0][0:14]) < int(string_time):
            if record_time > segment_time:
                print(f"chưa có video để capture -> sleep {record_time}s")
                time.sleep(record_time+10)
            print(f"chưa có video để capture -> sleep {segment_time}s")
            time.sleep(segment_time+10)

            # lấy tất cả các file video trong đường đẫn
            files = os.listdir(input_video)
        # lấy file video cần capture
        list_file = [file for file in files if int(file[0:14]) - int(string_time) <= 0]
        list_file.sort(reverse=True)
        video_name = list_file[0]
            
        cap = cv2.VideoCapture(source_path+id+"/"+video_name)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(frame_count/segment_time)
        time_of_video = int(frame_count/fps)
        # xác định thời gian lấy ảnh
        time_of_frame =  int(string_time) - int(video_name[0:14])
        # set vị trí frame ảnh
        cap.set(cv2.CAP_PROP_POS_FRAMES, time_of_frame*fps)
        ret, frame = cap.read()
        # kiểm tra đường dẫn output tồn tại chưa, nếu chưa -> tạo
        if os.path.exists(capture_path+id) == False:
            os.makedirs(capture_path+id)
        # Lưu frame dưới dạng JPG
        file = capture_path+id+ f"/{string_time}.jpg"
        cv2.imwrite(file, frame)
        cap.release()
        return 1, file
    except:
        print(f"lỗi xử lý capture")
        return 0, ""

# quay video
def record(id, string_time):
    try:
        # Đường dẫn folder các video lưu lâu dài của camera
        input_video = source_path + id
        # kiểm tra xem đường đãn tồn tại ko, nếu không có -> 2
        if os.path.exists(input_video) == False:
            print(f"duong dan {input_video} khong ton tai")
            return 2, ""
        
        # kiểm tra dường dẫn video output tồn tại chưa, nếu chưa -> tạo
        if os.path.exists(record_path + id) == False:
            os.makedirs(record_path + id)

        # lấy tất cả các file video trong đường đẫn, nếu ko có gì -> 3
        files = os.listdir(input_video)
        if len(files) == 0:
            return 3, ""
        
        # kiểm tra video cuối cùng có thời gian lớn hơn thời gian chụp không, nếu ko -> sleep đợi video mới
        files.sort(reverse=True)
        if int(files[0][0:14]) < int(string_time):
            if record_time > segment_time:
                print(f"chua co video de record -> doi {record_time}s")
                time.sleep(record_time+10)
            print(f"chua co video de record -> doi {segment_time}s")
            time.sleep(segment_time+10)

            # lấy tất cả các file video trong đường đẫn
            files = os.listdir(input_video)
        # trả về 2 video gần thời gian cần lấy nhất
        list_file_before = [file for file in files if int(file[0:14]) - int(string_time) <= 0]
        list_file_after = [file for file in files if int(file[0:14]) - int(string_time) >= 0]
        list_file_before.sort(reverse=True)
        list_file_after.sort(reverse=False)
        file_before = list_file_before[0]
        file_after = list_file_after[0]

        # nếu giống nhau -> move file sang output không cần xử lý
        if file_before == file_after:
            from_file = input_video+f"/{file_before}"
            file = record_path+id+f"/{file_before}"
            os.rename(from_file, file)
            return 1, file
        # đọc video
        cap1 = cv2.VideoCapture(source_path+id + "/" + file_before)
        cap2 = cv2.VideoCapture(source_path+id + "/" + file_after)
        # lấy frame ảnh
        frame_count_1 = int(cap1.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_count_2 = int(cap1.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(frame_count_1/segment_time)
        # xác định thời gian lấy ảnh
        time_of_frame =  int(string_time) - int(file_before[0:14])
        # set vị trí frame bắt đầu lấy ảnh
        cap1.set(cv2.CAP_PROP_POS_FRAMES, time_of_frame*fps)

        # Tạo một đối tượng VideoWriter để ghi đoạn cắt
        video = record_path+id+"/"+ f"{string_time}.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        width  = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
        writer = cv2.VideoWriter(video, fourcc, fps, (width, height))

        while True:
            # Đọc khung ảnh
            ret, frame = cap1.read()

            # Nếu không còn khung hình nào, thì thoát khỏi vòng lặp
            if not ret:
                break

            writer.write(frame)
        for i in range(0,time_of_frame*fps):
            # Đọc khung ảnh
            ret, frame = cap2.read()

            # Nếu không còn khung hình nào, thì thoát khỏi vòng lặp
            if not ret:
                break

            writer.write(frame)

        # Đóng các đối tượng VideoCapture và VideoWriter
        cap1.release()
        cap2.release()
        writer.release()

        return 1, video
    except:
        print(f"lỗi xử lý quay video")
        return 0, ""
    
# record("cam1","20230816114858")
# capture("cam1","20230816115105")
