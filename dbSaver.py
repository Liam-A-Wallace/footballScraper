#program to save the data to a sqlite 3 db
import sqlite3

def saveToDbLeague(data,db_name):
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



def saveToDbPlayer(data, db_name):
    try:
        # Establish the SQLite database connection
        sqliteConnection = sqlite3.connect(db_name)
        cursor = sqliteConnection.cursor()
        print("DB Init")

        # Create the player_data table with columns matching the CSV headers exactly.
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS player_data (
            "Player" TEXT PRIMARY KEY,
            "Nation" TEXT,
            "Pos" TEXT,
            "Age" INTEGER,
            "MP" INTEGER,
            "Starts" INTEGER,
            "Min" INTEGER,
            "90s" REAL,
            "Gls" INTEGER,
            "Ast" INTEGER,
            "G+A" INTEGER,
            "G-PK" INTEGER,
            "PK" INTEGER,
            "PKatt" INTEGER,
            "CrdY" INTEGER,
            "CrdR" INTEGER,
            "Gls (Per 90)" REAL,
            "Ast (Per 90)" REAL,
            "G+A (Per 90)" REAL,
            "G-PK (Per 90)" REAL,
            "G+A-PK" REAL,
            "Team" TEXT,
            FOREIGN KEY (Team) REFERENCES league_Table_SP(Team)
        )
        ''')

        # Insert each row from the cleaned dictionary into the database.
        for row in data:
            cursor.execute('''
            INSERT INTO player_data (
                "Player", "Nation", "Pos", "Age", "MP", "Starts", "Min", "90s",
                "Gls", "Ast", "G+A", "G-PK", "PK", "PKatt", "CrdY", "CrdR",
                "Gls (Per 90)", "Ast (Per 90)", "G+A (Per 90)", "G-PK (Per 90)", "G+A-PK", "Team"
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT("Player") DO UPDATE SET
                "Nation"=excluded."Nation",
                "Pos"=excluded."Pos",
                "Age"=excluded."Age",
                "MP"=excluded."MP",
                "Starts"=excluded."Starts",
                "Min"=excluded."Min",
                "90s"=excluded."90s",
                "Gls"=excluded."Gls",
                "Ast"=excluded."Ast",
                "G+A"=excluded."G+A",
                "G-PK"=excluded."G-PK",
                "PK"=excluded."PK",
                "PKatt"=excluded."PKatt",
                "CrdY"=excluded."CrdY",
                "CrdR"=excluded."CrdR",
                "Gls (Per 90)"=excluded."Gls (Per 90)",
                "Ast (Per 90)"=excluded."Ast (Per 90)",
                "G+A (Per 90)"=excluded."G+A (Per 90)",
                "G-PK (Per 90)"=excluded."G-PK (Per 90)",
                "G+A-PK"=excluded."G+A-PK",
                "Team"=excluded."Team"
            ''', (
                row["Player"], row["Nation"], row["Pos"], row["Age"], row["MP"], row["Starts"],
                row["Min"], row["90s"], row["Gls"], row["Ast"], row["G+A"], row["G-PK"],
                row["PK"], row["PKatt"], row["CrdY"], row["CrdR"], row["Gls (Per 90)"],
                row["Ast (Per 90)"], row["G+A (Per 90)"], row["G-PK (Per 90)"], row["G+A-PK"], row["Club"]
            ))

        sqliteConnection.commit()
        print("Data saved")

    except sqlite3.Error as error:
        print("Error occurred:", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("Connection Closed")
