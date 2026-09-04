FutbolX Media Server

A self-hosted media streaming server built with FastAPI, FFmpeg, HLS, Nginx, and a web dashboard.

This guide is designed so that FutbolX can be installed from scratch on a new VPS without needing to remember the previous setup.

---

Table of Contents

1. "What FutbolX Does" (#1-what-futbolx-does)
2. "VPS Requirements" (#2-vps-requirements)
3. "Fresh VPS Preparation" (#3-fresh-vps-preparation)
4. "Install Required Software" (#4-install-required-software)
5. "Install Git" (#5-install-git)
6. "Install Python" (#6-install-python)
7. "Install FFmpeg" (#7-install-ffmpeg)
8. "Install Nginx" (#8-install-nginx)
9. "Install Certbot" (#9-install-certbot)
10. "Clone FutbolX" (#10-clone-futbolx)
11. "Create Required Directories" (#11-create-required-directories)
12. "Create Python Virtual Environment" (#12-create-python-virtual-environment)
13. "Install Python Dependencies" (#13-install-python-dependencies)
14. "Test FutbolX Manually" (#14-test-futbolx-manually)
15. "Configure Nginx" (#15-configure-nginx)
16. "Configure DNS" (#16-configure-dns)
17. "Create Systemd Service" (#17-create-systemd-service)
18. "Start FutbolX" (#18-start-futbolx)
19. "Configure Firewall" (#19-configure-firewall)
20. "Configure HTTPS / SSL" (#20-configure-https--ssl)
21. "Verify Installation" (#21-verify-installation)
22. "Using the Dashboard" (#22-using-the-dashboard)
23. "Creating a Live Stream" (#23-creating-a-live-stream)
24. "Scheduling a Stream" (#24-scheduling-a-stream)
25. "Starting a Scheduled Stream" (#25-starting-a-scheduled-stream)
26. "Stopping a Stream" (#26-stopping-a-stream)
27. "Copying an M3U8 URL" (#27-copying-an-m3u8-url)
28. "Stream Health" (#28-stream-health)
29. "Server Logs" (#29-server-logs)
30. "Restarting FutbolX" (#30-restarting-futbolx)
31. "Stopping FutbolX" (#31-stopping-futbolx)
32. "Updating FutbolX" (#32-updating-futbolx)
33. "Moving FutbolX to Another VPS" (#33-moving-futbolx-to-another-vps)
34. "Backing Up FutbolX" (#34-backing-up-futbolx)
35. "Restoring FutbolX" (#35-restoring-futbolx)
36. "Troubleshooting" (#36-troubleshooting)
37. "Useful Commands" (#37-useful-commands)
38. "Project Structure" (#38-project-structure)
39. "Production Architecture" (#39-production-architecture)
40. "Security Notes" (#40-security-notes)

---

1. What FutbolX Does

FutbolX is a self-hosted streaming server.

The server accepts a media source and uses FFmpeg to convert the incoming stream into HLS.

The generated HLS files are served through Nginx.

The architecture is:

Source
   |
   v
FFmpeg
   |
   v
HLS .m3u8 + .ts files
   |
   v
Nginx
   |
   v
Viewer

The FastAPI application manages:

- Stream creation
- Stream starting
- Stream stopping
- Stream restarting
- Stream deletion
- Viewer tracking
- Stream status
- Stream health
- VPS statistics
- Dashboard API

The dashboard provides:

- Dashboard
- Live Streams
- Stream Health
- Stream uptime
- Viewer count
- M3U8 copy button
- Start/stop controls
- Scheduled stream creation

---

2. VPS Requirements

Recommended VPS:

Operating System:
Ubuntu 22.04 LTS or newer

CPU:
2+ vCPU

RAM:
2 GB minimum
4 GB+ recommended

Storage:
20 GB minimum

Network:
Stable internet connection

The required software is:

Git
Python 3
Python virtual environment
FFmpeg
Nginx
Certbot
FastAPI
Uvicorn
psutil

The VPS should have a public IPv4 address.

You should also have a domain/subdomain pointing to the VPS.

Example:

futbol-x.xyz
www.futbol-x.xyz

---

3. Fresh VPS Preparation

SSH into the new VPS.

Example:

ssh root@YOUR_SERVER_IP

Check the operating system:

cat /etc/os-release

Check the current user:

whoami

Update the server:

apt update
apt upgrade -y

Install basic utilities:

apt install -y curl wget unzip zip nano sudo software-properties-common ca-certificates

Reboot if the VPS requests it:

reboot

Reconnect after the reboot:

ssh root@YOUR_SERVER_IP

---

4. Install Required Software

Install the main packages:

apt install -y git python3 python3-pip python3-venv nginx ffmpeg

Verify Git:

git --version

Verify Python:

python3 --version

Verify pip:

pip3 --version

Verify FFmpeg:

ffmpeg -version

Verify Nginx:

nginx -v

All of these commands should return version information.

---

5. Install Git

If Git was not installed in the previous step:

apt update
apt install -y git

Verify:

git --version

---

6. Install Python

Check Python:

python3 --version

Check the virtual environment module:

python3 -m venv --help

If that works, Python is ready.

If the venv module is missing:

apt install -y python3-venv

---

7. Install FFmpeg

FFmpeg is responsible for receiving the media source and creating the HLS stream.

Install:

apt install -y ffmpeg

Verify:

ffmpeg -version

You can also check the executable location:

which ffmpeg

Usually this returns:

/usr/bin/ffmpeg

Test FFmpeg:

ffmpeg -hide_banner -version

---

8. Install Nginx

Install:

apt install -y nginx

Enable Nginx:

systemctl enable nginx

Start Nginx:

systemctl start nginx

Check status:

systemctl status nginx

Press:

q

to leave the status screen.

Test the configuration:

nginx -t

Expected result:

syntax is ok
test is successful

---

9. Install Certbot

Certbot is used to obtain HTTPS certificates.

Install:

apt install -y certbot python3-certbot-nginx

Verify:

certbot --version

SSL will be configured after DNS and Nginx are ready.

---

10. Clone FutbolX

Go to "/opt":

cd /opt

Clone the repository:

git clone https://github.com/epltv1/FutbolX-Media-Server.git

Enter the project:

cd /opt/FutbolX-Media-Server

Check the files:

ls

You should see something similar to:

config
server
dashboard
README.md
requirements.txt

Check Git status:

git status

---

11. Create Required Directories

Create the HLS directory:

mkdir -p /var/www/futbolx/hls

Create the dashboard directory if it does not already exist:

mkdir -p /opt/FutbolX-Media-Server/dashboard

Set ownership:

chown -R www-data:www-data /var/www/futbolx

Set permissions:

chmod -R 755 /var/www/futbolx

Check:

ls -la /var/www/futbolx

---

12. Create Python Virtual Environment

Enter the project:

cd /opt/FutbolX-Media-Server

Create the virtual environment:

python3 -m venv venv

Activate it:

source venv/bin/activate

Your terminal should now show something similar to:

(venv) root@server:/opt/FutbolX-Media-Server#

Upgrade pip:

pip install --upgrade pip

---

13. Install Python Dependencies

Make sure you are inside the project:

cd /opt/FutbolX-Media-Server

Activate the virtual environment:

source venv/bin/activate

Install requirements:

pip install -r requirements.txt

If you need to install the packages manually:

pip install fastapi "uvicorn[standard]" psutil

Verify FastAPI:

pip show fastapi

Verify Uvicorn:

pip show uvicorn

Verify psutil:

pip show psutil

---

14. Test FutbolX Manually

Before creating the systemd service, test the application manually.

Enter the project:

cd /opt/FutbolX-Media-Server

Activate the environment:

source venv/bin/activate

Start FastAPI:

uvicorn server.main:app --host 127.0.0.1 --port 8000

If successful, you should see something similar to:

Uvicorn running on http://127.0.0.1:8000

Leave this process running.

Open another SSH session and test:

curl http://127.0.0.1:8000/api/health

You should receive a JSON response similar to:

{
  "status": "ok"
}

You can also test:

curl http://127.0.0.1:8000/api/streams

If the application responds, FastAPI is working.

Stop the manual server with:

CTRL+C

---

15. Configure Nginx

The Nginx configuration connects the public domain to FutbolX.

Remove the default site:

rm -f /etc/nginx/sites-enabled/default

Create the FutbolX configuration:

nano /etc/nginx/sites-available/futbolx

Paste the following configuration:

server {
    listen 80;
    listen [::]:80;

    server_name futbol-x.xyz www.futbol-x.xyz futbol-x.top www.futbol-x.top;

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /hls/ {
        alias /var/www/futbolx/hls/;

        types {
            application/vnd.apple.mpegurl m3u8;
            video/mp2t ts;
        }

        add_header Cache-Control "no-cache, no-store, must-revalidate";
        add_header Pragma "no-cache";
        add_header Access-Control-Allow-Origin "*";

        valid_referers none blocked futbol-x.xyz www.futbol-x.xyz futbol-x.top www.futbol-x.top;

        if ($invalid_referer) {
            return 403;
        }

        try_files $uri =404;
    }
}

Save:

CTRL+O
ENTER
CTRL+X

Enable the configuration:

ln -s /etc/nginx/sites-available/futbolx /etc/nginx/sites-enabled/futbolx

Test Nginx:

nginx -t

If successful:

systemctl reload nginx

---

16. Configure DNS

Go to your domain provider.

Create DNS records pointing to the VPS.

For example:

Type: A
Name: @
Value: YOUR_SERVER_IP

And:

Type: A
Name: www
Value: YOUR_SERVER_IP

For the second domain:

Type: A
Name: @
Value: YOUR_SERVER_IP

and:

Type: A
Name: www
Value: YOUR_SERVER_IP

DNS propagation can take some time.

Check DNS from the VPS:

apt install -y dnsutils

Then:

dig futbol-x.xyz

You should see your VPS IP.

You can also check:

dig www.futbol-x.xyz

Do not continue with SSL until the domain resolves to the correct VPS.

---

17. Create Systemd Service

Systemd keeps FutbolX running in the background.

It also allows FutbolX to automatically start after a VPS reboot.

Create the service:

nano /etc/systemd/system/futbolx.service

Paste:

[Unit]
Description=FutbolX Media Server
After=network.target nginx.service

[Service]
Type=simple

User=root
Group=root

WorkingDirectory=/opt/FutbolX-Media-Server

Environment="PATH=/opt/FutbolX-Media-Server/venv/bin"

ExecStart=/opt/FutbolX-Media-Server/venv/bin/uvicorn server.main:app --host 127.0.0.1 --port 8000

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target

Save:

CTRL+O
ENTER
CTRL+X

Reload systemd:

systemctl daemon-reload

Enable FutbolX:

systemctl enable futbolx

Start FutbolX:

systemctl start futbolx

Check:

systemctl status futbolx

You should see:

Active: active (running)

---

18. Start FutbolX

The normal command to start FutbolX is:

systemctl start futbolx

Enable automatic startup:

systemctl enable futbolx

Check:

systemctl status futbolx

Restart:

systemctl restart futbolx

Stop:

systemctl stop futbolx

---

19. Configure Firewall

If UFW is installed, allow SSH:

ufw allow OpenSSH

Allow HTTP:

ufw allow 80/tcp

Allow HTTPS:

ufw allow 443/tcp

Enable UFW:

ufw enable

Check:

ufw status

Expected ports:

22
80
443

Port "8000" does NOT need to be publicly exposed because Nginx communicates with FastAPI locally.

Do NOT open port 8000 unnecessarily.

---

20. Configure HTTPS / SSL

Once DNS is working and Nginx is running, request the certificate:

certbot --nginx -d futbol-x.xyz -d www.futbol-x.xyz

If using the second domain:

certbot --nginx -d futbol-x.top -d www.futbol-x.top

Certbot will ask whether HTTP should redirect to HTTPS.

Choose the HTTPS redirect option.

Check certificates:

certbot certificates

Test automatic renewal:

certbot renew --dry-run

If the test succeeds, automatic renewal is configured.

---

21. Verify Installation

First check FastAPI:

curl http://127.0.0.1:8000/api/health

Then check through Nginx:

curl http://futbol-x.xyz/api/health

After SSL:

curl https://futbol-x.xyz/api/health

Check streams:

curl https://futbol-x.xyz/api/streams

Open the dashboard in a browser:

https://futbol-x.xyz/

---

22. Using the Dashboard

The dashboard contains:

Dashboard
Live Streams
Stream Health

The sidebar also displays:

Server Online
Server Uptime

The dashboard communicates with the FastAPI API.

The server should remain running through systemd.

---

23. Creating a Live Stream

A stream can be created with:

Name
Source URL

Example:

Name:
Test Stream

Source:
YOUR_AUTHORIZED_MEDIA_SOURCE

Then press:

Start

The API creates a stream ID.

Example:

abc12345

The HLS output becomes:

https://futbol-x.xyz/hls/abc12345/index.m3u8

Only use media sources that you are authorized to stream.

---

24. Scheduling a Stream

A scheduled stream can be created without a source.

For example:

Name:
Match Stream

The stream receives an ID but FFmpeg does not start.

The stream appears as a scheduled/offline stream.

The dashboard can then display an:

Add Stream

button.

---

25. Starting a Scheduled Stream

When a source is available, add the source to the scheduled stream.

Then press:

Start

The server starts FFmpeg.

The stream becomes live.

The "started_at" timestamp is recorded when the FFmpeg process starts successfully.

---

26. Stopping a Stream

Press:

Stop

The server should:

1. Stop FFmpeg.
2. Kill the FFmpeg process.
3. Remove the FFmpeg process from memory.
4. Delete the stream's HLS directory.
5. Remove the ".m3u8" file.
6. Remove the ".ts" segments.
7. Clear viewer tracking.
8. Remove the stream from the active stream list.

After stopping, the old M3U8 URL should no longer work.

Example:

/hls/abc12345/index.m3u8

will no longer have an active HLS playlist.

---

27. Copying an M3U8 URL

For every active stream, the dashboard provides a copy button.

The generated URL follows this format:

https://YOUR_DOMAIN/hls/STREAM_ID/index.m3u8

Example:

https://futbol-x.xyz/hls/abc12345/index.m3u8

The exact stream ID is generated automatically.

---

28. Stream Health

The Stream Health page displays server information such as:

Active Streams
Total Viewers
CPU Usage
RAM Usage
Server Uptime

The dashboard periodically refreshes the statistics.

CPU and RAM statistics are obtained from the VPS itself.

Server uptime is based on the VPS boot time.

---

29. Server Logs

Check FutbolX logs:

journalctl -u futbolx

Follow logs live:

journalctl -u futbolx -f

Show the latest logs:

journalctl -u futbolx -n 100

Show logs since the last boot:

journalctl -u futbolx -b

Nginx error log:

tail -f /var/log/nginx/error.log

Nginx access log:

tail -f /var/log/nginx/access.log

---

30. Restarting FutbolX

Restart the application:

systemctl restart futbolx

Check status:

systemctl status futbolx

Restart Nginx:

systemctl restart nginx

Check Nginx:

systemctl status nginx

---

31. Stopping FutbolX

Stop the application:

systemctl stop futbolx

Check:

systemctl status futbolx

Start again:

systemctl start futbolx

Disable automatic startup:

systemctl disable futbolx

Normally, keep FutbolX enabled:

systemctl enable futbolx

---

32. Updating FutbolX

Before updating, check the current directory:

cd /opt/FutbolX-Media-Server

Check status:

git status

Stop FutbolX:

systemctl stop futbolx

Download the latest repository changes:

git pull

Activate the virtual environment:

source venv/bin/activate

Update dependencies:

pip install -r requirements.txt

Restart:

systemctl restart futbolx

Check:

systemctl status futbolx

Test:

curl http://127.0.0.1:8000/api/health

---

33. Moving FutbolX to Another VPS

This is the important migration procedure.

The easiest migration is:

New VPS
   |
   +-- Install software
   |
   +-- Clone GitHub repository
   |
   +-- Create directories
   |
   +-- Install Python dependencies
   |
   +-- Configure Nginx
   |
   +-- Configure systemd
   |
   +-- Point DNS to new VPS
   |
   +-- Install SSL
   |
   +-- Start FutbolX

Step 1 — Prepare the new VPS

SSH into the new VPS:

ssh root@NEW_SERVER_IP

Update:

apt update
apt upgrade -y

Install dependencies:

apt install -y git python3 python3-pip python3-venv nginx ffmpeg curl wget unzip zip nano sudo ca-certificates certbot python3-certbot-nginx

---

Step 2 — Clone the repository

cd /opt

git clone https://github.com/epltv1/FutbolX-Media-Server.git

cd /opt/FutbolX-Media-Server

---

Step 3 — Create directories

mkdir -p /var/www/futbolx/hls

chown -R www-data:www-data /var/www/futbolx

chmod -R 755 /var/www/futbolx

---

Step 4 — Create virtual environment

cd /opt/FutbolX-Media-Server

python3 -m venv venv

source venv/bin/activate

---

Step 5 — Install dependencies

pip install --upgrade pip

pip install -r requirements.txt

---

Step 6 — Configure Nginx

Create:

nano /etc/nginx/sites-available/futbolx

Paste the Nginx configuration from this README.

Enable it:

ln -s /etc/nginx/sites-available/futbolx /etc/nginx/sites-enabled/futbolx

Test:

nginx -t

Reload:

systemctl reload nginx

---

Step 7 — Configure systemd

Create:

nano /etc/systemd/system/futbolx.service

Paste the systemd configuration from this README.

Then:

systemctl daemon-reload

Enable:

systemctl enable futbolx

Start:

systemctl start futbolx

---

Step 8 — Move DNS

Change the domain's A records from the old VPS IP to the new VPS IP.

Example:

OLD VPS:
1.2.3.4

NEW VPS:
5.6.7.8

Change:

futbol-x.xyz -> 5.6.7.8

Wait for DNS propagation.

Verify:

dig futbol-x.xyz

---

Step 9 — Install SSL

Once DNS points to the new VPS:

certbot --nginx -d futbol-x.xyz -d www.futbol-x.xyz

Then:

certbot renew --dry-run

---

Step 10 — Verify

Check:

systemctl status futbolx

Check:

systemctl status nginx

Check API:

curl https://futbol-x.xyz/api/health

Open:

https://futbol-x.xyz/

The new VPS is now running FutbolX.

---

34. Backing Up FutbolX

The application itself is stored in GitHub, so the main code does not need to be manually backed up.

Check the repository:

cd /opt/FutbolX-Media-Server

git status

If you make important local changes, commit and push them to GitHub.

Example:

git add .

git commit -m "Update FutbolX"

git push

Backup Nginx

Create a backup directory:

mkdir -p /root/futbolx-backup

Copy Nginx configuration:

cp /etc/nginx/sites-available/futbolx /root/futbolx-backup/

Backup systemd

cp /etc/systemd/system/futbolx.service /root/futbolx-backup/

Backup dashboard/server configuration

If configuration files contain custom settings:

cp -r /opt/FutbolX-Media-Server /root/futbolx-backup/

Be careful with copying the virtual environment because it is normally unnecessary and can be recreated.

---

35. Restoring FutbolX

On a new VPS:

cd /opt

Clone the repository:

git clone https://github.com/epltv1/FutbolX-Media-Server.git

Install dependencies again:

cd /opt/FutbolX-Media-Server

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

Restore Nginx:

cp /root/futbolx-backup/futbolx /etc/nginx/sites-available/futbolx

Enable:

ln -s /etc/nginx/sites-available/futbolx /etc/nginx/sites-enabled/futbolx

Restore systemd:

cp /root/futbolx-backup/futbolx.service /etc/systemd/system/futbolx.service

Reload:

systemctl daemon-reload

Enable:

systemctl enable futbolx

Start:

systemctl start futbolx

Test:

nginx -t

systemctl restart nginx

---

36. Troubleshooting

FutbolX will not start

Check:

systemctl status futbolx

Then:

journalctl -u futbolx -n 100 --no-pager

Check Python:

/opt/FutbolX-Media-Server/venv/bin/python --version

Check Uvicorn:

/opt/FutbolX-Media-Server/venv/bin/uvicorn --version

---

Port 8000 is not responding

Check:

ss -lntp | grep 8000

Try:

curl http://127.0.0.1:8000/api/health

If it does not respond, check:

systemctl status futbolx

---

Nginx is not working

Test:

nginx -t

Check:

systemctl status nginx

Check errors:

tail -100 /var/log/nginx/error.log

---

Domain does not open

Check DNS:

dig futbol-x.xyz

Make sure the returned IP is the VPS IP.

Check Nginx:

systemctl status nginx

Check firewall:

ufw status

Make sure ports "80" and "443" are allowed.

---

SSL does not work

First verify DNS.

Then:

certbot certificates

Try:

certbot renew --dry-run

Check Nginx:

nginx -t

---

HLS stream does not work

Check the HLS directory:

ls -lah /var/www/futbolx/hls

Check whether a stream directory exists:

ls -lah /var/www/futbolx/hls/STREAM_ID

You should see files similar to:

index.m3u8
segment*.ts

Check FutbolX:

journalctl -u futbolx -f

Check FFmpeg:

ps aux | grep ffmpeg

---

FFmpeg is not running

Check:

ps aux | grep ffmpeg

Check:

journalctl -u futbolx -n 100 --no-pager

Verify FFmpeg:

which ffmpeg

ffmpeg -version

---

Stream stops unexpectedly

Check:

journalctl -u futbolx -f

Check server resources:

free -h

df -h

Check CPU:

top

Also verify that the source is available and that you are authorized to use it.

---

VPS disk is full

Check:

df -h

Check the HLS directory:

du -sh /var/www/futbolx/hls

Check the project:

du -sh /opt/FutbolX-Media-Server

Check system logs:

journalctl --disk-usage

Clean old system logs if necessary:

journalctl --vacuum-time=7d

---

37. Useful Commands

FutbolX

Start:

systemctl start futbolx

Stop:

systemctl stop futbolx

Restart:

systemctl restart futbolx

Status:

systemctl status futbolx

Enable startup:

systemctl enable futbolx

Disable startup:

systemctl disable futbolx

Logs:

journalctl -u futbolx -f

---

Nginx

Start:

systemctl start nginx

Stop:

systemctl stop nginx

Restart:

systemctl restart nginx

Reload:

systemctl reload nginx

Status:

systemctl status nginx

Test:

nginx -t

---

FFmpeg

Check:

ffmpeg -version

Find executable:

which ffmpeg

Check running processes:

ps aux | grep ffmpeg

---

Python

Check:

python3 --version

Activate environment:

cd /opt/FutbolX-Media-Server
source venv/bin/activate

Install requirements:

pip install -r requirements.txt

---

Server Resources

CPU/memory:

top

Memory:

free -h

Disk:

df -h

Disk usage:

du -sh /var/www/futbolx/hls

Network ports:

ss -lntp

VPS uptime:

uptime

---

38. Project Structure

The project should look approximately like:

FutbolX-Media-Server/
│
├── config/
│   └── nginx.conf
│
├── dashboard/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── server/
│   ├── main.py
│   ├── ffmpeg.py
│   ├── security.py
│   ├── streams.py
│   └── viewers.py
│
├── venv/
│
├── .gitignore
├── README.md
└── requirements.txt

The HLS output is stored outside the Git repository:

/var/www/futbolx/hls/

A running stream may create:

/var/www/futbolx/hls/
└── STREAM_ID/
    ├── index.m3u8
    ├── segment1.ts
    ├── segment2.ts
    └── ...

When a stream is stopped, its HLS files should be removed.

---

39. Production Architecture

The production setup is:

                    INTERNET
                       |
                       v
                +-------------+
                |    Nginx    |
                |   :80/:443  |
                +------+------+
                       |
          +------------+------------+
          |                         |
          v                         v
     FastAPI API                  HLS
     127.0.0.1:8000       /var/www/futbolx/hls
          |
          v
       FFmpeg
          |
          v
   Authorized source

Systemd keeps FastAPI running:

systemd
   |
   v
FutbolX
   |
   v
FastAPI
   |
   +---- FFmpeg
   |
   +---- Stream management
   |
   +---- Viewer tracking
   |
   +---- Server statistics

Nginx handles:

HTTPS
Reverse proxy
HLS delivery
Static media delivery
Domain routing

FastAPI handles:

API
Dashboard backend
Stream management
Viewer management
Health information

FFmpeg handles:

Media input
HLS generation
Segment creation

---

40. Security Notes

Keep FastAPI private

FastAPI listens on:

127.0.0.1:8000

Do not expose port "8000" directly to the internet unless there is a specific reason.

Nginx should be the public entry point.

---

Use HTTPS

Production access should use:

https://

rather than plain:

http://

---

Keep the VPS updated

Regularly run:

apt update
apt upgrade -y

---

Protect SSH

Use SSH keys where possible.

Do not expose unnecessary ports.

Check:

ufw status

---

Monitor disk space

HLS streams create media segments.

Regularly check:

df -h

and:

du -sh /var/www/futbolx/hls

---

COMPLETE FRESH-VPS INSTALLATION CHEAT SHEET

For a completely fresh Ubuntu VPS, the basic installation flow is:

apt update && apt upgrade -y

apt install -y git python3 python3-pip python3-venv nginx ffmpeg curl wget unzip zip nano sudo ca-certificates certbot python3-certbot-nginx

cd /opt

git clone https://github.com/epltv1/FutbolX-Media-Server.git

cd /opt/FutbolX-Media-Server

mkdir -p /var/www/futbolx/hls

chown -R www-data:www-data /var/www/futbolx

chmod -R 755 /var/www/futbolx

python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip

pip install -r requirements.txt

Test:

uvicorn server.main:app --host 127.0.0.1 --port 8000

In another SSH session:

curl http://127.0.0.1:8000/api/health

Then configure Nginx:

nano /etc/nginx/sites-available/futbolx

Enable:

ln -s /etc/nginx/sites-available/futbolx /etc/nginx/sites-enabled/futbolx

Test:

nginx -t

Reload:

systemctl reload nginx

Create systemd:

nano /etc/systemd/system/futbolx.service

Then:

systemctl daemon-reload

systemctl enable futbolx

systemctl start futbolx

Check:

systemctl status futbolx

Configure firewall:

ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable

After DNS points to the VPS:

certbot --nginx -d futbol-x.xyz -d www.futbol-x.xyz

Finally:

curl https://futbol-x.xyz/api/health

Open:

https://futbol-x.xyz/

---

FINAL CHECKLIST

Before considering the installation complete, verify every item:

[ ] VPS updated
[ ] Git installed
[ ] Python installed
[ ] Python venv installed
[ ] FFmpeg installed
[ ] Nginx installed
[ ] Certbot installed
[ ] FutbolX cloned
[ ] HLS directory created
[ ] Python virtual environment created
[ ] Python requirements installed
[ ] FastAPI tested
[ ] Nginx configured
[ ] DNS points to VPS
[ ] Systemd service created
[ ] FutbolX service enabled
[ ] FutbolX service running
[ ] Firewall configured
[ ] SSL certificate installed
[ ] HTTPS working
[ ] API responding
[ ] Dashboard loading
[ ] HLS directory accessible
[ ] Stream creation tested
[ ] Stream start tested
[ ] Stream stop tested
[ ] M3U8 URL tested
[ ] Stream health tested
[ ] Logs checked

---

IMPORTANT PATHS

FutbolX project:

/opt/FutbolX-Media-Server

Python virtual environment:

/opt/FutbolX-Media-Server/venv

HLS directory:

/var/www/futbolx/hls

Nginx configuration:

/etc/nginx/sites-available/futbolx

Enabled Nginx configuration:

/etc/nginx/sites-enabled/futbolx

Systemd service:

/etc/systemd/system/futbolx.service

Nginx logs:

/var/log/nginx/

---

QUICK MIGRATION FORMULA

When moving FutbolX to a new VPS, remember:

1. Get new VPS
2. Install Ubuntu packages
3. Install Git/Python/FFmpeg/Nginx/Certbot
4. Clone FutbolX
5. Create /var/www/futbolx/hls
6. Create Python venv
7. Install requirements
8. Configure Nginx
9. Configure systemd
10. Start FutbolX
11. Point DNS to new VPS
12. Install SSL
13. Test API
14. Test dashboard
15. Test a stream

The GitHub repository contains the application code.

The VPS-specific configuration consists mainly of:

Nginx
Systemd
DNS
SSL
HLS directory

This means FutbolX can be rebuilt on a new VPS without manually rebuilding the entire application from scratch.
