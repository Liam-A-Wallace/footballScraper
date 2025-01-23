import time 
import sys
from scraper import *
from csvSaver import saveToCsv
from dbSaver import saveToDb
from cleaner import cleanLeagueData


#start of program
start = time.time()
db_name = "league_data.db"

print("Welcome")
saveChoice = input("Would you like to save this info to a csv or db? ").strip().lower()
#scrape all the league table info
headers, rows = leagueScrape()


if not rows:
    print("Error scraping")
    sys.exit()
print(rows)
clean_L_Data = cleanLeagueData(rows)

if not clean_L_Data:
    print("No valid data")
    sys.exit()

if saveChoice == "csv":
    file_name = input("Enter a filename: ").strip()
    saveToCsv(clean_L_Data, file_name)
elif saveChoice == "db":
    saveToDb(clean_L_Data,db_name)
else:
    print("Invalid choice exiting")

#####FOCUSING ON FIRST SETTING UP STORAGE OF LEAGUE DATA
#finds all the clubs urls
#urls = teamUrlFindr()

#also need to scrape all the player info prob need to do that whenever im looking through each club
#clubScraper(urls)

#calculate runtime
end = time.time()
runtime = (end-start)

#print total runtime out of curiousity
print(runtime)


## identify clubs by their club name and identify players using their url page hopefully it should show up somewhere in their personal page

#most likely store using sqlLite need to define schemas asnd shit tho
#maybe do some flask?
#use matplot for creating graphs