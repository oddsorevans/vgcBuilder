#Load the db from text file to database
from tinydb import TinyDB
from pathlib import Path
import os
import sys

#Take data from raw usage stats found at https://www.smogon.com/stats/{month}/moveset and insert it into database
def create_new(file_name: str, source: str):
    if not os.path.isfile(file_name):
        # create
        db = TinyDB(file_name)
        cleaned = cleanData(source)
        loadData(db, cleaned)
        os.remove(cleaned)
    else:
        print(f"{file_name} already exists. Please define a new file")

#This script only uses the Teammates section, so removing the unused extra before processing        
def cleanData(source: str):
    #sections for logic to occur
    cleaned = Path(source).stem + '_cleaned.txt'
    start = True
    underName = False
    teammates = False
    end = False
    with open(source, 'r') as file:
        lines = file.readlines()
    with open(cleaned, 'w') as file:
        for line in lines:
            if start:
                if not line.startswith(' +--'):
                    file.write(clean_line(line))
                    start = False
                    underName = True
            elif underName:
                if line.startswith(' | Teammates'):
                    underName = False
                    teammates = True
            elif teammates:
                if line.startswith(' +--'):
                    teammates = False
                    end = True
                else:
                    file.write(clean_line(line))
            elif end:
                if line.startswith(' +--'):
                    file.write('\n')
                    end = False
                    start = True
    return cleaned
                
#load cleaned data into db
def loadData(db: TinyDB, source: str):
    with open(source, 'r') as file:
        lines = file.readlines()
    
    pokemon = {}
    teammates = []
    #sections
    name = True
    for line in lines:
        if name:
            pokemon['Name'] = line.strip('\n')
            name = False
        else:
            if line != '\n':
                formatted = line.strip('\n').rsplit(' ', 1)
                formatted[1] = formatted[1].rstrip('%')
                teammates.append(formatted)
            else: 
                pokemon['Teammates'] = teammates
                db.insert(pokemon)
                pokemon = {}
                teammates = []
                name = True

def clean_line(line: str):
    # Stripping off the leading and trailing '|' characters and spaces
    cleaned_line = line.strip('| \n') + '\n'
    return cleaned_line

#take command line arguments and run create_new
database_name = sys.argv[1]
source = sys.argv[2]
create_new(database_name, source)