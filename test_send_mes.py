
import zmq
import json

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5555")

#  Do 10 requests, waiting each time for a response

# data = {
#     "type":3,
#     "data": {
#         "id":"id1",
#         "station_camera_id":"cam1",
#         "time":"20230817115105"
#     }
# }
data = {
    "type":0,
    "data": {
        "station_camera_id":"cam2",
        "link_rtsp":"link1"
    }
}
print(json.dumps(data))
socket.send(json.dumps(data).encode("utf-8"))

#  Get the reply.
message = socket.recv()
print("--------------------------")
print(message)