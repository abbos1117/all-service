FROM ubuntu:20.04

ENV container docker
ENV DEBIAN_FRONTEND=noninteractive
USER root
#Paketlarni o‘rnatish
RUN apt-get update && apt-get install -y \
    python3 python3-venv python3-pip systemd systemd-sysv tzdata ufw nano vim \
    iproute2 net-tools iputils-ping bridge-utils iptables socat netcat telnet supervisor \
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

RUN chown -R root:root /home/secureuser #ADD
RUN chmod -R 755 /home/secureuser           #ADD
RUN chmod 750 /bin/su
RUN echo "umask 077" >> /home/secureuser/.bashrc
RUN find /home/secureuser -type f -exec chmod 700 {} \; 
RUN mkdir -p /app && chown secureuser:secureuser /app && chmod 700 /app
RUN usermod -d /app secureuser
RUN echo "cd /app" >> /home/secureuser/.bashrc

COPY server_2000.service server_2001.service server_2002.service \
     server_2003.service kali_server.service /etc/systemd/system/

RUN chown -R root:root /etc/systemd/system/  #ADD
RUN chmod  711 /etc/systemd/system/
# Virtual muhit yaratish va kutubxonalarni o‘rnatish
RUN python3 -m venv /home/secureuser/server_8080/env && \
    /home/secureuser/server_8080/env/bin/pip install --no-cache-dir -r /home/secureuser/server_8080/requirements.txt && \
    /home/secureuser/server_8080/env/bin/pip install scapy && \
     pip3 install --no-cache-dir scapy

# /sbin/init sozlash
RUN ln -sf /lib/systemd/systemd /sbin/init

# Systemd va XDG_RUNTIME_DIR sozlash
RUN echo "export XDG_RUNTIME_DIR=/run/user/0" >> /root/.bashrc

# Systemd ishlashi uchun kerakli konfiguratsiyalar
VOLUME [ "/sys/fs/cgroup" ]
STOPSIGNAL SIGRTMIN+3

RUN systemctl enable server_8080.service  server_2000.service server_2001.service \
                     server_2002.service  server_2003.service  kali_server.service

EXPOSE 2000 2001 2002 2003 8080 9876

# Systemd bilan ishga tushirish
ENTRYPOINT ["/sbin/init"]

RUN echo 'exec /bin/bash' >> /home/secureuser/.bashrc

WORKDIR /app
