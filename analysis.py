import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_data():
    # Connect to databases
    league_conn = sqlite3.connect("league_data.db")
    player_conn = sqlite3.connect("player_data.db")
    
    # Load data into DataFrames
    league_df = pd.read_sql_query("SELECT * FROM league_Table_SP", league_conn)
    players_df = pd.read_sql_query("SELECT * FROM player_data", player_conn)
    
    # Close connections
    league_conn.close()
    player_conn.close()
  
    # List of numeric columns in player data
    numeric_cols = [
        'Age', 'MP', 'Starts', 'Min', '90s', 'Gls', 'Ast', 'G+A', 'G-PK',
        'PK', 'PKatt', 'CrdY', 'CrdR', 'Gls (Per 90)', 'Ast (Per 90)',
        'G+A (Per 90)', 'G-PK (Per 90)', 'G+A-PK'
    ]
    
    # Convert columns to numeric, handling errors
    for col in numeric_cols:
        if col in players_df.columns:
            players_df[col] = pd.to_numeric(players_df[col], errors='coerce')
    
    # Convert league table numeric columns
    league_numeric = [
        'LeaguePosition', 'MatchesPlayed', 'Won', 'Drawn', 'Lost',
        'GoalsFor', 'GoalsAgainst', 'GoalDifference', 'Points',
        'PointsPerMatch', 'Attendance'
    ]
    
    for col in league_numeric:
        if col in league_df.columns:
            league_df[col] = pd.to_numeric(league_df[col], errors='coerce')

    
    while True:
        print("\n===== FOOTBALL STATS ANALYSIS =====")
        print("1. League Standings Visualization")
        print("2. Team Performance Analysis")
        print("3. Player Performance Analysis")
        print("4. Exit")
        
        choice = input("Select analysis option: ").strip()
        
        if choice == "1":
            # League standings bar chart
            league_df = league_df.sort_values("Points", ascending=False)
            plt.figure(figsize=(12, 8))
            ax = sns.barplot(x="Team", y="Points", data=league_df, palette="viridis")
            plt.title("League Standings")
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            
            # Annotate values
            for p in ax.patches:
                ax.annotate(f"{p.get_height():.0f}", 
                            (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', 
                            xytext=(0, 5), 
                            textcoords='offset points')
            plt.show()
            
        elif choice == "2":
            # Team performance radar chart
            team = input("Enter team name: ").strip()
            team_data = league_df[league_df["Team"] == team].iloc[0]
            
            categories = ['GoalsFor', 'GoalsAgainst', 'Won', 'Attendance']
            values = [
                team_data['GoalsFor'],
                team_data['GoalsAgainst'],
                team_data['Won'],
                team_data['Attendance'] / 1000  # Normalize
            ]
            
            # Radar chart setup
            angles = [n / float(len(categories)) * 2 * 3.14159 for n in range(len(categories))]
            values += values[:1]  # Close the radar
            angles += angles[:1]
            
            fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
            ax.plot(angles, values, linewidth=1, linestyle='solid', label=team)
            ax.fill(angles, values, alpha=0.25)
            ax.set_theta_offset(3.14159 / 2)
            ax.set_theta_direction(-1)
            ax.set_thetagrids([a * 180/3.14159 for a in angles[:-1]], categories)
            plt.title(f"{team} Performance Profile")
            plt.legend()
            plt.show()
            
        elif choice == "3":
            # Player analysis
            metric = input("Metric to analyze (Gls, Ast, CrdY, etc): ").strip()
            top_n = int(input("Number of players to show: "))
            
            # Get top players
            top_players = players_df.nlargest(top_n, metric)
            
            # Plot comparison
            plt.figure(figsize=(14, 6))
            ax = sns.barplot(x="Player", y=metric, hue="Team", data=top_players, dodge=False)
            plt.title(f"Top {top_n} Players by {metric}")
            plt.xticks(rotation=15)
            plt.tight_layout()
            
            # Add value labels
            for p in ax.patches:
                ax.annotate(f"{p.get_height():.1f}", 
                            (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', 
                            xytext=(0, 5), 
                            textcoords='offset points')
            plt.show()
            
        elif choice == "4":
            print("Exiting analysis...")
            break
            
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    analyze_data()