import socket
import threading
import random
import string  # Bu qatorni qo'shish kerak
import time

FLAG = "HD{Try-va-except-pitch-va-catch-ga-o'xshaydi,-biri-xatolikni-ushlab-qoladi,-biri-esa-qabul-qiladi}"
MESSAGE_COUNT = 10
TIMEOUT = 15  # Soniyalar ichida

# Uzilishlarni vaqti haqida global ma'lumot
disconnects = 0
start_time = None
end_time = None

# Tasodifiy xabar generatsiyasi
def generate_random_message(length=8):
    return ''.join(random.choices(string.ascii_letters + string.ascii_lowercase + string.digits, k=length))

def handle_client(client_socket):
    global disconnects

    try:
        client_socket.settimeout(TIMEOUT)
        successful_messages = 0
        client_start_time = time.time()

        while successful_messages < MESSAGE_COUNT:
            # Agar 15 soniya o'tgan bo'lsa, xatolik yuboring
            if time.time() - client_start_time > TIMEOUT:
                client_socket.sendall(b"Xatolik: 15 soniya ichida 10 ta javob olishning imkoni bo'lmadi.")
                print("Xatolik: Vaqt tugadi!")
                return

            # Server uzilishlarni yaratadi (70% ehtimol bilan xabar yubormaydi)
            if random.random() < 0.7:
                disconnects += 1
                print(f"UZILISH: Server xabar yubormadi.")
                time.sleep(random.uniform(0.1, 0.5))  # Kechikish
                continue
            
            # Tasodifiy xabar yaratish
            message = generate_random_message()
            client_socket.sendall(message.encode())
            print(f"Yuborildi: {message}")

            try:
                # Mijozdan javobni qabul qilish
                client_response = client_socket.recv(1024).decode().strip()
                print(f"Mijozdan qabul qilindi: {client_response}")
                if client_response == message:
                    successful_messages += 1
                else:
                    client_socket.sendall(b"Xatolik: noto'g'ri javob.")
                    return
            except socket.timeout:
                print("Xato: mijoz javob bermadi (timeout).")
                client_socket.sendall(b"Xatolik: vaqt tugadi.")
                return

        # Flag yuborish
        client_socket.sendall(FLAG.encode())
        print(f"Muvaffaqiyat! Flag yuborildi: {FLAG}")
        client_end_time = time.time()
        print(f"Mijoz uchun sarflangan vaqt: {client_end_time - client_start_time:.2f} soniya.")
    except Exception as e:
        print(f"Xato yuz berdi: {e}")
    finally:
        client_socket.close()

def start_server(host='0.0.0.0', port=2001):
    global start_time, end_time

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server {port}-portda ishga tushdi!")
    start_time = time.time()

    try:
        while True:
            client_socket, addr = server.accept()
            print(f"Mijoz ulandi: {addr}")
            # Har bir mijoz uchun alohida oqim
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()
    except KeyboardInterrupt:
        end_time = time.time()
        print("\nServer o'chirilmoqda...")
        total_time = end_time - start_time
        print(f"Server umumiy ishlagan vaqt: {total_time:.2f} soniya.")
        print(f"Umumiy uzilishlar soni: {disconnects}")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()

