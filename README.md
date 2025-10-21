# Football Data Analysis

A Python application that scrapes, processes, and analyzes Scottish Premiership football data from FBRef.com.

## Features
- **Web Scraping**: Automatically collects league and player statistics
- **Data Storage**: Save to CSV files or SQLite databases  
- **Analysis Tools**: Interactive visualizations and performance metrics
- **Data Cleaning**: Processes raw data into structured formats

## Quick Start
1. Install requirements: `pip install requests beautifulsoup4 pandas matplotlib seaborn plotly`
2. Run: `python main.py`
3. Choose to scrape new data or analyze existing data

## Modules
- `main.py` - Program controller
- `scraper.py` - Web scraping functions
- `cleaner.py` - Data processing utilities
- `dbSaver.py` / `csvSaver.py` - Storage handlers
- `analysis.py` - Visualization and analysis

## Data Includes
- League standings and team statistics
- Player performance metrics
- Goals, assists, playing time, efficiency rates
- Interactive charts and team comparisons

Run the application and follow the menu prompts to scrape data or analyze existing datasets.