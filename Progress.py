class Progress:
    def __init__(self, data):
        self.prep = data[0]
        self.throw = data[1]
        self.debat = data[2]
        self.trim = data[3]
        self.assemble = data[4]
        self.polish = data[5]
        self.data = data

    def __iter__(self):
        return iter(self.data)

    def get_sum(self):
        return self.prep + self.throw + self.debat + self.trim + self.assemble + self.polish
