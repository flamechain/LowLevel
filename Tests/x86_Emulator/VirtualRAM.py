class Memory:
    def __init__(self):
        self.Data = []
        for i in range(16**4):
            self.Data.append(0x00)
