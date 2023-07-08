import os
import sys

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

date = input("Please put the date in format '2023/12/31': ")
num_of_page = input("Please put the num of page(from 1 to 4): ")
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

file_path = os.path.join(desktop_path, f"{date.replace('/','')}friendlies.xlsx")
url = f"https://int.soccerway.com/international/world/club-friendlies/2023/club-friendlies-{num_of_page}"
options = Options()
options.add_argument('--ignore-certificate-errors')
# options.add_argument('--headless')

driver = webdriver.Chrome(options=options)
driver.get(url)
data_matches = []
full_data_matches = []
venue_added = False

try:
    new_match_dataa = []
    full_match_data = driver.find_elements(By.CSS_SELECTOR, 'tr.match.border')
    match_urls = []
    for match in full_match_data:
        new_match_dataa = []
        data_match = []
        driver.implicitly_wait(3)
        one_match = match.find_elements(By.CSS_SELECTOR, 'td.score-time a')
        for oni in one_match:
            match_url = oni.get_attribute('href')
            match_urls.append(match_url)  # Зберігаємо URL-адресу кожного матчу

            driver.get(match_url)
            teams = driver.find_elements(By.CLASS_NAME, 'team-title')
            for team in teams:
                team_url = team.get_attribute('href')
                team_name = str(team_url).split('/')[-3]
                team_country = str(team_url).split('/')[-4]
                data_match.append(team_name)
                data_match.append(team_country)
                data_match.append(team_url)
            try:
                date_match = driver.find_element(By.CSS_SELECTOR, "div.details a").get_attribute('href')[-11:-1]
            except:
                date_match = 'TBC'
            new_match_dataa.append(date_match)
            try:
                venue = driver.find_element(By.XPATH, "//span[text()='Venue']/following-sibling::span/a").text
            except:
                venue = 'TBC'
            try:
                time = driver.find_element(By.XPATH, "//span[text()='KO']/following-sibling::span").text
            except:
                time = 'TBC'
            try:
                score = driver.find_element(By.CLASS_NAME, 'scoretime').text
            except:
                score = 'TBC'
            data_match.append(match_url)
            if [venue] not in data_match:
                data_match.append(venue)
            else:
                pass
            data_match.append(time)
            data_match.append(score)
            if date != ''.join(new_match_dataa) and len(full_data_matches) == 0:
                continue
            elif date == ''.join(new_match_dataa):
                data_matches.append(data_match)
            elif len(full_data_matches) == len(data_matches) and ''.join(new_match_dataa) != date:
                header = ['Team name A', 'Country name team A', 'Team A url', 'Team name B', 'Country name team B', 'Team B url', 'Match URL','Venue','Time', 'Score']
                df = pd.DataFrame(data_matches, columns=header)
                df.to_excel(file_path, engine='openpyxl', index=False)

                sys.exit()
            full_data_matches = data_matches.copy()

        driver.back()
    for match_url in match_urls:
        driver.get(match_url)


finally:
    driver.quit()
