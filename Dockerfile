FROM ubuntu:20.04

ENV container docker
ENV DEBIAN_FRONTEND=noninteractive

# Root userda ishlash
USER root

# Paketlarni o‘rnatish
RUN apt-get update && apt-get install -y \
    python3 python3-venv python3-pip systemd systemd-sysv tzdata ufw nano vim \
    iproute2 net-tools iputils-ping bridge-utils iptables socat netcat supervisor \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Tizim vaqtini avtomatik sozlash
RUN ln -fs /usr/share/zoneinfo/Etc/UTC /etc/localtime && dpkg-reconfigure --frontend noninteractive tzdata

# Systemd konfiguratsiyasi
RUN mkdir -p /run/systemd /run/lock 

# secureuser foydalanuvchisini yaratish
RUN useradd -m -d /home/secureuser -s /bin/bash secureuser

# Fayllarni nusxalash va ruxsat berish
COPY --chown=secureuser:secureuser server_8080 /home/secureuser/server_8080
COPY --chown=secureuser:secureuser server_2000.py server_2001.py server_2002.py server_2003.py /home/secureuser/
COPY --chown=secureuser:secureuser client_2004 /home/secureuser/client_2004
COPY --chown=secureuser:secureuser kali_server.py /home/secureuser/kali_server.py
COPY server_8080.service /etc/systemd/system/server_8080.service

COPY server_2000.service /etc/systemd/system/server_2000.service
COPY server_2001.service /etc/systemd/system/server_2001.service
COPY server_2002.service /etc/systemd/system/server_2002.service
COPY server_2003.service /etc/systemd/system/server_2003.service
COPY kali_server.service /etc/systemd/system/kali_server.service

# Skriptni nusxalash va bajarish huquqini berish
COPY start_servers.sh /home/secureuser/start_servers.sh
RUN chown secureuser:secureuser /home/secureuser/start_servers.sh
RUN chmod +x /home/secureuser/start_servers.sh

# Fayllarga ruxsat berish
RUN chmod -R 750 /home/secureuser && \
    find /home/secureuser -type f -exec chmod 640 {} \; && \
    chmod 644 /etc/systemd/system/server_8080.service

# Virtual muhit yaratish va kutubxonalarni o‘rnatish
RUN python3 -m venv /home/secureuser/server_8080/env && \
    /home/secureuser/server_8080/env/bin/pip install --no-cache-dir -r /home/secureuser/server_8080/requirements.txt && \
    /home/secureuser/server_8080/env/bin/pip install scapy

RUN pip3 install --no-cache-dir scapy

# /sbin/init sozlash
RUN ln -sf /lib/systemd/systemd /sbin/init

# Systemd va XDG_RUNTIME_DIR sozlash
RUN echo "export XDG_RUNTIME_DIR=/run/user/0" >> /root/.bashrc

# Systemd ishlashi uchun kerakli konfiguratsiyalar
VOLUME [ "/sys/fs/cgroup" ]
STOPSIGNAL SIGRTMIN+3

RUN systemctl enable server_8080.service

RUN systemctl enable server_2000.service
RUN systemctl enable server_2001.service
RUN systemctl enable server_2002.service
RUN systemctl enable server_2003.service
RUN systemctl enable kali_server.service
# Portlarni ochish
EXPOSE 2000 2001 2002 2003 8080 9876

# Systemd bilan ishga tushirish
ENTRYPOINT ["/sbin/init"]
#CMD ["/bin/bash", "-c", "/home/secureuser/start_servers.sh && exec /sbin/init"]
#CMD ["/bin/bash", "-c", "chmod +x /home/secureuser/start_servers.sh && /home/secureuser/start_servers.sh && exec /sbin/init"]
#CMD /bin/bash -c "/home/secureuser/start_servers.sh && exec /sbin/init"
