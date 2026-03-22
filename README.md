# Home Security Bot

A Telegram controlled security robot built with a Raspberry Pi 4B, Arduino Uno, and a Logitech C525 webcam. Control the car remotely, take snapshots, and watch a live camera feed from anywhere via Tailscale.

## Features

- Remote movement control via Telegram (`/forward`, `/backward`, `/left`, `/right`, `/stop`)
- Snapshot on demand (`/snapshot`) which sends a 1080p photo accessible on Telegram
- Live camera stream (`/stream`) which is made accessible from anywhere via Tailscale
- Auto-starts on boot via systemd

## Hardware

- Raspberry Pi 4B (4GB RAM)
- Arduino Uno with motor shield (M1: pins 3, 5 — M2: pins 6, 11)
- Logitech C525 USB webcam (with built-in mic)
- 2x DC motors
- Ultrasonic sensor, IR sensor, LDR, buzzer, LEDs

## Software Stack

- Python 3 (Raspberry Pi OS)
- `python-telegram-bot` — Telegram bot framework
- `pyserial` — Serial communication with Arduino
- `opencv-python` — Camera capture
- `flask` — Live MJPEG stream server
- `tailscale` — Secure remote access

## Setup

### 1. Install dependencies

```bash
pip install python-telegram-bot pyserial opencv-python flask --break-system-packages
sudo apt install ffmpeg -y
```

### 2. Configure

Edit `bot.py` and set:
```python
TOKEN        = "your_telegram_bot_token"
TAILSCALE_IP = "your_tailscale_ip"
```

### 3. Arduino

Upload `arduino/main.ino` to your Arduino Uno using Arduino IDE.

Serial commands:
- `F` — forward (1 second)
- `B` — backward (1 second)
- `L` — turn left (0.6 seconds)
- `R` — turn right (0.6 seconds)
- `S` — stop

### 4. Udev rule (fixed Arduino port)

```bash
echo 'SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", ATTRS{serial}=="YOUR_SERIAL", SYMLINK+="arduino"' | sudo tee /etc/udev/rules.d/99-arduino.rules
sudo udevadm control --reload-rules && sudo udevadm trigger
```

### 5. Auto-start on boot

```bash
sudo nano /etc/systemd/system/homeSecBot.service
```

Paste:
```ini
[Unit]
Description=Home Security Bot
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/bot.py
WorkingDirectory=/home/pi
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable homeSecBot
sudo systemctl start homeSecBot
```

### 6. Tailscale

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
tailscale ip
```

Install Tailscale on your phone, sign in with the same account. Access the stream at `http://<tailscale-ip>:5000`.

## Telegram Commands

| Command | Description |
|---|---|
| `/start` | Check if bot is online |
| `/forward` | Move forward 1 second |
| `/backward` | Move backward 1 second |
| `/left` | Turn left |
| `/right` | Turn right |
| `/stop` | Stop motors |
| `/snapshot` | Take and send a photo |
| `/stream` | Get live stream URL |
