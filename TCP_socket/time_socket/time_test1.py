#time_client.py
import socket
import time

while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = ("localhost", 5000)
    sock.connect(address)   #서버에 연결
    time.sleep(1)
    print("현재 시각: ", sock.recv(1024).decode())  #수신 내용을 문자열로 변환하여 출력