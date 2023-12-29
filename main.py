# To run the file, first pass in the filepath to the database to be used, and then the pokemon you want to include in the team. If the pokemon's name includes a space, surround it with quotes.
import sys
from tinydb import TinyDB
import service.teambuilder as teambuilder

db = TinyDB(sys.argv[1])
team = sys.argv[2:]

result = teambuilder.createTeam(team, db)

print(result)