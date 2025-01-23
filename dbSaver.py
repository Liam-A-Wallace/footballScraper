#program to save the data to a csv file intended to take in data and a filename and turn the resulting data into a csv
import sqlite3

def saveToDb(data,db_name):
    #add logic here to ensure rows is correct columns
    try:
        sqliteConnection = sqlite3.connect(db_name)
        cursor = conn.cursor
        print("DB Init")

        #COLS with data type
        #League position INTEGER
        #Team Name TEXT
        #matches played INTEGER
        #matches won INTEGER
        #matches drawn INTEGER
        #matches lost INTEGER
        #goals for INTEGER
        #goals against INTEGER
        #gd INTEGER
        #pts INTEGER
        #pts per match played REAL
        #last 5 TEXT
        #Attendance (This has a comma in the number may need to clean can i sort a string?) INTEGER
        #top scorer string with number wonder if i can split it somehow TEXT AND INTEGER
        #simply goalkeeper name INTEGER

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS league_Table_SP (
        PlaceHolder
        )
        
        ''')

        #logic to handle updates
        #pos team name etc are placeholders CHANGE
        for position, team_name, points in rows:
            cursor.execute('''league_Table_SP (pos)''')
    except sqlite3.Error as error:
        print("Error occured: ", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("Connection Closed")