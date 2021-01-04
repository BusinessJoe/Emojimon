import random
import json


class move:
    moveName = ""
    moveType = ""
    movePower = 0
    moveAccuracy = 0
    moveEffect = ""
    moveHitType = ""


class Emoji:
    # basic information
    name = ""
    type = ""
    emojiNumber = 0
    imageReference = ""
    level = 0
    evolution = ""  # Name of evolved emoji
    evolutionLevel = 0

    # xp and leveling
    currentXp = 0
    neededXp = 0
    levelingMod = 1.0

    # Genes and stats gained upon level up, range from 0.2 to 5 naturally, stats are calculated with this and genes
    hpGain = 1.0;
    atkGain = 1.0
    defGain = 1.0
    speAtkGain = 1.0
    speDefGain = 1.0
    speGain = 1.0

    hpGene = 1.0  # range of 1 to 2
    atkGene = 1.0
    defGene = 1.0
    speAtkGene = 1.0
    speDefGene = 1.0
    speGene = 1.0

    # stats
    currentHp = 0
    attackMod = 1.0
    defenseMod = 1.0
    specialAttackMod = 1.0
    specialDefenseMod = 1.0
    speedMod = 1.0
    dodgeMod = 1.0

    # stat calc and genes, these are used in conjunction with the above
    maxHp = 0
    atkStat = 0
    defStat = 0
    specialAtkStat = 0
    specialDefStat = 0
    speedStat = 0
    dodgeChance = 1.0

    # moves
    move1 = ""
    move2 = ""
    move3 = ""
    move4 = ""

    movePool = []
    moveLearnDictionary = {}

    def __init__(self, indexNum):
        self.emojiNumber = indexNum
        self.imageReference = "Emoji" + indexNum.__str__()
        self.name = RandomWord()
        self.type = RandomType()
        self.level = random.randint(1, 50)
        # Evolutions will be handled out of initialization
        self.evolution = ""
        self.evolutionLevel = 0

        self.levelingMod = random.uniform(1.0, 3.0)
        self.neededXp = int(self.level * 100 * self.levelingMod)

        self.hpGain = random.uniform(0.2, 5)
        self.atkGain = random.uniform(0.2, 5)
        self.defGain = random.uniform(0.2, 5)
        self.speAtkGain = random.uniform(0.2, 5)
        self.speDefGain = random.uniform(0.2, 5)
        self.speGain = random.uniform(0.2, 5)

        self.hpGene = random.uniform(1, 2)
        self.atkGene = random.uniform(1, 2)
        self.defGene = random.uniform(1, 2)
        self.speAtkGene = random.uniform(1, 2)
        self.speDefGene = random.uniform(1, 2)
        self.speGene = random.uniform(1, 2)

        self.maxHp = int(self.level * self.hpGain * self.hpGene)
        self.atkStat = int(self.level * self.atkGain * self.atkGene)
        self.defStat = int(self.level * self.defGain * self.defGene)
        self.specialAtkStat = int(self.level * self.speAtkGain * self.speAtkGene)
        self.specialDefStat = int(self.level * self.speDefGain * self.speDefGene)
        self.speedStat = int(self.level * self.speGain * self.speGene)
        self.dodgeChance = random.uniform(1.0, 5.0)

        self.moveLearnDictionary = MoveListDict()

    def recalculateStats(self):
        self.neededXp = int(self.level * 100 * self.levelingMod)

        self.maxHp = int(self.level * self.hpGain * self.hpGene)
        self.atkStat = int(self.level * self.atkGain * self.atkGene)
        self.defStat = int(self.level * self.defGain * self.defGene)
        self.specialAtkStat = int(self.level * self.speAtkGain * self.speAtkGene)
        self.specialDefStat = int(self.level * self.speDefGain * self.speDefGene)
        self.speedStat = int(self.level * self.speGain * self.speGene)

