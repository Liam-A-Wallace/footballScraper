import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate
import plotly.express as px  # For interactive plots
import plotly.graph_objects as go

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

    # Create efficiency metrics
    players_df['Goals_Per_Minute'] = players_df['Gls'] / players_df['Min']
    players_df['Goals_Per_90'] = players_df['Gls'] / players_df['90s']
    players_df['Assists_Per_90'] = players_df['Ast'] / players_df['90s']
    
    while True:
        print("\n===== FOOTBALL STATS ANALYSIS =====")
        print("1. League Standings Visualization")
        print("2. Team Performance Analysis")
        print("3. Player Performance Analysis")
        print("4. Player Efficiency Scatter Plots")
        print("5. View Team Player Stats")
        print("6. Exit")
        
        choice = input("Select analysis option: ").strip()
        
        if choice == "1":
            # League standings bar chart
            league_df = league_df.sort_values("Points", ascending=False)
            plt.figure(figsize=(12, 8))
            ax = sns.barplot(x="Team", y="Points", data=league_df, palette="viridis")
            plt.title("Scottish Premiership Standings")
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
            if team not in league_df['Team'].values:
                print(f"Team '{team}' not found in database")
                continue
                
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
            if metric not in players_df.columns:
                print(f"Metric '{metric}' not found in player data")
                continue
                
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
            # Player efficiency scatter plots
            print("\n===== PLAYER EFFICIENCY ANALYSIS =====")
            print("1. Goals vs Minutes Played")
            print("2. Goals per 90 vs Assists per 90")
            print("3. Custom Scatter Plot")
            plot_choice = input("Select plot type: ").strip()
            
            if plot_choice == "1":
                # Filter out players with minimal minutes
                filtered = players_df[players_df['Min'] > 200].copy()
                filtered['Goals_Per_90'] = filtered['Gls'] / filtered['90s']
                
                fig = px.scatter(
                    filtered,
                    x='Min',
                    y='Gls',
                    color='Pos',
                    size='Goals_Per_90',
                    hover_name='Player',
                    hover_data=['Team', 'Pos', 'Age', 'Min', 'Gls', 'Goals_Per_90'],
                    title='Goals vs Minutes Played',
                    labels={'Min': 'Minutes Played', 'Gls': 'Goals Scored'}
                )
                fig.update_traces(marker=dict(opacity=0.7))
                fig.update_layout(hovermode='closest')
                fig.show()
                
            elif plot_choice == "2":
                # Filter out players with minimal minutes
                filtered = players_df[players_df['90s'] > 5].copy()
                filtered['Assists_Per_90'] = filtered['Ast'] / filtered['90s']
                
                fig = px.scatter(
                    filtered,
                    x='Goals_Per_90',
                    y='Assists_Per_90',
                    color='Team',
                    size='G+A',
                    hover_name='Player',
                    hover_data=['Team', 'Pos', 'Age', 'Goals_Per_90', 'Assists_Per_90', 'G+A'],
                    title='Goals per 90 vs Assists per 90',
                    labels={'Goals_Per_90': 'Goals per 90', 'Assists_Per_90': 'Assists per 90'}
                )
                fig.update_traces(marker=dict(opacity=0.7))
                fig.update_layout(hovermode='closest')
                fig.show()
                
            elif plot_choice == "3":
                x_metric = input("Enter metric for x-axis: ").strip()
                y_metric = input("Enter metric for y-axis: ").strip()
                
                if x_metric not in players_df.columns or y_metric not in players_df.columns:
                    print("One or both metrics not found in player data")
                    continue
                    
                fig = px.scatter(
                    players_df,
                    x=x_metric,
                    y=y_metric,
                    color='Pos',
                    size='Age',
                    hover_name='Player',
                    hover_data=['Team', 'Pos', 'Age', x_metric, y_metric],
                    title=f'{y_metric} vs {x_metric}',
                    labels={x_metric: x_metric, y_metric: y_metric}
                )
                fig.update_traces(marker=dict(opacity=0.7))
                fig.update_layout(hovermode='closest')
                fig.show()
                
            else:
                print("Invalid choice")
                
        elif choice == "5":
            # View team player stats
            team = input("Enter team name: ").strip()
            if team not in players_df['Team'].values:
                print(f"Team '{team}' not found in database")
                continue
                
            # Filter players
            team_players = players_df[players_df['Team'] == team]
            
            print(f"\n===== {team} PLAYER STATISTICS =====")
            print("1. Show all players")
            print("2. Show top scorers")
            print("3. Show top assist providers")
            print("4. Show goalkeepers")
            view_choice = input("Select view: ").strip()
            
            # Sort and display data
            if view_choice == "1":
                display_df = team_players[['Player', 'Pos', 'Age', 'MP', 'Starts', 'Gls', 'Ast']]
            elif view_choice == "2":
                display_df = team_players.nlargest(10, 'Gls')[['Player', 'Pos', 'Gls', 'Min', 'Goals_Per_90']]
            elif view_choice == "3":
                display_df = team_players.nlargest(10, 'Ast')[['Player', 'Pos', 'Ast', 'Min', 'Assists_Per_90']]
            elif view_choice == "4":
                display_df = team_players[team_players['Pos'] == 'GK'][['Player', 'Age', 'MP', 'Starts', 'Min']]
            else:
                print("Invalid choice")
                continue
                
            # Format and display
            print(tabulate(
                display_df.sort_values('Player'), 
                headers='keys', 
                tablefmt='psql',
                showindex=False,
                floatfmt=".2f"
            ))
            
        elif choice == "6":
            print("Exiting analysis...")
            break
            
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    analyze_data()