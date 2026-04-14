import csv
import random
from datetime import datetime

ips = [
    "192.168.1.1",
    "192.168.1.2",
    "10.0.0.5",
    "45.33.32.1"  # IP suspect
]

actions = ["login", "download"]
statuses = ["success", "failed"]

with open("logs.csv", "a", newline="") as file:
    writer = csv.writer(file)

    for _ in range(10):
        timestamp = datetime.now()
        ip = random.choice(ips)
        action = random.choice(actions)
        status = random.choice(statuses)

        writer.writerow([timestamp, ip, action, status])

print("Loguri generate!")