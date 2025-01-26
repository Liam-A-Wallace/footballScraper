import requests
import time 
import random
from bs4 import BeautifulSoup
from cleaner import urlCleaner

def leagueScrape():
    # Making a GET request
    r = requests.get('https://fbref.com/en/comps/40/Scottish-Premiership-Stats')

    if r.status_code != 200:
        print(f"Failed to retrieve page, status code: {r.status_code}")
        return None,None
    # check status code for response received
    # success code - 200
    print(r.status_code)
    

    # Parsing the HTML
    soup = BeautifulSoup(r.content, 'html.parser')


    #write to file
    with open('WholePage.html', 'w', encoding='utf-8') as file:
        file.write(soup.prettify())

    print("written page")

    table = soup.find('table',{'id': 'results2024-2025400_overall'})

    if not table:
        print("Table not found!")
        return None,None

    headers = [th.text.strip() for th in table.find_all('th')]
    rows = []
    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')
        if cells:
            rows.append([cell.text.strip() for cell in cells])
    return headers, rows
    

#trying to think of player stats
#problem 1 is finding each club pages url 
#problem 2 player stats are among multiple tables not quite sure how to combine or if i take down every single stat
#work on one problem at a time

def teamUrlFindr():
    urls = []

     # Making a GET request
    r = requests.get('https://fbref.com/en/comps/40/Scottish-Premiership-Stats')

    # check status code for response received
    # success code - 200
    print(r.status_code)

    # Parsing the HTML
    soup = BeautifulSoup(r.content, 'html.parser')

    #finds the table with all relevant links
    table = soup.find('table',{'id': 'results2024-2025400_overall'})
    #find all instances of a within table
    links = table.find_all('a')
    for link in links:
        #appends every link to the url list
        urls.append(link.get('href'))
    
    #calls the cleaner with squad category then returns
    cleanUrls = urlCleaner(urls,"squads")
    return cleanUrls

def clubScraper(urls):
    rows = []
    for url in urls:
        time.sleep(random.uniform(6,9))
        # Making a GET request
        
        r = requests.get(url)

        # check status code for response received
        # success code - 200
        print(f"{r.status_code} {url}")


        # Parsing the HTML
        soup = BeautifulSoup(r.content, 'html.parser')
        
        table = soup.find('table',{'id': 'stats_standard_40'})
        if not table:
            print("Table not found")
            return None
        


 
    