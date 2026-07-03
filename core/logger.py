import logging
from logging.handlers import TimedRotatingFileHandler
import os
os.makedirs("logs",exist_ok=True)
# os.makedirs → Folder banao
# exist_ok=True → Agar already hai → Error mat do

# LOGGER: Diary likhne wala
logger=logging.getLogger("todos")
logger.setLevel(logging.INFO)

# getLogger("todos") --> todos naam ka logger
# setLevel(INFO) --> INFO aur upar sab log kro DEBUG ignore kro

# FORMATTER: Diary likhne ka format 
formatter=logging.Formatter(
    "%(asctime)s - %(levelname)s -%(message)s"
)

# %(asctime)s   → Time: "2024-01-15 10:30:00"
# %(levelname)s → Level: "INFO" ya "ERROR"
# %(message)s   → Message: "User logged in"

# Output:
# "2024-01-15 10:30:00 - INFO - User logged in"

# 3. HANDLER: Kaha likhe log --> Terminal ya file mei ya dono places pe

# Terminal pe dikhane k liye

console_handler=logging.StreamHandler()
console_handler.setFormatter(formatter)
# StreamHandler → Terminal mein dikhao
# setFormatter  → Wahi format use karo(jo upar define kiya hai)

# File mei save Kro
# Python ke built-in logging module ke andar ek sub-module hai handlers, usme se TimedRotatingFileHandler class import kar rahe hain. Ye handler ka kaam hai logs ko file mein likhna, lekin ek twist ke saath — ye time ke basis par log file ko "rotate" karta hai, matlab purani file ko rename karke nayi fresh file shuru kar deta hai. Isse ek hi file bahut badi nahi hoti.

file_handler=TimedRotatingFileHandler(
    filename="logs/app.log",
    when="h",
    interval=1,
    backupCount=5,delay=True
)
file_handler.setFormatter(formatter)

# filename="logs/app.log" — Logs is file mein likhe jaayenge. Dhyan rahe, logs folder pehle se exist karna chahiye, warna FileNotFoundError aayega. Handler file to bana lega, par folder nahi banata.
# when="h" — Rotation kis unit par hoga, ye batata hai. "h" matlab hours. Aur options bhi hote hain: "s" (seconds), "m" (minutes), "d" (days), "midnight" (har raat 12 baje), "w0" se "w6" (weekday, w0 = Monday).
# interval=1 — when ke saath milkar kaam karta hai. when="h" aur interval=1 ka matlab: har 1 ghante mein rotation hogi. Agar interval=6 hota to har 6 ghante mein.
# backupCount=24 — Maximum kitni purani (rotated) files rakhni hain. Yahan 24 hai, matlab 24 purani files rakhega, uske baad sabse purani file automatically delete ho jaayegi. Kyunki har ghante rotate ho raha hai aur 24 backups hain, to effectively aapke paas pichle 24 ghanton (1 din) ke logs rahenge.


# 4. Handlers logger se jodo
logger.addHandler(console_handler) # terminal k liye
logger.addHandler(file_handler) # File k liye