import random
import pickle


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

        self.moveLearnDictionary = {}
        self.movePool

    def recalculateStats(self):
        self.neededXp = int(self.level * 100 * self.levelingMod)

        self.maxHp = int(self.level * self.hpGain * self.hpGene)
        self.atkStat = int(self.level * self.atkGain * self.atkGene)
        self.defStat = int(self.level * self.defGain * self.defGene)
        self.specialAtkStat = int(self.level * self.speAtkGain * self.speAtkGene)
        self.specialDefStat = int(self.level * self.speDefGain * self.speDefGene)
        self.speedStat = int(self.level * self.speGain * self.speGene)

    def level_up(self):
        """
        Deals with leveling up the emoji, involving raise level by one, as well as maybe improve stats
        and learn new moves
        """
        self.level += 1
        for move_name in self.moveLearnDictionary.items():
            if move_name[0] not in self.movePool:
                if move_name[1] <= self.level:
                    self.movePool.append(move_name[0])


class Trainer:
    def __init__(self, name, discord_id: int, beginner_emoji: Emoji, date_started: str):
        self.name = name
        self.beginner_emoji = beginner_emoji
        self.team = [self.beginner_emoji, None, None, None]
        self.achievements = []
        self.gym_badges = []
        self.wins = 0
        self.losses = 0
        self.emojis_caught = 0
        self.date_started = date_started
        self.id = discord_id
        self.role = 'player'  # If it is the name of one of the emoji type, the person is a gym leader

    def __str__(self):
        return self.name

    def add_w(self):
        """
        Any win adds should be through this method to check for achievements
        :returns achievement if you earned any, if not it returns None
        """
        achievement = None
        self.wins += 1
        if self.wins == 10:
            self.achievements.append("All that Ws")
            achievement = "All that Ws"
        if self.wins == 50:
            self.achievements.append("Apex Emoji")
            achievement = "Apex Emoji"
        return achievement

    def add_l(self):
        """
        Any loss adds should be through this method to check for achievements
        :returns achievement if you earned any, if not it returns None
        """
        achievement = None
        self.losses += 1
        if self.losses == 10:
            self.achievements.append("The bane of emojis")
            achievement = "The bane of emojis"
        if self.losses == 50:
            self.achievements.append("Did it for the achievement")
            achievement = "Did it for the achievement"

        return achievement

    def add_team(self, new_emoji: Emoji):
        """
        Add an emoji to team
        :returns True if team is full, False if it isn't, as well as achievement if it was achieved
        """
        achievement = None
        self.emojis_caught += 1

        if self.emojis_caught == 10:
            self.achievements.append("Emoji Collector")
            achievement = "Emoji Collector"
        if self.emojis_caught == 20:
            self.achievements.append("Emoji Hoarder")
            achievement = "Emoji Hoarder"
        if self.emojis_caught == 50:
            self.achievements.append("Emoji Trafficking")
            achievement = "Emoji Trafficking"

        for i in range(len(self.team)):
            if self.team[i] is None:
                self.team[i] = new_emoji
                return False, achievement

        return True, achievement


if __name__ == '__main__':
    with open('CompleteEmojiDex.dat', 'rb') as f:
        data_list = pickle.load(f)

    data_list[1412].level_up()
    print(data_list[1412].movePool, data_list[1412].level)
