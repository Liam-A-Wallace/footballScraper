#program to save the data to a sqlite 3 db
import sqlite3

def saveToDb(data,db_name):
    #add logic here to ensure rows is correct columns
    try:
        sqliteConnection = sqlite3.connect(db_name)
        cursor = sqliteConnection.cursor()
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
        #Attendance INTEGER
        #top scorer  TEXT
        #simply goalkeeper name INTEGER

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS league_Table_SP (
            LeaguePosition INTEGER NOT NULL,
            Team TEXT PRIMARY KEY,
            MatchesPlayed INTEGER,
            Won INTEGER,
            Drawn INTEGER,
            Lost INTEGER,
            GoalsFor INTEGER,
            GoalsAgainst INTEGER,
            GoalDifference INTEGER,
            Points INTEGER,
            PointsPerMatch REAL,
            Last5 TEXT,
            Attendance INTEGER,
            TopScorer TEXT,
            Goalkeeper Text


        )
        
        ''')

        #logic to handle updates
        #pos team name etc are placeholders CHANGE
        for row in data:
            cursor.execute('''
            INSERT INTO league_Table_SP (
                LeaguePosition, Team, MatchesPlayed, Won, Drawn, Lost, 
                GoalsFor, GoalsAgainst, GoalDifference, Points, 
                PointsPerMatch, Last5, Attendance, TopScorer, Goalkeeper
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(Team) DO UPDATE SET
                LeaguePosition=excluded.LeaguePosition,
                MatchesPlayed=excluded.MatchesPlayed,
                Won=excluded.Won,
                Drawn=excluded.Drawn,
                Lost=excluded.Lost,
                GoalsFor=excluded.GoalsFor,
                GoalsAgainst=excluded.GoalsAgainst,
                GoalDifference=excluded.GoalDifference,
                Points=excluded.Points,
                PointsPerMatch=excluded.PointsPerMatch,
                Last5=excluded.Last5,
                Attendance=excluded.Attendance,
                TopScorer=excluded.TopScorer,
                Goalkeeper=excluded.Goalkeeper
             ''',row)
            sqliteConnection.commit()
            print("Data saved")
    except sqlite3.Error as error:
        print("Error occured: ", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("Connection Closed")