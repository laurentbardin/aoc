class Card:

    def __init__(self, label):
        assert(label in 'AKQJT98765432')

        self.label = label
        match label:
            case 'A':
                self.value = 14
            case 'K':
                self.value = 13
            case 'Q':
                self.value = 12
            case 'J':
                self.value = 11
            case 'T':
                self.value = 10
            case _:
                self.value = int(label)


    def __eq__(self, other):
        return self.label == other.label
    def __ne__(self, other):
        return self.label != other.label

    def __lt__(self, other):
        return self.value < other.label
    def __le__(self, other):
        return self.value <= other.label
    def __gt__(self, other):
        return self.value > other.label
    def __ge__(self, other):
        return self.value >= other.label

