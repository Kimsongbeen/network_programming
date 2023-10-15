import socket
import threading

# 서버 IP 주소 및 포트 번호 설정
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345

# 클라이언트 리스트
clients = []

# 서버 소켓 설정
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(5)

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
                client.send(message.encode('utf-8'))
            except Exception as e:
                print(e)


# 클라이언트 연결 수락
while True:
    client_socket, addr = server_socket.accept()
    clients.append(client_socket)
    print(f"클라이언트 {addr} 연결됨")

    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
