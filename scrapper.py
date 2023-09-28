from selenium import webdriver
from bs4 import BeautifulSoup
import os

# Specify the path to the Edge WebDriver executable
driver_path = r'C:\Users\hp\Downloads\edgedriver_win64\msedgedriver.exe'

# Add the driver path to the PATH environment variable
os.environ['PATH'] += os.pathsep + driver_path

# Create a WebDriver instance for Microsoft Edge
driver = webdriver.Edge()

# URL of the page you want to scrape
url = "https://us.soccerway.com/"
driver.get(url)

# Wait for the page to load (you may need to adjust the waiting time)
driver.implicitly_wait(10)

# Extract the page source
page_source = driver.page_source

# Parse the HTML content of the page with BeautifulSoup
soup = BeautifulSoup(page_source, "html.parser")

# Find all matchinfo elements
matchinfo_elements = soup.find_all("div", class_="matchinfo")

# Initialize a list to store match details
matches = []

for matchinfo_element in matchinfo_elements:
    # Extract match details from each matchinfo element
    kickoff_time = matchinfo_element.find("time", class_="kickoff_time").text.strip()
    
    teams = matchinfo_element.find_all("div", class_="team_name")
    team1 = teams[0].text.strip()
    team2 = teams[1].text.strip()
    
    match_status = matchinfo_element.find("div", class_="match_status").text.strip()
    
    # Initialize scores for both teams as None
    score_team1 = None
    score_team2 = None
    
    # Check if the match has started
    if match_status != "-":
        # Extract the scores for both teams
        score_elements = matchinfo_element.find_all("span", class_="team_score")
        if len(score_elements) == 2:
            score_team1 = score_elements[0].text.strip()
            score_team2 = score_elements[1].text.strip()
    
    # Create a dictionary to represent the match
    match_info = {
        "Kickoff Time": kickoff_time,
        "Team 1": team1,
        "Team 2": team2,
        "Match Status": match_status,
        "Score Team 1": score_team1,  # Include the score for Team A
        "Score Team 2": score_team2,  # Include the score for Team 
    }
    
    # Append the match info to the list
    matches.append(match_info)

# Print the list of matches
for match in matches:
    print(match)

# Close the WebDriver session when done
driver.quit()
