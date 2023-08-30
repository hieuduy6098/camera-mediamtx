import yaml
import os
from config import *

# đọc file yml
def read_yaml_file():
  """Reads a .yml file and returns the contents as a Python dictionary."""
  try:
    # kiem tra duong dan co ton tai ko
    if os.path.exists(mediamtx_path) == False:
      print(f"file mediamtx {mediamtx_path} không tồn tại")
      return None

    with open(mediamtx_path, "r") as f:
      data = yaml.safe_load(f)

    return data
  except:
    print(f"lỗi đọc file {mediamtx_path}")
    return None

# ghi file yml
def write_yaml_file(data):
  """Writes the contents of a Python dictionary to a .yml file."""
  try:
    # kiem tra duong dan co ton tai ko
    if os.path.exists(mediamtx_path):
      with open(mediamtx_path, "w") as f:
        yaml.dump(data, f, allow_unicode=True,sort_keys=False, default_flow_style=False)

    else:
      print(f"file mediamtx {mediamtx_path} không tồn tại")

  except:
    print(f"lỗi ghi data vào file {mediamtx_path}")

# thêm
def add_camera(id, link_rtsp):
  try:
    # lấy dữ liệu file yml
    yml_data = read_yaml_file()

    # không lấy được dữ liệu -> status = 0
    if yml_data == None:
      return 0

    cameras = yml_data["paths"]
    
    # tạo đường dẫn thư mục output cho video
    camera_output_path = source_path + f"{id}/"

    if os.path.exists(camera_output_path) == False:
      print(f"file {id} không tồn tại -> tạo mới thư mục: {id}")
      os.makedirs(camera_output_path)

    # thêm camera vào file yml
    camera_element = {
      "source": link_rtsp,
      # "runOnInit": f"ffmpeg -rtsp_transport tcp -i {link_rtsp} -c:v copy -f segment -segment_time {segment_time} -segment_format mp4 -strftime 1 -reset_timestamps 1 {source_path}{id}/%Y%m%d%H%M%S.mp4",
      # "runOnInitRestart": True,
      "sourceProtocol": "tcp",
    }
    
    cameras.update({id:camera_element})
    yml_data["paths"] = cameras

    # update file yml
    write_yaml_file(yml_data)

    # thêm camera xong trả trạng thái 1
    return 1
  except:
    # nếu lỗi trả trạng thái 0
    return 0
  
# sửa camera
def update_camera(id, link_rtsp):
  try:
    # lay du lieu file yml
    yml_data = read_yaml_file()

    # ko lay dc du lieu tra trang thai = 0
    if yml_data == None:
      return 0
    
    # kiem tra id co ton tai khong neu co thi cap nhat
    cameras = yml_data["paths"]
    if (cameras == None) or (id not in cameras):
      print(f"camera id: {id} chưa được cấu hình trên file yml")
      return 3
    
    camera_element = {
      "source": link_rtsp,
      # "runOnInit": f"ffmpeg -rtsp_transport tcp -i {link_rtsp} -c:v copy -f segment -segment_time {segment_time} -segment_format mp4 -strftime 1 -reset_timestamps 1 {source_path}{id}/%Y%m%d%H%M%S.mp4",
      # "runOnInitRestart": True,
      "sourceProtocol": "tcp",
    }
    cameras[f"{id}"] = camera_element
    yml_data["paths"] = cameras

    # update file yml
    write_yaml_file(yml_data)

    return 1
  
  except:
    print("loi trong qua trinh update camera")
    return 0  

# xoa camera
def delete_camera(id):
  try:
    # lay du lieu file yml
    yml_data = read_yaml_file()

    # ko lay dc du lieu tra trang thai = 0
    if yml_data == None:
      return 0
    
    # kiem tra xem id co ton tai hay khong
    cameras = yml_data["paths"]
    if (cameras == None) or (id not in cameras):
      return 3
    # xoa camera
    cameras.pop(id)
    yml_data["paths"] = cameras
    # update file yml
    write_yaml_file(yml_data)
    return 1

  except:
    print(f"loi trong qua trinh xoa camera: {id}")
    return 0

# tra ve cac camera dc cau hinh tren server
def get_all_camera():
  try:
    # lay du lieu file yml
    yml_data = read_yaml_file()
    
    # ko lay dc du lieu tra trang thai = 0
    if yml_data == None:
      return 0
    
    # kiem tra 
    cameras = yml_data["paths"]
    
    if cameras == None or len(cameras) == 0:
      return None

    list_id = [key for key in cameras.keys()]
    string_list_id = ",".join(list_id)
    
    # tra ve string la list cac id cam ngan cach bang dau ","
    return string_list_id

  except:
    print(f"loi trong qua trinh lay camera")
    return None
  

# print(get_all_camera())   
# add_camera("cam1", "rtsp://admin:Deahan123@117.2.46.10:664/Streaming/Channels/101/")
# update_camera("cam1", "rtsp://admin:Deahan123@117.2.46.10:664/Streaming/Channels/101/")
# delete_camera("cam1", "rtsp://admin:Deahan123@117.2.46.10:664/Streaming/Channels/101/")
