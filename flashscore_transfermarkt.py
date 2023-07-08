import os
import csv
import re
from selenium import webdriver
import pandas as pd
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def get_transfermarkt_links(team_name):
    url = "https://www.transfermarkt.co.uk/"
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    try:
        driver.implicitly_wait(3)
        search_input = driver.find_element(By.CSS_SELECTOR, 'input.tm-header__input--search-field')
        a = search_input.send_keys(team_name)
        search_input.send_keys(Keys.ENTER)
        try:
            clubs_list = driver.find_elements(By.CSS_SELECTOR, "td.hauptlink a")
            clubs = [i.get_attribute('title') for i in clubs_list]
            country_list = driver.find_elements(By.CSS_SELECTOR, "td.zentriert img")
            country = [i.get_attribute('title') for i in country_list][1::2]
            if len(clubs_list) == 0:
                tm_links.append('TBC')
            count = 0
            for link in clubs_list:
                count += 1
                link_title = link.get_attribute("title")
                modified_title = link_title
                pattern = r'\b{}\b'.format(re.escape(modified_title))
                match = re.search(pattern, link_title, re.IGNORECASE)
                if match:
                    found_link = link.get_attribute("href")
                    if 'verein' in found_link:
                        tm_links.append(found_link)
                        break
                else:
                    tm_links.append('TBC')
                    pass
        except:
            pass
    finally:
        driver.implicitly_wait(3)
        driver.quit()

def get_flashscore_links(team_name):
    url = "https://www.flashscore.com/"
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    try:
        driver.implicitly_wait(5)
        search = driver.find_element(By.ID, "search-window")
        search_btn = search.click()
        search_input = driver.find_element(By.CLASS_NAME, "searchInput__input")
        a = search_input.send_keys(team_name)
        search_input.send_keys(Keys.ENTER)
        teams = driver.find_elements(By.CSS_SELECTOR, "a.searchResult")
        for team in teams:
            category = team.find_element(By.CLASS_NAME, "searchResult__participantCategory").text
            country_n = category.split(',')[1].lstrip()
            team_name_fs = team.find_element(By.CLASS_NAME, "searchResult__participantName").text
            pattern = r'\b{}\b'.format(re.escape(team_name_fs))
            match = re.search(pattern, team_name_fs, re.IGNORECASE)
            if match and country_n.lower()==country_name.lower():
                found_link = team.get_attribute("href")
                fs_links.append(found_link)
                break
            else:
                link_team = 'TBC'
                fs_links.append(link_team)
    finally:
        driver.implicitly_wait(3)
        driver.quit()

tm_links = []
fs_links = []
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
file_path = os.path.join(desktop_path, "flashscore_transfermarkt.xlsx")

with open('matches_data.csv', 'r', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    rows = []
    for row in csvreader:
        team_name = row[0].replace('SKN', '')
        country_name = row[1]
        get_transfermarkt_links(team_name)
        get_flashscore_links(team_name)
        rows.append([team_name, tm_links[-1], fs_links[-1]])
        fs_links = []
        tm_links = []

header = ['Team name', 'Transfermarkt links', 'Flashscore links']
df = pd.DataFrame(rows, columns=header)
df.to_excel(file_path, engine='openpyxl', index=False)

