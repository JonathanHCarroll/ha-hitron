import random

class HitronClient:
    def __init__(self, host="192.168.0.1", username="admin", password="password"):
        self.host = host
        self.username = username
        self.password = password

    def reboot(self):
        # your code to send reboot command
        pass

    def get_status(self):
        return {
            "uptime": f"{random.randint(1, 5)} days",
            "signal_strength": -60 - random.randint(0, 10),
            "connected": random.choice([True, False]),
        }