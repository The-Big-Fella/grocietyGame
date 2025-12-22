import time

class Timer:
    def __init__(self):
        self.start_time = time.time()

    def elapsed_time(self):
        return int(time.time() - self.start_time)

    def countdown(self, count):
        for x in range (1, count):
            time.sleep(1)
            print(x)