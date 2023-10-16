import tkinter as tk
import cv2
from PIL import Image, ImageTk
import socket
import threading

# 서버 IP 주소 및 포트 번호 설정
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345

# 화면 갱신 함수
def update():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        label.config(image=photo)
        label.image = photo
    window.after(10, update)


# 메시지 보내기 함수
def send_message():
    message = entry.get()
    chat_text.config(state=tk.NORMAL)
    chat_text.insert(tk.END, "나: " + message + "\n")
    chat_text.config(state=tk.DISABLED)
    entry.delete(0, tk.END)


# GUI 초기화
window = tk.Tk()
window.title("화상 채팅 서버")

# 웹캠 초기화
cap = cv2.VideoCapture(0)

# 라벨 위젯을 사용 하여 영상 표시 (80%)
label = tk.Label(window, text="0")
label.grid(row=0, column=0, padx=10, pady=10, rowspan=2, sticky="nsew")

# 채팅 창 (Text 위젯) 추가 (20%)
chat_text = tk.Text(window, wrap=tk.WORD, state=tk.DISABLED)
chat_text.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# 메시지 입력 필드 (20%)
entry = tk.Entry(window)
entry.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# 메시지 보내기 버튼 (20%)
send_button = tk.Button(window, text="보내기", command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10, sticky="se")

# 행 및 열 가중치 설정
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=4)  # 비디오 화면이 80% 차지
window.grid_columnconfigure(1, weight=1)  # 채팅 창이 20% 차지

# 갱신 함수 호출
update()

# GUI 시작
window.mainloop()

# 클라이언트 리스트
clients = []

# 서버 소켓 설정
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((SERVER_IP, SERVER_PORT))
server_sock.listen(5)

print("서버 대기 중...")

# 클라이언트 연결 처리 함수
def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"받은 메시지: {message}")
            broadcast(message, client_socket)
        except Exception as e:
            print(e)
            break

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except Exception as e:
                print(e)


# 클라이언트 연결 수락
while True:
    client_socket, addr = server_sock.accept()
    clients.append(client_socket)
    print(f"클라이언트 {addr} 연결됨")

    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()

# 웹캠 해제
cap.release()
