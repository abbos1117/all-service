#!/bin/bash
set -m  # Foreground va background jarayonlarni boshqarish

echo "Serverlarni ishga tushiryapman..."

# Har bir skriptni alohida log faylga yo‘naltirish va fonda ishlash
nohup python3 /home/secureuser/server_2000.py --port 2000 > /var/log/server_2000.log 2>&1 &
nohup python3 /home/secureuser/server_2001.py --port 2001 > /var/log/server_2001.log 2>&1 &
nohup python3 /home/secureuser/server_2002.py --port 2002 > /var/log/server_2002.log 2>&1 &
nohup python3 /home/secureuser/server_2003.py --port 2003 > /var/log/server_2003.log 2>&1 &
nohup python3 /home/secureuser/kali_server.py > /var/log/kali_server.log 2>&1 &

# Barcha jarayonlarning tugashini kutish
wait
