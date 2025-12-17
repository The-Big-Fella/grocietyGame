import time

class Timer:
    # currenttime = float(0)

    def __init__(self):
        self.currenttime = time.time()

    def gettimer(self):
        print(self.currenttime)

    print(self.currenttime)