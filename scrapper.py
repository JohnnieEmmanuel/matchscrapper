//currently scrapping just 25 league games . we will increase this later when we modify for latency sake 
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time

# Function to scrape and update match data
def scrape_and_update():
    # Specify the path to the Edge WebDriver executable
    driver_path = r'C:\Users\hp\Downloads\edgedriver_win64\msedgedriver.exe'

    # Add the driver path to the PATH environment variable
    os.environ['PATH'] += os.pathsep + driver_path

    # Create a WebDriver instance for Microsoft Edge
    driver = webdriver.Edge()

    # URL of the page you want to scrape
    main_url = "https://us.soccerway.com/"
    driver.get(main_url)

    # Wait for the page to load (you may need to adjust the waiting time)
    driver.implicitly_wait(10)

    # Initialize a list to store match details
    matches = []

    # Counter for the number of leagues processed
    league_count = 0

    try:
        while True:
            try:
                # Find all league elements
                league_elements = driver.find_elements(By.CLASS_NAME, "livescores-comp")

                for league_element in league_elements:
                    if league_count >= 15:
                        break  # Exit the loop once 15 leagues have been processed

                    # Check if the league is expanded by checking the "data-expanded" attribute
                    is_expanded = league_element.get_attribute("data-expanded") == "1"
                    
                    if not is_expanded:
                        # If the league is not expanded, click the "expand-icon" button
                        try:
                            # Scroll into view to ensure the button is clickable
                            driver.execute_script("arguments[0].scrollIntoView();", league_element)
                            expand_icon_button = league_element.find_element(By.CLASS_NAME, "expand-icon")
                            expand_icon_button.click()
                            # Wait for a moment to load the matches
                            time.sleep(2)
                        except Exception as e:
                            print(f"Error clicking 'expand-icon' button: {e}")
                            # Handle the error, e.g., log it or skip this league
                            continue

                    # Extract league details
                    league_name = league_element.find_element(By.CLASS_NAME, "area-name").text.strip()

                    # Find all matchinfo elements within the league element
                    matchinfo_elements = league_element.find_elements(By.CLASS_NAME, "livescore_match")

                    for matchinfo_element in matchinfo_elements:
                        # Extract match details from each matchinfo element
                        kickoff_time = matchinfo_element.find_element(By.CLASS_NAME, "kickoff_time").text.strip()

                        teams = matchinfo_element.find_elements(By.CLASS_NAME, "team_name")
                        team1 = teams[0].text.strip()
                        team2 = teams[1].text.strip()

                        match_status = matchinfo_element.find_element(By.CLASS_NAME, "match_status").text.strip()

                        # Initialize scores for both teams as None
                        score_team1 = None
                        score_team2 = None

                        # Check if the match has started
                        if match_status != "-":
                            # Extract the scores for both teams
                            score_elements = matchinfo_element.find_elements(By.CLASS_NAME, "team_score")
                            if len(score_elements) == 2:
                                score_team1 = score_elements[0].text.strip()
                                score_team2 = score_elements[1].text.strip()

                        # Create a dictionary to represent the match
                        match_info = {
                            "League Name": league_name,
                            "Kickoff Time": kickoff_time,
                            "Team 1": team1,
                            "Team 2": team2,
                            "Match Status": match_status,
                            "Score Team 1": score_team1,  # Include the score for Team A
                            "Score Team 2": score_team2,  # Include the score for Team B
                        }

                        # Append the match info to the list
                        matches.append(match_info)

                    # Increment the league count
                    league_count += 1

                if league_count >= 15:
                    break  # Exit the loop once 15 leagues have been processed

                # Find the next page button if available and click it
                next_page_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Next')]")
                if next_page_button:
                    next_page_button.click()
                else:
                    break  # No more pages

            except Exception as e:
                print(f"Error scraping: {e}")
                break  # Break the loop if an error occurs

    finally:
        # Close the WebDriver session when done
        driver.quit()

    return matches

# Define the path to the JSON file
json_file_path = 'matches.json'

while True:
    # Scrape and update the match data
    updated_matches = scrape_and_update()
    
    # Save the updated matches to a JSON file
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(updated_matches, json_file, ensure_ascii=False, indent=4)

    print("Matches updated and saved to matches.json")

    # Pause for 10 minutes before checking again
    time.sleep(600)  # 600 seconds = 10 minutes
