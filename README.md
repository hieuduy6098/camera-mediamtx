# camera-mediamtx
python 3.9

# example message: them, sua, xoa, lay tat ca cac camera
## 0: them, 1: sua, 2:xoa, 3:lay tat ca cac camera id

{
    "type_message":0
    "data": {
        "station_camera_id":"string"
        "link_rtsp":"string"
    }
}

neu lay tat ca cac camera id
{
    "type_message":3
    "data": null
}

---------------------------------------

# chup anh, quay video
## 4: chup anh, 5 quay video
example
{
    "type_message":4
    "data": {
        "id":"string"
        "station_camera_id":"string"
        "time": "20230808110000" 
    }
}   