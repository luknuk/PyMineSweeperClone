class Field:
    def __init__(self):
        '''
        A Field

        In task 1, 2; self.value will contain * or the number 0-9.
        In task 3, self.value will contain a number for a k-colour.
        '''
        self.value = 0
        self.flag = False
        self.revealed = False

    def set_mine(self):
        self.value = "*"
    @property
    def is_mined(self):
        if self.value is "*":
            return True
        return
    def set_flag(self, b):
        # Expects boolean
        self.flag = b
    def increment(self):
        if self.value is not "*":
            self.value += 1
    def reveal(self):
        self.revealed = True
