class Player(object):
    name = ""
    position = ""
    draftAdvice = ""
    ranking = ""
    age = ""
    inFullList = False
    drafted = False

    def __init__(self, name, position, draftAdvice, ranking, age, inFullList, drafted):
        self.name = name
        self.position = position
        self.draftAdvice = draftAdvice
        self.age = age
        self.ranking = ranking
        self.inFullList = inFullList
        self.drafted = drafted