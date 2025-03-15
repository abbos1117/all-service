import socket
import threading
import random
import string

FLAG = "HD{aylanib-aylanib-maqsadga-erishamiz!}"
MESSAGE_COUNT = 10
TIMEOUT = 15  # Soniyalar ichida

# Tasodifiy xabar generatsiyasi
def generate_random_message(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def handle_client(client_socket):
    try:
        client_socket.settimeout(TIMEOUT)
        for i in range(MESSAGE_COUNT):
            # Tasodifiy xabar yaratish
            message = generate_random_message()
            
            # Xabarni mijozga yuborish
            client_socket.sendall(message.encode())
            
            # Mijozdan xabarni qabul qilish
            client_response = client_socket.recv(1024).decode().strip()
            
            # Javobni tekshirish
            if client_response != message:
                client_socket.sendall(b"Xatolik: Noto'g'ri javob.")
                return
        
        # 11-xabarda flagni yuborish
        client_socket.sendall(FLAG.encode())
    except socket.timeout:
        client_socket.sendall(b"Xatolik: Vaqt tugadi.")
    except Exception as e:
        print(f"Xato yuz berdi: {e}")
    finally:
        client_socket.close()

def start_server(host='0.0.0.0', port=2000):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server {port}-portda ishga tushdi!")

    try:
        while True:
            client_socket, addr = server.accept()
            print(f"Mijoz ulandi: {addr}")
            # Har bir mijoz uchun alohida oqim
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()
    except KeyboardInterrupt:
        print("\nServer o'chirilmoqda...")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()

