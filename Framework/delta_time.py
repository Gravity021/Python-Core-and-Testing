import time

class DeltaTime:
    def __init__(self):
        self.last_time = time.time()
        self.dt = 1
    
    def update(self):
        self.dt = time.time() - self.last_time
        self.dt *= 60
        # self.dt = int(self.dt)
        self.last_time = time.time()