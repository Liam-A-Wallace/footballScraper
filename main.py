import time 
import sys
from scraper import *
from csvSaver import *
from dbSaver import *
from cleaner import *
from analysis import analyze_data


#start of program
start = time.time()

#initialising database names
LEAGUE_DB_NAME = "league_data.db"
PLAYER_DB_NAME = "player_data.db"

print("Welcome")
mode = input("Choose:\n1. Scrape & Save\n2. Analyze existing data\n> ").strip()
#user choice of saving info as csv or database
if mode == "1":
    saveChoice = input("Would you like to save this info to a csv or db? ").strip().lower()
    #scrape all the league table info
    headers, leagueData = leagueScrape()

    # Filter out rows with an empty club name (first column)
    leagueData = [row for row in leagueData if row[0].strip()]

    urls = teamUrlFindr()

    #scrape all the player info here
    headers, playerData = clubScraper(urls,leagueData)

    if not leagueData or not playerData:
        print("Error scraping")
        sys.exit()

    clean_L_Data = cleanLeagueData(leagueData)
    #clean the player data where possible
    clean_P_Data = cleanPlayerData(playerData)





    if not clean_L_Data or not clean_P_Data:
        print("No valid data")
        sys.exit()

    #add one for each for league and data
    if saveChoice == "csv":
        file_name_l = input("Enter a filename for the league data CSV: ").strip()
        saveToCsvLeague(clean_L_Data, file_name_l)
        file_name_p = input("Enter a filename for the player data CSV: ").strip()
        saveToCsvPlayer(clean_P_Data, file_name_p)
    elif saveChoice == "db":
        saveToDbLeague(clean_L_Data,LEAGUE_DB_NAME)
        saveToDbPlayer(clean_P_Data,PLAYER_DB_NAME)
    else:
        print("Invalid choice exiting")

elif mode == "2":
    analyze_data()
else:
    print("Invalid choice, exiting")
    

#calculate runtime
end = time.time()
runtime = (end-start)

#print total runtime out of curiousity
print(runtime)










#maybe do some flask?
#use matplot for creating graphs