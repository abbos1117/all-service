import socket
import random

# Matematik savollarni yaratish
def generate_question():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operator = random.choice(['+', '*', '/'])
    
    # Savolni va to'g'ri javobni hisoblash
    if operator == '+':
        correct_answer = num1 + num2
    elif operator == '*':
        correct_answer = num1 * num2
    else:  # operator == '/'
        correct_answer = round(num1 / num2, 2)  # Floats with 2 decimal places
    
    question = f"{num1} {operator} {num2} = ?"
    return question, correct_answer

# Serverni ishga tushirish
def start_server(host='0.0.0.0', port=2003):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server {port}-portda ishlayapti...")

    flag = "HD{Siz-savol-javob-ustasisiz!}"

    try:
        while True:
            # Mijoz ulanishini kutish
            client_socket, addr = server.accept()
            print(f"Mijoz ulandi: {addr}")

            try:
                # Savollarni yuborish va tekshirish
                for _ in range(2):  # 5 ta savol so'raymiz
                    question, correct_answer = generate_question()
                    client_socket.sendall(question.encode())
                    print(f"Savol yuborildi: {question}")

                    # Mijozdan javobni olish
                    client_response = client_socket.recv(1024).decode().strip()

                    # Javobni tekshirish
                    try:
                        if float(client_response) == correct_answer:
                            print(f"Javob to'g'ri: {client_response}")
                        else:
                            print(f"Javob noto'g'ri: {client_response}")
                            client_socket.sendall(b"Xatolik: Noto'g'ri javob.")
                            client_socket.close()
                            print("Mijozdan noto'g'ri javob, ulanish uzildi.")
                            break  # Mijoz noto'g'ri javob berib, ulanishni uzamiz
                    except ValueError:
                        # Agar javob raqam bo'lmasa
                        print(f"Javob noto'g'ri: {client_response}")
                        client_socket.sendall(b"Xatolik: Noto'g'ri javob.")
                        client_socket.close()
                        print("Mijozdan noto'g'ri javob, ulanish uzildi.")
                        break  # Mijoz noto'g'ri javob berib, ulanishni uzamiz

                # To'g'ri javoblarni yuborib, flagni yuborish
                client_socket.sendall(flag.encode())
                print(f"Flag yuborildi: {flag}")

            except Exception as e:
                print(f"Xatolik yuz berdi: {e}")
            finally:
                client_socket.close()
                print("Mijoz bilan ulanish tugadi.")

    except KeyboardInterrupt:
        print("\nServer o'chirilmoqda...")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()

