FutbolX Media Server

Self-hosted media streaming server using FastAPI, FFmpeg, HLS, Nginx, and Systemd.

This README is written as a from-scratch installation and migration manual.

The goal is simple:

«If you get a completely new VPS, you should be able to open this README and rebuild FutbolX without needing to remember anything from the previous server.»

---

🚦 HOW TO READ THIS README

Before doing anything, understand the labels used throughout this guide.

🟢 COPY & RUN

Whenever you see this:

🟢 COPY & RUN

Copy the command(s) inside the following code block and paste them directly into your VPS terminal.

Example:

apt update && apt upgrade -y

---

🔵 CREATE / EDIT FILE

Whenever you see:

🔵 CREATE / EDIT FILE

You will be told:

1. Which file to open.
2. Exactly what content to put inside it.
3. How to save it.

For example:

nano /etc/nginx/sites-available/futbolx

Then you will be told to paste the configuration provided below that command.

---

🟡 EDIT THIS

Whenever you see:

🟡 EDIT THIS

You must replace the example value with your own value.

For example:

YOUR_SERVER_IP
YOUR_DOMAIN
YOUR_STREAM_SOURCE

Do not literally paste "YOUR_SERVER_IP" unless the command specifically tells you to.

---

⚪ EXPLANATION

Anything outside a command block is normally an explanation.

You don't need to copy the explanation into the VPS.

---

🔴 EXPECTED RESULT

Anything marked as an expected result is something you should see after running a command.

Do not copy the expected result into the terminal.

---

TABLE OF CONTENTS

