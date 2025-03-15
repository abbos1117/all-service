# **13. Network Scripting.**

- **13.1.2  Socket Methods**
    1. `server_2000.py`  fayl ishlatib qo’yish kerak bu 2000 partda ishlaydi falag beradigan kod (`python3 server_2000.py`) qilib ishga tushirilishi kerak bu doim ishlab turishi kerak
- **13.2.1  Error Handling:Try and Except Clauses**
    
    1.`server_2001.py`  fayl ishlatib qo’yish kerak bu 2001 partda ishlaydi falag beradigan kod (`python3 server_2001.py`) qilib ishga tushirilishi kerak bu doim ishlab turishi kerak
    
- **13.2.2 Handling Unknown Data Size**
    
    1.`server_2002.py`  fayl ishlatib qo’yish kerak bu 2002 partda ishlaydi falag beradigan kod (`python3 server_2002.py`) qilib ishga tushirilishi kerak bu doim ishlab turishi kerak
    
- **13.2.3 Interactive Sockets**
    
    1.`server_2003.py`  fayl ishlatib qo’yish kerak bu 2003 partda ishlaydi falag beradigan kod (`python3 server_2003.py`) qilib ishga tushirilishi kerak bu doim ishlab turishi kerak
    
- **13.3.2 Testing our Client and Server**
    1. root:root user yaratilishi kerak va root/ ichdida `client_2004` binary faylni joylash krak
- **3.4.1 Using the Socket Module to Create a Port Scanner**
    
    !! Server yaratilganda qilish kerak bulgan ctf
    
- **13.4.2 Port Knocking**
    
    !! Server yaratilganda qilish kerak bulgan ctf
    
- **13.5.2. The Application Layer: GET Requests with Python dan 13.6.2. Request Header and Non-Text-based Content bitada yig’ilgan**
    
    server_8080 to’liq ko’chirilsin 
    
    ishga tushirish tartibi
    
    1.qadam loyihani tayyorlash
    
    ```bash
    # 1.server_8080 papkaga kirib olish
    cd server_8080
    
    #2.vertual muhut yaratish
    python3 -m venv env
    #3.muhutni aktivlashtirish
    source env/bin/activate 
    
    #4.kerakli ktubxonalarni urnatish
    pip install -r requirements.txt
    
    ```
    
    loyiha doim ishlab turishi uchun serves fayl yaratilishi kerak
    
    2.qama service faylni yaratish va tayyorlash
    
    ```bash
    #1.service fayl yaratib olish kerak
    sudo nano /etc/systemd/system/ server_8080.service
    
    #2.service fayl ichida quydagilar bulishi kerak
    
    [Service]
    User=ubuntu #userni nomi
    WorkingDirectory=/home/ubuntu/server_8080 # server_8080 papkasi joylashuvi va <WorkingDirectory>  urniga ham shunday jotylashuvlar quyilishi kerak
    ExecStart=<WorkingDirectory>/env/bin/python3 <WorkingDirectory>/manage.py runserver 0.0.0.0:8080
    Restart=always
    # replace /home/user/.virtualenv/bin/python with your virtualenv and main.py with your script
    
    [Install]
    WantedBy=multi-user.target
    
    ```
    
    3.qadam service falni ishga tushirish
    
    ```bash
    #1.service faylni ishga tushirish
    sudo systemctl start server_8080.service
    #2.service faylni holatini ko'rish xatolik bulsa ishlammaydi
    sudo systemctl satus server_8080.service
    #3.service faylni doim ishlab turishi uchun enabled qilish
    sudo systemctl enabled server_8080.service
    ```
    
- **13.7.7. Sending and Receiving a Response from Scapy**
    
    serverga scapy urnatish kerak bu siz ishlamaydi bu bulimni ctf lari
    
    ```bash
    pip install scapy
    ```
    
    `kali_server.py`  fayl root qismiga quygan yaxshi bu flaglarni beradi va `9876` porti Allow qilinishi kerak 
    
    ```bash
    sudo ufw allow from 0.0.0.0 to any port 9876
    
    ```
    
    kodni ishga tushirish (`sudo python3 kali_server.py`) doim ishlab turishi  taminlanishi kerak yoki yuqoridagiday `service` fayl yozilishi kerak