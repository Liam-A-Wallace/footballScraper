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

def clubScraper(urls,leagueData):
    headers = []
    playerData = []
    urlIndex = 0
    

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
            print(f"Table not found on {url}")
            continue


        if not headers:
            all_rows = table.find('thead').find_all('tr')  
            if len(all_rows) > 1:  
                header_row = all_rows[1]  # Select the second row (actual headers)
                
                raw_headers = [th.text.strip() for th in header_row.find_all('th')]

                # Fix duplicate column names by adding section names
                unique_headers = []
                header_count = {}

                for header in raw_headers:
                    if header in header_count:
                        header_count[header] += 1
                        if header_count[header] == 2:
                            unique_headers.append(f"{header} (Per 90)")
                    else:
                        header_count[header] = 1
                        unique_headers.append(header)

                headers = unique_headers  # Store unique headers
                headers.append("Club")
        
        tbody = table.find('tbody')
        for row in tbody.find_all('tr'):
            cols = row.find_all(['th','td'])
            if len(cols) != len(headers) -1:
                continue
            player_dict = {headers[i]: cols[i].text.strip() for i in range(len(cols))}
            player_dict["Club"] = leagueData[urlIndex][0]
            playerData.append(player_dict)
        urlIndex +=1
            
    
    return headers, playerData
        


 
    