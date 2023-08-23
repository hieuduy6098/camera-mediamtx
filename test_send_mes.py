
import zmq
import json

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5555")

#  Do 10 requests, waiting each time for a response

data = {
    "type":4,
    "data": {
        "id":"e1e70e9f-3667-41ba-863a-b6473090563a",
        "station_camera_id":"80aebd2b-11c5-471f-8b30-7316ab35dadb",
        "time":"20230823153950"
    }
}
# data = {
#     "type":0,
#     "data": {
#         "station_camera_id":"cam2",
#         "link_rtsp":"link1"
#     }
# }
print(json.dumps(data))
socket.send(json.dumps(data).encode("utf-8"))

#  Get the reply.
message = socket.recv()
print("--------------------------")
print(message)