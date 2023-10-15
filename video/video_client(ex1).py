import socket
import tkinter as tk
import threading

# 서버 IP 주소 및 포트 번호 설정
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345

# 클라이언트 소켓 설정
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

# GUI 생성
root = tk.Tk()
root.title("채팅 클라이언트")

# 채팅 창
chat_text = tk.Text(root, state=tk.DISABLED)
chat_text.pack()

# 채팅 입력 상자
entry = tk.Entry(root, width=50)
entry.pack()

# 메시지 전송 함수
def send_message():
    message = entry.get()
    if message:
        client_socket.send(message.encode('utf-8'))
        entry.delete(0, tk.END)

# 전송 버튼
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

# 메시지 수신 함수
def receive_message():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            chat_text.config(state=tk.NORMAL)
            chat_text.insert(tk.END, message + "\n")
            chat_text.config(state=tk.DISABLED)
        except Exception as e:
            print(e)
            break

# 메시지 수신 스레드 시작
message_thread = threading.Thread(target=receive_message)
message_thread.daemon = True
message_thread.start()

# GUI 시작
root.mainloop()

