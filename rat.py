# Graeson Brickner
# U1 Lab 1
# Biggest rat project

class Rat:
    def __init__(self, sex, weight):
        self.sex = sex
        self.weight = weight
        self.litters = 0

    def __str__(self):
        return f"Rat: {self.sex}, {self.weight}g"

    def __repr__(self):
        return f"{self.weight}g"

    def getWeight(self):
        return self.weight
    
    def setWeight(self, newWeight):
        self.weight = newWeight
    
    def getSex(self):
        return self.sex
    
    def canBreed(self):
        return self.litters < 5
    
    def incrementLitters(self):
        self.litters += 1
    
    def __lt__(self, other):
        return self.weight < other.weight
    
    def __gt__(self, other):
        return self.weight > other.weight
    
    def __le__(self, other):
        return self.weight <= other.weight
    
    def __ge__(self, other):
        return self.weight >= other.weight
    
    def __eq__(self, other):
        return self.weight == other.weight