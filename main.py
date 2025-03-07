import time 
import sys
from scraper import *
from csvSaver import saveToCsvLeague
from dbSaver import saveToLeagueDb
from cleaner import cleanLeagueData


#start of program
start = time.time()

#initialising database names
LEAGUE_DB_NAME = "league_data.db"
PLAYER_DB_NAME = "player_data.db"

print("Welcome")
#user choice of saving info as csv or database
saveChoice = input("Would you like to save this info to a csv or db? ").strip().lower()
#scrape all the league table info
headers, rows = leagueScrape()


urls = teamUrlFindr()


#scrape all the player info here
headers, rows = clubScraper(urls)

if not rows:
    print("Error scraping")
    sys.exit()

clean_L_Data = cleanLeagueData(rows)
#clean the player data where possible




#add one for player data
if not clean_L_Data:
    print("No valid data")
    sys.exit()

#add one for each for league and data
if saveChoice == "csv":
    file_name = input("Enter a filename: ").strip()
    saveToCsvLeague(clean_L_Data, file_name)
elif saveChoice == "db":
    saveToLeagueDb(clean_L_Data,league_db_name)
else:
    print("Invalid choice exiting")


#calculate runtime
end = time.time()
runtime = (end-start)

#print total runtime out of curiousity
print(runtime)


## identify clubs by their club name and identify players using their url page hopefully it should show up somewhere in their personal page









#maybe do some flask?
#use matplot for creating graphs