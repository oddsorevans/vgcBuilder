#Use database to create team given list of pokemon
from tinydb import TinyDB, Query
from pprint import pprint

def createTeam(team: list, db: TinyDB):
    query = Query()
    teammateValues = {}
    #get current sums for pokemon in team
    for member in team:
        response = db.get(query.Name == member)
        teammateValues = updateTeamValues(teammateValues, response['Teammates'])
    
    #find new teammate, and add their teammates scores into list until team is full
    while len(team) < 6:
        # get list of highest value teammates
        sortedPairs = sorted(teammateValues.items(), key=lambda item: item[1], reverse=True)
        sortedTeammates = [key for key, value in sortedPairs]
        for teammate in sortedTeammates:
            if teammate not in team:
                team.append(teammate)
                response = db.get(query.Name == teammate)
                teammateValues = updateTeamValues(teammateValues, response['Teammates'])
                break
    return team
                
        
def updateTeamValues(current: dict, addition: list):
    for teammate in addition:
        if teammate[0] in current:
            current[teammate[0]] = current[teammate[0]] + float(teammate[1])
        else:
            current[teammate[0]] = float(teammate[1])
    return current
        
db = TinyDB('data/11-2023/vgc11-2023.json')
team = createTeam(['Heatran', 'Ogerpon-Wellspring'], db)
print(team)