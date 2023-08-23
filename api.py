import requests
import json

# Hàm lấy token
def getToken():
    try:
        # url get token
        url = f"http://192.168.91.132:6969/api/generate-token?grantType=CLIENT_CREDENTIAL&appId=DATALOGGER_TNN&secret=7c67bd94-3d70-11ed-b878-0242ac120002"
        # lấy access token
        response = requests.get(url)
        # convert string to dict
        data = json.loads(response.text)
        access_token = data['data']['accessToken']
        return access_token
    except:
        print("lỗi lấy token")
        return None


def update_capture(id, path, status):
    try:
        # lấy token
        accessToken = getToken()
        if accessToken is None:
            return
        # get url
        authorization = f"Bearer {accessToken}"
        # tao request body 
        body = {
            "id": id,
            "path": path,
            "status": status
        }
        requestUrl = "http://192.168.91.132:9000/api/cameras/camera-captures/response"
        response = requests.put(requestUrl, json=body, headers={'Authorization': authorization})

        # Check the status code
        if response.status_code == 200:
            print("cap nhat capture thanh cong")
        else:
            print("cap nhat capture that bai")
    except:
        print("loi cap nhat capture")

def update_record(id, path, status):
    try:
        # lấy token
        accessToken = getToken()
        if accessToken is None:
            return
        # get url
        authorization = f"Bearer {accessToken}"
        # tao request body 
        body = {
            "id": id,
            "path": path,
            "status": status
        }
        requestUrl = "http://192.168.91.132:9000/api/cameras/camera-records/response"
        response = requests.put(requestUrl, json=body, headers={'Authorization': authorization})

        # Check the status code
        if response.status_code == 200:
            print("cap nhat record thanh cong")
        else:
            print("cap nhat record that bai")
    except:
        print("loi cap nhat record")