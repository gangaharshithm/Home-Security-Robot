import time
import serial
import asyncio
import cv2
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import stream

# ── Config ────────────────────────────────────────────────────────────────────
TOKEN        = "YOUR_TELEGRAM_BOT_TOKEN"
TAILSCALE_IP = "YOUR_TAILSCALE_IP"
# ──────────────────────────────────────────────────────────────────────────────

# Serial connection to Arduino
ser = serial.Serial('/dev/arduino', 9600, timeout=1)

# Camera setup
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
time.sleep(0.05)
stream.set_camera(cap)

# Start live stream in background thread
threading.Thread(target=stream.start_stream, daemon=True).start()


# ── Bot command handlers ───────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Home Security Bot online!")

async def forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ser.write(b'F')
    await update.message.reply_text("Moving forward")

async def backward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ser.write(b'B')
    await update.message.reply_text("Moving backward")

async def left(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ser.write(b'L')
    await update.message.reply_text("Turning left")

async def right(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ser.write(b'R')
    await update.message.reply_text("Turning right")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ser.write(b'S')
    await update.message.reply_text("Stopped")

async def snapshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Taking snapshot...")
    for _ in range(10):   # warm up camera exposure
        cap.read()
    ret, frame = cap.read()
    if ret:
        cv2.imwrite('/home/pi/snapshot.jpg', frame)
        await update.message.reply_photo(photo=open('/home/pi/snapshot.jpg', 'rb'))
    else:
        await update.message.reply_text("Failed to capture image")

async def streamcmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Live stream: http://{TAILSCALE_IP}:5000")


# ── Register handlers and start bot ───────────────────────────────────────────

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start",    start))
app.add_handler(CommandHandler("forward",  forward))
app.add_handler(CommandHandler("backward", backward))
app.add_handler(CommandHandler("left",     left))
app.add_handler(CommandHandler("right",    right))
app.add_handler(CommandHandler("stop",     stop))
app.add_handler(CommandHandler("snapshot", snapshot))
app.add_handler(CommandHandler("stream",   streamcmd))

print("Bot running...")
app.run_polling()
