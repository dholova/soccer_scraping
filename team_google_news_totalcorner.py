import csv
import os
from urllib.parse import quote
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
file_path = os.path.join(desktop_path, "teams_news_tc_url.xlsx")


news_tc_list = []
rowi = []

with open('matches_data.csv', 'r', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        rowi.append(row)

for row in rowi:
    team_name = row[0]
    print(row)
    if quote(row[1]) == 'TBC' or quote(row[1]) == 'Pakse':
        country_name = ''
    else:
        country_name = quote(row[1])
    row_quote = quote(row[0])
    row_tc = row_quote.replace(' ', '+')
    url_news = f'https://www.google.com.ua/search?q={row_quote}" "{country_name}&tbm=nws&sxsrf=APwXEddUkdHGyAC48ZLWlWL-fGnptsg0Jg%3A1687908958428&source=hp&ei=XnKbZMqIGJH9qwH-s49A&iflsig=AOEireoAAAAAZJuAbj2DzzNzlhhKMFMwpadMOEjcGpwH&ved=0ahUKEwjKr4PvzuT_AhWR_ioKHf7ZAwgQ4dUDCAk&uact=5&oq={team_name, country_name}&gs_lcp=Cgxnd3Mtd2l6LW5ld3MQAzIFCAAQgAQyCAgAEBYQHhAKMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeMgYIABAWEB4yBggAEBYQHlB-WH5g_AxoAXAAeACAAWOIAWOSAQExmAEAoAECoAEBsAEA&sclient=gws-wiz-news'
    url_tc = f'https://www.google.com.ua/search?q={row_tc}+{country_name}+totalcorner&biw=1166&bih=670&sxsrf=APwXEdeUWt8eA72LX1ZPwqIxpYPrjfL5xg%3A1687914863042&ei=b4mbZP6QAv2Vxc8P0uKJqAw&oq={row_tc}+totalcorner&gs_lcp=ChNtb2JpbGUtZ3dzLXdpei1zZXJwEAMyBAgjECcyBQgAEKIEMgUIABCiBDIFCAAQogQyBQgAEKIEOgoIABBHENYEELADSgQIQRgAUNoCWNoCYJUJaAFwAXgAgAGWAYgBlgGSAQMwLjGYAQCgAQKgAQHAAQHIAQg&sclient=mobile-gws-wiz-serp'
    driver = webdriver.Chrome()
    driver.get(url_tc)
    try:
        driver.implicitly_wait(3)
        search_tc = driver.find_element(By.CSS_SELECTOR, "div.yuRUbf a").get_attribute('href')
        print(search_tc)
    except:
        search_tc = 'TBC'
    finally:
        driver.quit()


    news_tc_list.append([team_name, country_name, url_news, search_tc])


header = ['Team name', 'Country', 'Google News Link', 'Total Corner Link']
df = pd.DataFrame(news_tc_list, columns=header)
df.to_excel(file_path, engine='openpyxl', index=False)
