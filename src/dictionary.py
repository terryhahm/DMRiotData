import json

def createConstantData():
    # Modify Riot Constant Champion JSON file as following
    # {'Id': 'Name'}
    with open('Constant/champion.json', encoding='UTF8') as f:
        championPool = json.load(f)

    championDict = {}
    for champ in championPool["data"]:
        championDict[ championPool["data"][champ]["key"] ] = championPool["data"][champ]["name"]

    with open('src/Constant/modifiedChampion.json', 'w', encoding='UTF8') as out:
        json.dump(championDict, out)

    # Modify Riot Constant Spell JSON file as following
    # {'Id': 'Name'}
    with open('Constant/spell.json', encoding='UTF8') as f:
        spellPool = json.load(f)

    spellDict = {}
    for spell in spellPool["data"]:
        spellDict[ spellPool["data"][spell]["key"]  ] = spellPool["data"][spell]["name"]

    with open('src/Constant/modifiedSpell.json', 'w', encoding='UTF8') as out:
        json.dump(spellDict, out)

    # Modify Riot Constant Item JSON file as following
    # {'Id': 'Name'}
    with open('Constant/item.json', encoding='UTF8') as f:
        itemPool = json.load(f)

    itemDict = {}

    for key, val in itemPool["data"].items():
        itemDict[key] = val["name"]

    with open('src/Constant/modifiedItem.json', 'w', encoding='UTF8') as out:
        json.dump(itemDict, out)

    # Modify Riot Constant Runes JSON file as following
    # {'Id': 'Name'}
    with open('Constant/runesReforged.json', encoding='UTF8') as f:
        runePool = json.load(f)

    runeDict = {}
    for primaryStyle in runePool:
        runeDict[ str(primaryStyle["id"]) ] = primaryStyle["name"]
        for secondaryStyle in primaryStyle["slots"]:
            for secondary in secondaryStyle["runes"]:
                runeDict[ str(secondary["id"]) ] = secondary["name"]

    with open('src/Constant/modifiedRunes.json', 'w', encoding='UTF8') as out:
        json.dump(runeDict, out)

