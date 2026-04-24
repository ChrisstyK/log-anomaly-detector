import csv
import random
from datetime import datetime

ip_good = ["192.168.1.1", "192.168.1.2"]
ip_bad = "185.220.101.1"

def write(ip, action, status):
    with open("logs.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), ip, action, status])

def normal():
    for _ in range(20):
        write(random.choice(ip_good), "visit", "success")

def brute():
    for _ in range(20):
        write(ip_bad, "login", "failed")

def slow():
    for _ in range(10):
        write(ip_bad, "login", "failed")
        write(ip_bad, "visit", "success")

def weird():
    for _ in range(10):
        write(ip_bad, "download", "success")
        write(ip_bad, "login", "failed")

print("1 normal | 2 brute | 3 slow | 4 weird")
c = input()

if c == "1": normal()
elif c == "2": brute()
elif c == "3": slow()
elif c == "4": weird()