import csv
import random
import os
from datetime import datetime

# IP-uri normale
normal_ips = [
    "192.168.1.1",
    "192.168.1.2"
]

# IP atacator
attacker_ip = "185.220.101.1"

actions = ["login", "download"]

# =========================
# SCRIERE LOG
# =========================
def write_log(ip, action, status):
    file_exists = os.path.isfile("logs.csv")

    with open("logs.csv", "a", newline="") as file:
        writer = csv.writer(file)

        # header dacă fișierul e nou
        if not file_exists:
            writer.writerow(["timestamp", "ip", "action", "status"])

        writer.writerow([datetime.now(), ip, action, status])


# =========================
# TRAFIC NORMAL
# =========================
def normal_activity():
    for _ in range(10):
        ip = random.choice(normal_ips)
        action = random.choice(actions)
        status = "success"
        write_log(ip, action, status)


# =========================
# ATAC BRUTE FORCE
# =========================
def brute_force_attack():
    for _ in range(20):  # mai multe pentru claritate
        write_log(attacker_ip, "login", "failed")


# =========================
# MENIU
# =========================
print("1 - Trafic normal")
print("2 - Atac brute force")

choice = input("Alege scenariu: ")

if choice == "1":
    normal_activity()
    print("Trafic normal generat")

elif choice == "2":
    brute_force_attack()
    print("Atac generat")

else:
    print("Optiune invalida")