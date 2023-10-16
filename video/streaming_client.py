import tkinter as tk
import threading
import cv2
import socket
import numpy as np
from PIL import Image, ImageTk

# 서버 IP 주소 및 포트 번호
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345

# GUI 생성
root = tk.Tk()
root.title("Video Streaming Client")

# 비디오 프레임 표시
frame = tk.Label(root)
frame.pack()

# 채팅 창
chat_text = tk.Text(root, state=tk.DISABLED)
chat_text.pack()

# 클라이언트 소켓 설정
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 메시지 전송 함수
def send_message():
    message = entry.get()
    client_socket.sendall(message.encode())
    entry.delete(0, tk.END)


# 서버로부터 비디오 스트리밍을 받아 화면에 표시하는 함수
def receive_video_stream(frame_label=None):
    while True:
        try:
            img_bytes = client_socket.recv(1024)
            img_encoded = np.frombuffer(img_bytes, dtype=np.uint8)
            frame = cv2.imdecode(img_encoded, cv2.IMREAD_COLOR)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            frame_label.config(image=photo)
            frame_label.image = photo
        except Exception as e:
            print(e)
            break


# 메시지 수신 함수
def receive_message():
    while True:
        try:
            message = client_socket.recvfrom(1024).decode('utf-8')
            chat_text.config(state=tk.NORMAL)
            chat_text.insert(tk.END, message + "\n")
            chat_text.config(state=tk.DISABLED)
        except Exception as e:
            print(e)
            break

# 전송 버튼
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

# 비디오 수신 스레드 시작
video_thread = threading.Thread(target=receive_video_stream)
video_thread.daemon = True
video_thread.start()

# 메시지 수신 스레드 시작
message_thread = threading.Thread(target=receive_message)
message_thread.daemon = True
message_thread.start()

# 채팅 입력 상자
entry = tk.Entry(root, width=30)
entry.pack()


# GUI 시작
root.mainloop()

# 연결 종료 시 스레드 및 소켓 닫기
client_socket.close()
