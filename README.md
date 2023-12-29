# vgcBuilder
Showdown is the largest website for battle simulations, and has the amazing benefit of also exporting a miriad of usage stats at the end of each month that is publically available. I wanted to use the data to build something that may help in the team building process. This was initially designed for use with VGC, however it can be used with any format that smogon keeps stats on. 

## Methodology
The part that I honed in on is from the raw usage stats found at https://www.smogon.com/stats/{month}/moveset where it includes a stat on the most used teammates for any given pokemon. Using this relational aspect of the data, I figured I could create something that goes from one pokemon to another finding the _best_ teammates

## Algorithm
The algorithm at the moment is fairly basic, and I will go into the limitations of it in another section. But the following is a explination of the process it goes towards.

The method of finding the _best_, or more aptly described _most logical_, teammates is by taking the aggregate percentages of teammate liklihood, and simply using the most likely one that is not already on the team. Let me show an example using the stats for [Gen 9 VGC 11/2023](https://www.smogon.com/stats/2023-11/moveset/gen9vgc2023regulationebo3-1760.txt). Lets say we start with the first 2 members being Amoonguss and Flutter Mane. The program will go through and add up all the teammates percentages and then store them. For the afermentioned starting two, the aggregation of percentages would look like the following:
```
[('Iron Hands', 102.32),
 ('Urshifu-Rapid-Strike', 78.11699999999999),
 ('Landorus-Therian', 67.803),
 ('Tornadus', 60.763999999999996),
 ('Heatran', 48.692),
 ('Arcanine-Hisui', 44.882),
 ('Flutter Mane', 43.896),
 ('Chien-Pao', 37.601),
 ('Chi-Yu', 34.14),
 ('Rillaboom', 30.284),
 ('Gholdengo', 28.363),
 ('Roaring Moon', 25.327),
 ('Ogerpon-Wellspring', 18.26),
 ('Amoonguss', 15.382)]
```
It would then go through this list, which is sorted with the highest values at the top, and pick the highest rated pokemon that isn't on the team, in this case Iron Hands. The team would then look like the following: `['Amoonguss', 'Flutter Mane', 'Iron Hands']`. After adding Iron Hands to the team, it would then get it's teammate percentages, and add them in to this list, which would result in the following list:
```
[('Iron Hands', 102.32),
 ('Urshifu-Rapid-Strike', 102.03199999999998),
 ('Landorus-Therian', 101.90199999999999),
 ('Flutter Mane', 85.07900000000001),
 ('Tornadus', 80.25399999999999),
 ('Heatran', 73.971),
 ('Arcanine-Hisui', 65.543),
 ('Gholdengo', 45.659),
 ('Amoonguss', 42.721),
 ('Roaring Moon', 41.693),
 ('Ogerpon-Wellspring', 40.579),
 ('Chien-Pao', 37.601),
 ('Chi-Yu', 34.14),
 ('Rillaboom', 30.284),
 ('Sinistcha', 13.261)]
 ```
 Note how even though Iron Hands added 0 points to his own score, it is still the top. Since he is already in the team, it would go to the next highest candidate, Urshifu-Rapid-Strike. It will then do the same thing where it adds it to the team, adds its teammate percentages, and continues to go through the process until it makes the final team of:
 `['Amoonguss', 'Flutter Mane', 'Iron Hands', 'Urshifu-Rapid-Strike', 'Tornadus', 'Gholdengo']`

This can be done for 1 or more amount of starting members. So for example, lets say I wanted to make a rain team consisting of Pelipper, Poliwrath, and Beartic, it would come up with the following completed team:
`['Pelipper', 'Poliwrath', 'Beartic', 'Iron Hands', 'Flutter Mane', 'Tornadus']`

## Limitations
This is based soley on teammate usage stats, which brings up a few limitations, which potentially could be sorted out in the future.

#### Pokemon Usage
This has no concept of team structure. It will only return teams based on pokemon that _generally_ go together. For example with an Amoonguss and Flutter Mane, Iron Hands would _generally_ be a good teammate, but it doesn't know why. This leads into the next limitation

#### Team Structure
The algorithm has no idea why each pokemon works together, which means that it also doesn't know what a team is missing. For example you could have a huge hole because you lack any kind of defensive counterplay, simply because how the numbers work out it could only be looking at offensive pokemon. This is not meant to be a solution that builds perfect teams, but instead a tool that could get you a starting place that you can tweak and refine

#### Old Data
The program takes advantage of the fact that showdown releases all of their stats on a monthly basis. This however means that the data could be outdated as metas change. This also means that as new regulations start, it will be unusable for a month until some data for the new regulation is released. 

## How to Use
Using this really goes into 2 steps. First you have prepare the database to be used. To do so simply download the file you desire to start from with https://www.smogon.com/stats/{month}/moveset/. It is important that you use the text file in the moveset repository.

#### Create Database

After downloading the file, run the following command while inside the service folder:
`python3 loadDB.py {database_name} {sourcefile_name}`

For example, using the file structure I have in the repo, after saving the text file for [Gen 9 VGC 11/2023](https://www.smogon.com/stats/2023-11/moveset/gen9vgc2023regulationebo3-1760.txt) I would run the following:
`python3 loadDB.py ../data/11-2023/vgc/vgc11-2023.json ../data/11-2023/vgc/gen9vgc2023regulatione-1760.txt`

This will create a json file that will be loaded as the database.

#### Create Team

Now that a useable database exists, you can now create a team. Do do so you would run the following command from the home folder:
`python3 main.py {database} {teammembers}`
The teammembers that you want to use must be seperated by a space. If the Pokemon name already contains a space in it, for example Flutter Mane, you must inclose it in quotes. For example to create the team for Amoonguss and Flutter Mane using the database generate above, I would run the following command:
`python3 main.py data/11-2023/vgc/vgc11-2023.json Amoonguss "Flutter Mane"`
 
Which gives the output of: `['Amoonguss', 'Flutter Mane', 'Iron Hands', 'Urshifu-Rapid-Strike', 'Tornadus', 'Gholdengo']`

**Note**: This readme is written with a unix system in mind. I believe it should work the same for python, however it is untested.

## ToDo

- Explore different algorithms
- Create an API that can be called so you don't have to run it locally
- Create Github Actions to run program using existing databases

This is an ongoing project, so I will update the README as things change. If you would like to collaborate on this, feel free to fork or reach out to me on twitter.