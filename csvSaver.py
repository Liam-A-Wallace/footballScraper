import csv

def saveToCsvLeague(data, file_name):
    if not data:
        print("No data to save.")
        return
    
    if not file_name.endswith(".csv"):
        file_name += ".csv"

    try:
        # Assuming data is a list of lists
        if isinstance(data[0], list):
            with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(data)
        # Assuming data is a list of dictionaries
        elif isinstance(data[0], dict):
            with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
        else:
            print("Unsupported data format for CSV.")
            return

        print(f"Data successfully saved to {file_name}")
    except Exception as e:
        print(f"An error occurred while saving to CSV: {e}")

def saveToCsvPlayer(data, file_name):
    if not data:
        print("No data to save.")
        return
