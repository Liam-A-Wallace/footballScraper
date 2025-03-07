
#function that takes in a url and target category matches/players/squad etc and returns a list of url for that specifically
def urlCleaner(urls, category):
    # Base URL to append
    templateUrl = "https://fbref.com"
    cleanUrls = []
    

    # Add the template URL to each cleaned URL
    for url in urls:
        if f'/{category}/' in url:
            if category == "players" and "matchlogs" in url:
                continue
            cleanUrls.append(f"{templateUrl}{url}")
    
    return cleanUrls

def cleanLeagueData(rawLeague):
    cleanData = []
    

    # Process each row in rawLeague (ignoring the headers row)
    for row in rawLeague[0:]:
        # Ensure all elements are strings and strip them
        row = [str(cell).strip() for cell in row]

        # Skip rows that are empty or don't contain meaningful data
        if not row or not any(cell for cell in row):  # check for non-empty rows
            continue
        
        # Only keep the first 14 columns
        row = row[:14]

        # Skip rows with less than 14 elements (invalid rows)
        if len(row) < 14:
            continue

        # Insert rank (position) at the start of the row
        rank = len(cleanData) + 1
        row.insert(0, rank)

        #removing the commas from attendance
        row[12] = row[12].replace(",","")

        # Add the cleaned row to the cleanData list
        cleanData.append(row)

    return cleanData

## drop players with zero appearances
# remove matches column,
# remove days from age
# maybe think of a way to better represent nationality dict
# what to do with players with multiple positions not sure
# change mins to a straight int remove commas
#   dont understand the 90s col
# there is a bug regarding goals/90 and goals
def cleanPlayerData(raw_data):
    cleanData = []
    for data in raw_data[0:]:
        data[6] = data[6].replace(",","")

        cleanData.append(data)
    return cleanData