1. "What FutbolX Does" (#1-what-futbolx-does)
2. "VPS Requirements" (#2-vps-requirements)
3. "Important Values" (#3-important-values)
4. "Fresh VPS Preparation" (#4-fresh-vps-preparation)
5. "Install Required Software" (#5-install-required-software)
6. "Verify Git" (#6-verify-git)
7. "Verify Python" (#7-verify-python)
8. "Verify FFmpeg" (#8-verify-ffmpeg)
9. "Install and Start Nginx" (#9-install-and-start-nginx)
10. "Install Certbot" (#10-install-certbot)
11. "Clone FutbolX" (#11-clone-futbolx)
12. "Create Required Directories" (#12-create-required-directories)
13. "Create Python Virtual Environment" (#13-create-python-virtual-environment)
14. "Install Python Dependencies" (#14-install-python-dependencies)
15. "Test FutbolX Manually" (#15-test-futbolx-manually)
16. "Configure Nginx" (#16-configure-nginx)
17. "Configure DNS" (#17-configure-dns)
18. "Create Systemd Service" (#18-create-systemd-service)
19. "Start FutbolX" (#19-start-futbolx)
20. "Configure Firewall" (#20-configure-firewall)
21. "Configure HTTPS / SSL" (#21-configure-https--ssl)
22. "Verify Installation" (#22-verify-installation)
23. "Using the Dashboard" (#23-using-the-dashboard)
24. "Creating a Live Stream" (#24-creating-a-live-stream)
25. "Scheduling a Stream" (#25-scheduling-a-stream)
26. "Starting a Scheduled Stream" (#26-starting-a-scheduled-stream)
27. "Stopping a Stream" (#27-stopping-a-stream)
28. "Copying an M3U8 URL" (#28-copying-an-m3u8-url)
29. "Stream Health" (#29-stream-health)
30. "Server Logs" (#30-server-logs)
31. "Restarting FutbolX" (#31-restarting-futbolx)
32. "Stopping FutbolX" (#32-stopping-futbolx)
33. "Updating FutbolX" (#33-updating-futbolx)
34. "Moving FutbolX to Another VPS" (#34-moving-futbolx-to-another-vps)
35. "Backing Up FutbolX" (#35-backing-up-futbolx)
36. "Restoring FutbolX" (#36-restoring-futbolx)
37. "Troubleshooting" (#37-troubleshooting)
38. "Useful Commands" (#38-useful-commands)
39. "Project Structure" (#39-project-structure)
40. "Production Architecture" (#40-production-architecture)
41. "Security Notes" (#41-security-notes)
42. "Complete Fresh VPS Installation" (#42-complete-fresh-vps-installation)
43. "Final Installation Checklist" (#43-final-installation-checklist)
44. "Important Paths" (#44-important-paths)
45. "Quick Migration Formula" (#45-quick-migration-formula)

---

1. What FutbolX Does

FutbolX is a self-hosted media streaming server.

The basic flow is:

MEDIA SOURCE
     |
     v
   FFmpeg
     |
     v
HLS .m3u8 + .ts segments
     |
     v
   Nginx
     |
     v
   VIEWER

FastAPI controls the streaming system.

It manages:

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

Recommended VPS

Operating System

Ubuntu 22.04 LTS or newer.

CPU

2+ vCPU recommended.

RAM

2 GB minimum.

4 GB+ recommended if running several streams.

Storage

20 GB minimum.

More storage may be required depending on how many streams are running.

Network

Stable internet connection.

IP

A public IPv4 address.

You should also have a domain pointing to the VPS.

Example:

futbol-x.xyz
www.futbol-x.xyz

---

3. Important Values

Before installation, know these values.

🟡 EDIT THIS

Replace the examples below with your actual values.

YOUR_SERVER_IP
YOUR_DOMAIN
YOUR_STREAM_SOURCE

For example:

YOUR_SERVER_IP = 123.123.123.123
YOUR_DOMAIN = futbol-x.xyz

You will use these values in several sections.

---

4. Fresh VPS Preparation

First connect to the new VPS.

🟢 COPY & RUN

ssh root@YOUR_SERVER_IP

Replace:

YOUR_SERVER_IP

with your actual VPS IP.

---

Check operating system

🟢 COPY & RUN

cat /etc/os-release

You should see Ubuntu information.

---

Check current user

🟢 COPY & RUN

whoami

🔴 EXPECTED RESULT

If you are installing as root:

root

---

Update the VPS

🟢 COPY & RUN

apt update && apt upgrade -y

This updates installed packages.

---

Install basic utilities

🟢 COPY & RUN

apt install -y curl wget unzip zip nano sudo software-properties-common ca-certificates

---

Reboot if necessary

If Ubuntu asks for a reboot, run:

🟢 COPY & RUN

reboot

Your SSH connection will close.

Wait a few seconds, then reconnect:

🟢 COPY & RUN

ssh root@YOUR_SERVER_IP

---

5. Install Required Software

Install the main FutbolX dependencies.

🟢 COPY & RUN

apt install -y git python3 python3-pip python3-venv nginx ffmpeg

This installs:

- Git
- Python 3
- pip
- Python virtual environment
- Nginx
- FFmpeg

---

6. Verify Git

🟢 COPY & RUN

git --version

🔴 EXPECTED RESULT

You should receive a Git version.

Example:

git version 2.x.x

---

7. Verify Python

🟢 COPY & RUN

python3 --version

You should receive a Python version.

Also test the virtual environment module:

🟢 COPY & RUN

python3 -m venv --help

If this works, Python's virtual environment support is installed.

If it does not work:

🟢 COPY & RUN

apt install -y python3-venv

---

8. Verify FFmpeg

FFmpeg receives the media source and converts it into HLS.

🟢 COPY & RUN

ffmpeg -version

Find the executable:

🟢 COPY & RUN

which ffmpeg

🔴 EXPECTED RESULT

Usually:

/usr/bin/ffmpeg

---

9. Install and Start Nginx

Nginx serves the HLS files and acts as the public reverse proxy.

Install:

🟢 COPY & RUN

apt install -y nginx

Enable automatic startup:

🟢 COPY & RUN

systemctl enable nginx

Start Nginx:

🟢 COPY & RUN

systemctl start nginx

Check:

🟢 COPY & RUN

systemctl status nginx

Press:

q

to exit the status screen.

Test configuration:

🟢 COPY & RUN

nginx -t

🔴 EXPECTED RESULT

You should see:

syntax is ok
test is successful

---

10. Install Certbot

Certbot obtains HTTPS certificates for your domain.

🟢 COPY & RUN

apt install -y certbot python3-certbot-nginx

Verify:

🟢 COPY & RUN

certbot --version

Do not request SSL yet.

DNS and Nginx must be configured first.

---

11. Clone FutbolX

Go to "/opt".

🟢 COPY & RUN

cd /opt

Clone the repository:

🟢 COPY & RUN

git clone https://github.com/epltv1/FutbolX-Media-Server.git

Enter the project:

🟢 COPY & RUN

cd /opt/FutbolX-Media-Server

Check the files:

🟢 COPY & RUN

ls

You should see the FutbolX project files.

Check Git:

🟢 COPY & RUN

git status

---

12. Create Required Directories

The HLS files should be stored outside the Git repository.

Create the HLS directory:

🟢 COPY & RUN

mkdir -p /var/www/futbolx/hls

Set ownership:

🟢 COPY & RUN

chown -R www-data:www-data /var/www/futbolx

Set permissions:

🟢 COPY & RUN

chmod -R 755 /var/www/futbolx

Check:

🟢 COPY & RUN

ls -la /var/www/futbolx

---

13. Create Python Virtual Environment

Enter the project:

🟢 COPY & RUN

cd /opt/FutbolX-Media-Server

Create the environment:

🟢 COPY & RUN

python3 -m venv venv

Activate it:

🟢 COPY & RUN

source venv/bin/activate

Your terminal should now show something similar to:

(venv) root@server:/opt/FutbolX-Media-Server#

Upgrade pip:

🟢 COPY & RUN

pip install --upgrade pip

---

14. Install Python Dependencies

Make sure you are in the project:

🟢 COPY & RUN

cd /opt/FutbolX-Media-Server

Activate the environment:

🟢 COPY & RUN

source venv/bin/activate

Install dependencies:

🟢 COPY & RUN

pip install -r requirements.txt

If the project does not contain a requirements file, install the required packages manually:

🟢 COPY & RUN

pip install fastapi "uvicorn[standard]" psutil

Verify FastAPI:

🟢 COPY & RUN

pip show fastapi

Verify Uvicorn:

🟢 COPY & RUN

pip show uvicorn

Verify psutil:

🟢 COPY & RUN

pip show psutil

---

15. Test FutbolX Manually

Do this before creating the Systemd service.

Enter the project:

🟢 COPY & RUN

cd /opt/FutbolX-Media-Server

Activate the environment:

🟢 COPY & RUN

source venv/bin/activate

Start FastAPI:

🟢 COPY & RUN

uvicorn server.main:app --host 127.0.0.1 --port 8000

🔴 EXPECTED RESULT

You should see something similar to:

Uvicorn running on http://127.0.0.1:8000

Do not close this SSH session yet.

Open another SSH session.

Test the health endpoint:

🟢 COPY & RUN

curl http://127.0.0.1:8000/api/health

🔴 EXPECTED RESULT

You should receive a response similar to:

{
  "status": "ok"
}

Also test:

🟢 COPY & RUN

curl http://127.0.0.1:8000/api/streams

If the API responds, FastAPI is working.

Return to the terminal running Uvicorn.

Stop it with:

🟢 PRESS

CTRL+C

---

16. Configure Nginx

Nginx will:

- Receive public HTTP/HTTPS requests.
- Forward API requests to FastAPI.
- Serve HLS files.
- Protect the FastAPI port from direct internet access.

---

Remove the default Nginx site

🟢 COPY & RUN

rm -f /etc/nginx/sites-enabled/default

---

Create the FutbolX Nginx configuration

🔵 CREATE / EDIT FILE

Run:

nano /etc/nginx/sites-available/futbolx

🟡 EDIT THIS

If your domain is different, replace the domain names in the configuration.

🟢 COPY & PASTE THIS ENTIRE CONFIGURATION

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

🔵 SAVE THE FILE

Inside nano:

CTRL+O
ENTER
CTRL+X

---

Enable the FutbolX configuration

🟢 COPY & RUN

ln -s /etc/nginx/sites-available/futbolx /etc/nginx/sites-enabled/futbolx

If the link already exists, do not create another one.

---

Test Nginx

🟢 COPY & RUN

nginx -t

🔴 EXPECTED RESULT

syntax is ok
test is successful

Reload:

🟢 COPY & RUN

systemctl reload nginx

---

17. Configure DNS

Go to the company where your domain is managed.

Create an A record pointing your domain to your VPS.

For:

futbol-x.xyz

Use:

Type: A
Name: @
Value: YOUR_SERVER_IP

For:

www.futbol-x.xyz

Use:

Type: A
Name: www
Value: YOUR_SERVER_IP

If you use "futbol-x.top", create the equivalent records for that domain.

---

Verify DNS

Install DNS utilities:

🟢 COPY & RUN

apt install -y dnsutils

Check:

🟢 COPY & RUN

dig futbol-x.xyz

And:

🟢 COPY & RUN

dig www.futbol-x.xyz

🔴 EXPECTED RESULT

The returned IP should be your VPS IP.

Do not continue to SSL until DNS points to the correct VPS.

---

18. Create Systemd Service

Systemd keeps FutbolX running in the background.

It also automatically starts FutbolX after a VPS reboot.

---

Create the service file

🔵 CREATE / EDIT FILE

Run:

nano /etc/systemd/system/futbolx.service

🟢 COPY & PASTE THIS ENTIRE FILE

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

🔵 SAVE THE FILE

CTRL+O
ENTER
CTRL+X

---

Reload Systemd

🟢 COPY & RUN

systemctl daemon-reload

---

19. Start FutbolX

Enable automatic startup:

🟢 COPY & RUN

systemctl enable futbolx

Start FutbolX:

🟢 COPY & RUN

systemctl start futbolx

Check status:

🟢 COPY & RUN

systemctl status futbolx

🔴 EXPECTED RESULT

Look for:

Active: active (running)

Press:

q

to leave the status screen.

---

20. Configure Firewall

If UFW is being used, allow SSH first.

🟢 COPY & RUN

ufw allow OpenSSH

Allow HTTP:

🟢 COPY & RUN

ufw allow 80/tcp

Allow HTTPS:

🟢 COPY & RUN

ufw allow 443/tcp

Enable UFW:

🟢 COPY & RUN

ufw enable

Check:

🟢 COPY & RUN

ufw status

You should have access to:

22
80
443

⚠️ IMPORTANT

Do NOT open port 8000 publicly.

FastAPI listens on:

127.0.0.1:8000

Nginx communicates with it locally.

---

21. Configure HTTPS / SSL

Only do this after:

- DNS is correct.
- Nginx is running.
- The domain resolves to the VPS.

For "futbol-x.xyz":

🟢 COPY & RUN

certbot --nginx -d futbol-x.xyz -d www.futbol-x.xyz

If using the ".top" domain:

🟢 COPY & RUN

certbot --nginx -d futbol-x.top -d www.futbol-x.top

Certbot will ask about redirecting HTTP to HTTPS.

Choose the HTTPS redirect option.

Check certificates:

🟢 COPY & RUN

certbot certificates

Test automatic renewal:

🟢 COPY & RUN

certbot renew --dry-run

🔴 EXPECTED RESULT

The renewal test should complete successfully.

---

22. Verify Installation

Test FastAPI locally:

🟢 COPY & RUN

curl http://127.0.0.1:8000/api/health

Test through Nginx:

🟢 COPY & RUN

curl https://futbol-x.xyz/api/health

Test streams:

🟢 COPY & RUN

curl https://futbol-x.xyz/api/streams

Open the dashboard:

🌐 OPEN IN BROWSER

https://futbol-x.xyz/

If the dashboard loads, the basic installation is complete.

---

23. Using the Dashboard

The dashboard provides:

- Dashboard
- Live Streams
- Stream Health
- Stream uptime
- Viewer count
- Start controls
- Stop controls
- M3U8 copy button
- Scheduled streams

The sidebar also displays server information such as:

- Server Online
- Server Uptime

The dashboard communicates with the FastAPI backend.

Systemd keeps the backend running.

---

24. Creating a Live Stream

A stream requires:

Name
Source URL

Example:

Name:
Test Stream

Source:
YOUR_AUTHORIZED_MEDIA_SOURCE

The server creates a stream ID.

Example:

abc12345

The HLS URL becomes:

https://futbol-x.xyz/hls/abc12345/index.m3u8

⚠️ IMPORTANT

Only use media sources that you are authorized to stream.

---

25. Scheduling a Stream

A scheduled stream can be created without immediately providing a source.

Example:

Name:
Match Stream

The stream receives an ID.

FFmpeg does not start until a source is provided and the stream is started.

The dashboard can display the scheduled/offline stream.

---

26. Starting a Scheduled Stream

When the source is available:

1. Add the source.
2. Press Start.

The server starts FFmpeg.

The stream becomes live.

The "started_at" timestamp is recorded when FFmpeg successfully starts.

---

27. Stopping a Stream

When Stop is pressed, FutbolX should:

1. Stop FFmpeg.
2. Kill the FFmpeg process if necessary.
3. Remove the FFmpeg process from memory.
4. Delete the stream's HLS directory.
5. Remove the ".m3u8" playlist.
6. Remove ".ts" segments.
7. Clear viewer tracking.
8. Remove the stream from the active stream list.

For example:

/hls/abc12345/index.m3u8

should no longer contain an active playlist after the stream is stopped.

---

28. Copying an M3U8 URL

Every active stream has an M3U8 URL.

Format:

https://YOUR_DOMAIN/hls/STREAM_ID/index.m3u8

Example:

https://futbol-x.xyz/hls/abc12345/index.m3u8

The stream ID is generated automatically.

The dashboard's Copy button should copy the complete URL.

---

29. Stream Health

The Stream Health section provides information such as:

- Active streams
- Total viewers
- CPU usage
- RAM usage
- Server uptime

CPU and RAM information comes from the VPS.

Server uptime is based on the VPS boot time.

---

30. Server Logs

FutbolX logs

🟢 COPY & RUN

journalctl -u futbolx

Follow logs live:

🟢 COPY & RUN

journalctl -u futbolx -f

Show the last 100 entries:

🟢 COPY & RUN

journalctl -u futbolx -n 100 --no-pager

Show logs since boot:

🟢 COPY & RUN

journalctl -u futbolx -b

---

Nginx error log

🟢 COPY & RUN

tail -f /var/log/nginx/error.log

---

Nginx access log

🟢 COPY & RUN

tail -f /var/log/nginx/access.log

---

31. Restarting FutbolX

Restart:

🟢 COPY & RUN

systemctl restart futbolx

Check:

🟢 COPY & RUN

systemctl status futbolx

Restart Nginx:

🟢 COPY & RUN

systemctl restart nginx

Check:

🟢 COPY & RUN

systemctl status nginx

---

32. Stopping FutbolX

Stop:

🟢 COPY & RUN

systemctl stop futbolx

Check:

🟢 COPY & RUN

systemctl status futbolx

Start again:

🟢 COPY & RUN

systemctl start futbolx

Disable automatic startup:

🟢 COPY & RUN

systemctl disable futbolx

Normally, keep automatic startup enabled:

🟢 COPY & RUN

systemctl enable futbolx

---

33. Updating FutbolX

Before updating:

🟢 COPY & RUN

cd /opt/FutbolX-Media-Server

Check Git:

🟢 COPY & RUN

git status

Stop FutbolX:

🟢 COPY & RUN

systemctl stop futbolx

Pull the latest code:

🟢 COPY & RUN

git pull

Activate the virtual environment:

🟢 COPY & RUN

source venv/bin/activate

Update dependencies:

🟢 COPY & RUN

pip install -r requirements.txt

Start FutbolX:

🟢 COPY & RUN

systemctl start futbolx

Check:

🟢 COPY & RUN

systemctl status futbolx

Test:

🟢 COPY & RUN

curl http://127.0.0.1:8000/api/health

---

34. Moving FutbolX to Another VPS

This is the main migration procedure.

The important thing to understand is that the application code lives in GitHub.

The new VPS mainly needs:

FutbolX code
+
Python environment
+
HLS directory
+
Nginx configuration
+
Systemd service
+
DNS
+
SSL

---

MIGRATION OVERVIEW

NEW VPS
   |
   +-- Install Ubuntu packages
   |
   +-- Clone FutbolX
   |
   +-- Create HLS directory
   |
   +-- Create Python venv
   |
   +-- Install dependencies
   |
   +-- Configure Nginx
   |
   +-- Configure Systemd
   |
   +-- Start FutbolX
   |
   +-- Point DNS to new VPS
   |
   +-- Install SSL
   |
   +-- Test

---

Step 1 — Connect to the new VPS

🟢 COPY & RUN

ssh root@NEW_SERVER_IP

🟡 EDIT THIS

Replace:

NEW_SERVER_IP

with the new VPS IP.

---

Step 2 — Update the VPS

🟢 COPY & RUN

apt update && apt upgrade -y

---

Step 3 — Install all required software

🟢 COPY & RUN

apt install -y git python3 python3-pip python3-venv nginx ffmpeg curl wget unzip zip nano sudo ca-certificates certbot python3-certbot-nginx dnsutils

---

Step 4 — Clone FutbolX

🟢 COPY & RUN

cd /opt

Then:

🟢 COPY & RUN

git clone https://github.com/epltv1/FutbolX-Media-Server.git

Enter:

🟢 COPY & RUN

cd /opt/FutbolX-Media-Server

---

Step 5 — Create HLS directory

🟢 COPY & RUN

mkdir -p /var/www/futbolx/hls

Then:

🟢 COPY & RUN

chown -R www-data:www-data /var/www/futbolx

Then:

🟢 COPY & RUN

chmod -R 755 /var/www/futbolx

---

Step 6 — Create Python environment

🟢 COPY & RUN

cd /opt/FutbolX-Media-Server

python3 -m venv venv

Activate:

source venv/bin/activate

Upgrade pip:

pip install --upgrade pip

---

Step 7 — Install Python dependencies

🟢 COPY & RUN

pip install -r requirements.txt

---

Step 8 — Configure Nginx

🔵 CREATE / EDIT FILE

nano /etc/nginx/sites-available/futbolx

🟢 COPY & PASTE

Copy the entire Nginx configuration from Section 16.

If your domain changed, update the domain names first.

Save:

CTRL+O
ENTER
CTRL+X

Enable:

🟢 COPY & RUN

rm -f /etc/nginx/sites-enabled/default

Then:

ln -s /etc/nginx/sites-available/futbolx /etc/nginx/sites-enabled/futbolx

Test:

nginx -t

Reload:

systemctl reload nginx

---

Step 9 — Configure Systemd

🔵 CREATE / EDIT FILE

nano /etc/systemd/system/futbolx.service

🟢 COPY & PASTE

Copy the entire Systemd configuration from Section 18.

Save:

CTRL+O
ENTER
CTRL+X

Reload:

🟢 COPY & RUN

systemctl daemon-reload

Enable:

systemctl enable futbolx

Start:

systemctl start futbolx

Check:

systemctl status futbolx

---

Step 10 — Move DNS

Go to your domain provider.

Change the A record from the old VPS IP to the new VPS IP.

Example:

OLD VPS
1.2.3.4

NEW VPS
5.6.7.8

Change:

futbol-x.xyz → 5.6.7.8

Verify:

🟢 COPY & RUN

dig futbol-x.xyz

The result should show the new VPS IP.

---

Step 11 — Configure SSL

After DNS points to the new VPS:

🟢 COPY & RUN

certbot --nginx -d futbol-x.xyz -d www.futbol-x.xyz

Then test renewal:

🟢 COPY & RUN

certbot renew --dry-run

---

Step 12 — Final migration test

Check FutbolX:

🟢 COPY & RUN

systemctl status futbolx

Check Nginx:

🟢 COPY & RUN

systemctl status nginx

Test API:

🟢 COPY & RUN

curl https://futbol-x.xyz/api/health

Open:

https://futbol-x.xyz/

Test stream creation, starting, stopping, and M3U8 playback.

---

35. Backing Up FutbolX

The application code is stored in GitHub.

Check the repository:

🟢 COPY & RUN

cd /opt/FutbolX-Media-Server
git status

If you have local code changes that should be preserved:

🟢 COPY & RUN

git add .

Then:

git commit -m "Update FutbolX"

Then:

git push

---

Backup Nginx

Create backup directory:

🟢 COPY & RUN

mkdir -p /root/futbolx-backup

Copy Nginx configuration:

🟢 COPY & RUN

cp /etc/nginx/sites-available/futbolx /root/futbolx-backup/

---

Backup Systemd

🟢 COPY & RUN

cp /etc/systemd/system/futbolx.service /root/futbolx-backup/

---

Backup custom project configuration

If you have important local configuration files:

🟢 COPY & RUN

cp -r /opt/FutbolX-Media-Server /root/futbolx-backup/

⚠️ IMPORTANT

The Python "venv" normally does not need to be backed up.

It can be recreated on the new VPS.

---

36. Restoring FutbolX

On the new VPS:

Clone the repository:

🟢 COPY & RUN

cd /opt

git clone https://github.com/epltv1/FutbolX-Media-Server.git

Create the Python environment:

🟢 COPY & RUN

cd /opt/FutbolX-Media-Server

python3 -m venv venv

Activate:

source venv/bin/activate

Install:

pip install -r requirements.txt

Create HLS directory:

mkdir -p /var/www/futbolx/hls

Restore Nginx:

🟢 COPY & RUN

cp /root/futbolx-backup/futbolx /etc/nginx/sites-available/futbolx

Enable:

ln -s /etc/nginx/sites-available/futbolx /etc/nginx/sites-enabled/futbolx

Restore Systemd:

🟢 COPY & RUN

cp /root/futbolx-backup/futbolx.service /etc/systemd/system/futbolx.service

Reload:

systemctl daemon-reload

Enable:

systemctl enable futbolx

Start:

systemctl start futbolx

Test Nginx:

nginx -t

Restart Nginx:

systemctl restart nginx

---

37. Troubleshooting

FutbolX will not start

Check:

🟢 COPY & RUN

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

🟢 COPY & RUN

ss -lntp | grep 8000

Then:

curl http://127.0.0.1:8000/api/health

If it fails:

systemctl status futbolx

And:

journalctl -u futbolx -n 100 --no-pager

---

Nginx is not working

🟢 COPY & RUN

nginx -t

Then:

systemctl status nginx

Check errors:

tail -100 /var/log/nginx/error.log

---

Domain does not open

Check DNS:

🟢 COPY & RUN

dig futbol-x.xyz

The returned IP must match your VPS.

Check Nginx:

systemctl status nginx

Check firewall:

ufw status

Ports 80 and 443 should be allowed.

---

SSL does not work

Check certificates:

🟢 COPY & RUN

certbot certificates

Test renewal:

certbot renew --dry-run

Check Nginx:

nginx -t

---

HLS stream does not work

Check HLS directory:

🟢 COPY & RUN

ls -lah /var/www/futbolx/hls

Check a stream:

🟡 EDIT THIS

Replace "STREAM_ID" with the actual stream ID.

ls -lah /var/www/futbolx/hls/STREAM_ID

You should see files similar to:

index.m3u8
segment1.ts
segment2.ts

Check FutbolX logs:

journalctl -u futbolx -f

Check FFmpeg:

ps aux | grep ffmpeg

---

FFmpeg is not running

🟢 COPY & RUN

ps aux | grep ffmpeg

Check logs:

journalctl -u futbolx -n 100 --no-pager

Check FFmpeg:

which ffmpeg

ffmpeg -version

---

Stream stops unexpectedly

Check:

🟢 COPY & RUN

journalctl -u futbolx -f

Check RAM:

free -h

Check disk:

df -h

Check CPU:

top

Also verify that the media source is still available and that you are authorized to use it.

---

VPS disk is full

Check disk:

🟢 COPY & RUN

df -h

Check HLS storage:

du -sh /var/www/futbolx/hls

Check project:

du -sh /opt/FutbolX-Media-Server

Check journal storage:

journalctl --disk-usage

If necessary, remove old system logs:

journalctl --vacuum-time=7d

---

38. Useful Commands

FutbolX

Start

systemctl start futbolx

Stop

systemctl stop futbolx

Restart

systemctl restart futbolx

Status

systemctl status futbolx

Enable startup

systemctl enable futbolx

Disable startup

systemctl disable futbolx

Live logs

journalctl -u futbolx -f

---

Nginx

Start

systemctl start nginx

Stop

systemctl stop nginx

Restart

systemctl restart nginx

Reload

systemctl reload nginx

Status

systemctl status nginx

Test configuration

nginx -t

---

FFmpeg

Version

ffmpeg -version

Location

which ffmpeg

Running processes

ps aux | grep ffmpeg

---

Python

Version

python3 --version

Activate environment

cd /opt/FutbolX-Media-Server
source venv/bin/activate

Install requirements

pip install -r requirements.txt

---

Server resources

CPU / processes

top

Memory

free -h

Disk

df -h

HLS disk usage

du -sh /var/www/futbolx/hls

Network ports

ss -lntp

VPS uptime

uptime

---

39. Project Structure

The project should approximately look like:

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

When a stream is stopped, FutbolX should remove its HLS files.

---

40. Production Architecture

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

Systemd:

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

- HTTPS
- Reverse proxy
- HLS delivery
- Domain routing

FastAPI handles:

- API
- Dashboard backend
- Stream management
- Viewer management
- Health information

FFmpeg handles:

- Media input
- HLS generation
- Segment creation

---

41. Security Notes

Keep FastAPI private

FastAPI listens on:

127.0.0.1:8000

Do not expose port 8000 directly to the internet.

Nginx should be the public entry point.

---

Use HTTPS

Production access should use:

https://

instead of:

http://

---

Keep the VPS updated

🟢 COPY & RUN

apt update && apt upgrade -y

---

Protect SSH

Use SSH keys where possible.

Do not expose unnecessary ports.

Check:

🟢 COPY & RUN

ufw status

---

Monitor disk space

HLS streams continuously create media segments.

Check regularly:

🟢 COPY & RUN

df -h

And:

du -sh /var/www/futbolx/hls

---

42. Complete Fresh VPS Installation

This is the quick installation path.

Use this when you already understand the detailed instructions above.

---

STEP 1 — Update VPS

🟢 COPY & RUN

apt update && apt upgrade -y

---

STEP 2 — Install software

🟢 COPY & RUN

apt install -y git python3 python3-pip python3-venv nginx ffmpeg curl wget unzip zip nano sudo ca-certificates certbot python3-certbot-nginx dnsutils

---

STEP 3 — Clone FutbolX

🟢 COPY & RUN

cd /opt
git clone https://github.com/epltv1/FutbolX-Media-Server.git
cd /opt/FutbolX-Media-Server

---

STEP 4 — Create HLS directory

🟢 COPY & RUN

mkdir -p /var/www/futbolx/hls
chown -R www-data:www-data /var/www/futbolx
chmod -R 755 /var/www/futbolx

---

STEP 5 — Create Python environment

🟢 COPY & RUN

cd /opt/FutbolX-Media-Server
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

---

STEP 6 — Test FutbolX

🟢 COPY & RUN

uvicorn server.main:app --host 127.0.0.1 --port 8000

Open another SSH session.

🟢 COPY & RUN

curl http://127.0.0.1:8000/api/health

Stop the test server with:

CTRL+C

---

STEP 7 — Configure Nginx

🔵 CREATE / EDIT FILE

nano /etc/nginx/sites-available/futbolx

🟢 COPY & PASTE

Copy the complete Nginx configuration from Section 16.

Save:

CTRL+O
ENTER
CTRL+X

Enable:

🟢 COPY & RUN

rm -f /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/futbolx /etc/nginx/sites-enabled/futbolx
nginx -t
systemctl reload nginx

---

STEP 8 — Configure Systemd

🔵 CREATE / EDIT FILE

nano /etc/systemd/system/futbolx.service

🟢 COPY & PASTE

Copy the complete Systemd configuration from Section 18.

Save:

CTRL+O
ENTER
CTRL+X

Then:

🟢 COPY & RUN

systemctl daemon-reload
systemctl enable futbolx
systemctl start futbolx
systemctl status futbolx

---

STEP 9 — Configure firewall

🟢 COPY & RUN

ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable
ufw status

---

STEP 10 — Configure DNS

Point:

futbol-x.xyz
www.futbol-x.xyz

to:

YOUR_SERVER_IP

Verify:

🟢 COPY & RUN

dig futbol-x.xyz

---

STEP 11 — Install SSL

🟢 COPY & RUN

certbot --nginx -d futbol-x.xyz -d www.futbol-x.xyz

Test renewal:

certbot renew --dry-run

---

STEP 12 — Final test

🟢 COPY & RUN

curl https://futbol-x.xyz/api/health

Then open:

https://futbol-x.xyz/

---

43. Final Installation Checklist

Before considering the installation complete:

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
[ ] HLS directory created
[ ] Stream creation tested
[ ] Stream start tested
[ ] Stream stop tested
[ ] M3U8 URL tested
[ ] Stream health tested
[ ] Logs checked

---

44. Important Paths

FutbolX project

/opt/FutbolX-Media-Server

Python virtual environment

/opt/FutbolX-Media-Server/venv

HLS directory

/var/www/futbolx/hls

Nginx configuration

/etc/nginx/sites-available/futbolx

Enabled Nginx configuration

/etc/nginx/sites-enabled/futbolx

Systemd service

/etc/systemd/system/futbolx.service

Nginx logs

/var/log/nginx/

---

45. Quick Migration Formula

When moving FutbolX to a new VPS:

1. Get new VPS
       ↓
2. Update VPS
       ↓
3. Install Git/Python/FFmpeg/Nginx/Certbot
       ↓
4. Clone FutbolX
       ↓
5. Create /var/www/futbolx/hls
       ↓
6. Create Python venv
       ↓
7. Install requirements
       ↓
8. Configure Nginx
       ↓
9. Configure Systemd
       ↓
10. Start FutbolX
       ↓
11. Point DNS to new VPS
       ↓
12. Install SSL
       ↓
13. Test API
       ↓
14. Test dashboard
       ↓
15. Test stream

The GitHub repository contains the application code.

The VPS-specific setup mainly consists of:

Nginx
Systemd
DNS
SSL
HLS directory
Python virtual environment

Therefore, FutbolX can be rebuilt on a new VPS without manually rebuilding the application from scratch.

---

🏁 FINAL REMINDER

When using this README on a new VPS:

🟢 GREEN = COPY/RUN

If something is under:

🟢 COPY & RUN

paste it into SSH.

🔵 BLUE = CREATE FILE

If something says:

🔵 CREATE / EDIT FILE

open the specified file with "nano", then paste the complete configuration provided.

🟡 YELLOW = REPLACE

If something says:

🟡 EDIT THIS

replace the placeholder with your real domain, IP, stream source, or other value.

🔴 RED = EXPECTED RESULT

Do not copy it.

It only tells you what the VPS should return.

---

END

FutbolX Media Server — VPS Installation & Migration Guide
