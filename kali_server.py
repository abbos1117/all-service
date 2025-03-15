import socket
from scapy.all import *
import threading

# Flaglar
FLAG_1 = "HD{Ko'proq_flag_uchun_vaqt_keldi!}"
FLAG_2 = "HD{Nega...salom_sizga_ham_muhandis!}"
FLAG_3 = "HD{Hey!Sen-SSH-Kabi-Ko'rinmaysan?!}"

# Serverni sozlash
SERVER_IP = "0.0.0.0"  # Server IP manzili (o'zingizning IP manzilingizni yozing)
SERVER_PORT = 9876  # TCP paketi uchun port


def handle_packet(packet):
    """
    Paket kelganda uni tahlil qilish va flagni qaytarish.
    """
    try:
        # Faqat kerakli manzilga yuborilgan paketlarni ko'rib chiqamiz
        if not (IP in packet and packet[IP].dst == SERVER_IP):
            return None

        # 1-shart: TTL qiymati 99 bo'lgan IP paket
        if IP in packet and packet[IP].ttl == 99 and not packet[IP].payload:
            print(f"[+] TTL 99 sharti bajarildi, flag: {FLAG_1}")
            return FLAG_1

        # 2-shart: ICMP paketi "Hello, Haady!" ma'lumotini o'z ichiga olishi kerak
        if ICMP in packet and b"Hello, Haady!" in raw(packet[ICMP].payload):
            print(f"[+] ICMP sharti bajarildi, flag: {FLAG_2}")
            return FLAG_2

        # 3-shart: Manba porti 22 bo'lgan TCP ACK paketi
        if TCP in packet and packet[TCP].flags == "A" and packet[TCP].sport == 22 and packet[TCP].dport == SERVER_PORT:
            print(f"[+] TCP ACK sharti bajarildi, flag: {FLAG_3}")
            return FLAG_3

        # Hech qanday shart bajarilmadi
        return None

    except Exception as e:
        print(f"[!] Xatolik yuz berdi: {e}")
        return None


def start_server():
    """
    Serverni ishga tushiradi.
    """
    print(f"[+] Server {SERVER_IP}:{SERVER_PORT} da ishga tushirildi...")
    try:
        # Socket RAW rejimda
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        server_socket.bind((SERVER_IP, SERVER_PORT))

        while True:
            # Paketni qabul qilish
            packet_data, addr = server_socket.recvfrom(65535)

            # Paketni Scapy yordamida tahlil qilish
            packet = IP(packet_data)
            print(f"[+] Paket qabul qilindi: {packet.summary()}")

            # Paketni tahlil qilish va flagni qaytarish
            flag = handle_packet(packet)
            if flag:
                print(f"[+] Flag yuborildi: {flag}")

    except KeyboardInterrupt:
        print("\n[!] Server to'xtatildi.")
    except Exception as e:
        print(f"[!] Xatolik: {e}")
    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server()
