import json
import zmq
import threading

from config import *
from yml_process import *
from video_process import capture, record
from api import update_capture, update_record

def main():
    # tao pool luu cac message 
    messages_pool = []
    # tao socket server
    context = zmq.Context()
    socket = context.socket(zmq.REP) # tcp
    print(f"socket server listen in {url}")
    socket.bind(url)
    # tạo zeromq server
    server = threading.Thread(target=listen_message, args=(socket,messages_pool,), daemon=True)
    server.start()

    while True:
        try:
            if len(messages_pool) != 0:
                message = messages_pool.pop(0)
                # xu ly goi tin
                type_message = message['type']
                id = message['data']["id"]
                station_camera_id = message['data']["station_camera_id"]
                time = message['data']["time"]
                if type_message == 3:
                    capture = threading.Thread(target=capture_process, args=(id, station_camera_id,time,))
                    capture.start()
                    capture.join()
                    print("capture xong")
                if type_message == 4:
                    record = threading.Thread(target=record_process, args=(id, station_camera_id,time,))
                    record.start()
                    record.join()
                    print("record xong")
                    
        except:
            print("loi xu ly cac thread")
            break
    socket.close()
    context.term()

# tạo zeromq server
def listen_message(socket, messages_pool):

    while True:
        try:
            #  doi tin nhan tu client
            message = socket.recv()

            # convert message
            data_message = convert_message(message)
            
            # xu ly goi tin
            type_message = data_message['type']
            data = data_message['data']

            status = "0"
            
            if type_message==0:
                # them moi
                station_camera_id = data["station_camera_id"]
                link_rtsp = data["link_rtsp"]
                status = add_camera(id=station_camera_id,link_rtsp=link_rtsp)
            
            elif type_message==1:
                # sua 
                station_camera_id = data["station_camera_id"]
                link_rtsp = data["link_rtsp"]
                status = update_camera(id=station_camera_id,link_rtsp=link_rtsp)

            elif type_message==2:
                # xoa
                station_camera_id = data["station_camera_id"]
                status = delete_camera(id=station_camera_id)
                
            elif type_message == 3:
                # chup anh
                messages_pool.append(data_message)
                status = 1
            
            elif type_message == 4:
                # quay video
                messages_pool.append(data_message)
                status = 1

            else:
                print(f"type_message = {type_message} khong phu hop")

            # gui trang thai ve client
            socket.send(str(status).encode())

        except:
            print("loi nhan message zeroMQ -> dung server")
            status = "0"
            socket.send(status.encode())
            break
    print("dong socket server")
    socket.close()

# xu ly record
def capture_process(id, station_camera_id, time):
    status, path = capture(station_camera_id, time)
    update_capture(id,path,status)

# xu ly capture
def record_process(id, station_camera_id, time):
    status, path = record(station_camera_id, time)
    update_record(id,path,status)

# convert message tu byte -> dict
def convert_message(byte_message):
    try:
        json_string = byte_message.decode("utf-8")
        json_object = json.loads(json_string)
        return json_object
    except:
        print("loi convert byte message -> dict")
        return ""

if __name__ == "__main__":
    main()