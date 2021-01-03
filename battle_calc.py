import random
from load_data import emojimon


def damage_calculation(attackingEmoji: emojimon, defendingEmoji: emojimon, movesName):
    import pickle
    with open("CompleteMoveList.dat", "rb") as f:
        moveListTemp = pickle.load(f)

    with open("TypeChart2dArray.dat", "rb") as f:
        newData = pickle.load(f)

    for y in range(1, len(newData)):
        for x in range(1, len(newData)):
            if newData[y][0] == attackingEmoji.type and newData[0][x] == defendingEmoji.type:
                typeEffectiveness = newData[y][x]

    moveType = ""
    moveDam = 0
    moveAcc = 0.0
    hitType = ""

    universalDamageMod = 1.2

    for x in range(len(moveListTemp)):
        if movesName == moveListTemp[x].moveName:
            moveType = moveListTemp[x].moveType
            moveDam = moveListTemp[x].movePower
            moveAcc = moveListTemp[x].moveAccuracy
            hitType = moveListTemp[x].moveHitType

    stabMod = 1.0

    if moveType == attackingEmoji.type:
        stabMod = 1.2

    hit = random.uniform(0.0, 1.0)

    print(moveAcc)

    if hit > moveAcc:
        print("WHIFF!")
        return 0

    damageSway = random.uniform(0.8, 1.2)

    if hitType == "Physical":
        return int((((moveDam * (
                attackingEmoji.atkStat / defendingEmoji.defStat)) ** universalDamageMod) / 5) * typeEffectiveness * stabMod * damageSway)
    else:
        return int((((moveDam * (
                attackingEmoji.specialAtkStat / defendingEmoji.specialDefStat)) ** universalDamageMod) / 5) * typeEffectiveness * stabMod * damageSway)
