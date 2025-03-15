import socket
import random
import time


# Flagni qismlarga bo'lish
def generate_flag_part(flag):
    part_size = random.choice([1, 2])  # Flag qismlarini 1 yoki 2 belgi qilib yuborish
    return flag[:part_size]


def start_server(host='0.0.0.0', port=2002):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server {port}-portda ishlayapti...")

    flag = "HD{Bu-flagning-belgilangan-uzunligi-yo'q!}"
    current_pos = 0  # Flag yuborilgan qismni kuzatib borish uchun o'zgaruvchi

    try:
        while True:
            # Mijoz ulanishini kutish
            client_socket, addr = server.accept()
            print(f"Mijoz ulandi: {addr}")

            try:
                # Mijozga flagni yuborish
                while current_pos < len(flag):
                    # Tasodifiy uzilish hosil qilish (50% ehtimol)
                    if random.random() < 0.5:
                        print(f"UZILISH: Flag yuborilmadi.")
                        time.sleep(random.uniform(0.1, 1))  # Kechikish va keyin davom etish
                        continue

                    # Flag qismini yuborish
                    flag_part = generate_flag_part(flag[current_pos:])
                    client_socket.sendall(flag_part.encode())
                    print(f"Flag qismi yuborildi: {flag_part}")

                    # Yuborilgan qismini saqlab qo'yish
                    current_pos += len(flag_part)

                # Flagni to'liq yuborgandan keyin mijozga habar yuborish

                print(f"Flagning barcha qismlari yuborildi.")
                current_pos=0
            except Exception as e:
                print(f"Xatolik yuz berdi: {e}")
            finally:
                client_socket.close()

    except KeyboardInterrupt:
        print("\nServer o'chirilmoqda...")
    finally:
        server.close()


if __name__ == "__main__":
    start_server()

