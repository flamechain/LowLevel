class Memory:
    def __init__(self, size=65536):
        self.Data = []

        for i in range(size):
            self.Data.append(0x00)
