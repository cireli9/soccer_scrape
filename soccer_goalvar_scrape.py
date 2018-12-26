import time
import numpy as np
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_premier():
    #Create dictionary for storing data
    data = {}
    sources = []

    #make driver headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")

    driver = webdriver.Chrome(chrome_options = chrome_options)
    driver.get("https://www.whoscored.com/Regions/206/Tournaments/4/Seasons/7466/Spain-La-Liga")

    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "text")))


    for n in range(9):
        #use to select specific years
        year = 2009+n
        select = Select(driver.find_element_by_xpath('//*[@id="seasons"]'))
        select.select_by_visible_text(str(year) + "/" + str(year+1))

        #navigate to goals
        driver.find_element_by_xpath('//*[@id="sub-navigation"]/ul/li[3]/a').click()

        #scroll to bottom of page
        SCROLL_PAUSE_TIME = 0.7
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME) #load page

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        sources.append(driver.page_source)
        print("got source " + str(year))

    driver.close()

    for source in sources:
        data_soup = BeautifulSoup(source, 'html.parser')

        teams_soup = data_soup.find(id = "top-team-stats-summary-content")
        teams = teams_soup.find_all("tr")
        for team in teams:
            team_name = team.find(class_ = 'team-link').get_text()
            if team_name not in data:
                data[team_name] = [np.nan]*9

    for i in range(len(sources)):
        data_soup = BeautifulSoup(sources[i], 'html.parser')

        #collect data
        teams_soup = data_soup.find(id = "top-team-stats-summary-content")
        teams = teams_soup.find_all("tr")
        for team in teams:
            team_name = team.find(class_ = 'team-link').get_text()
            goals = team.find(class_ = 'goal').get_text()
            data[team_name][i] = goals


    df = pd.DataFrame(data)

    df.to_csv('team_goals.csv')


    print("got data")


#scrape_premier()

# clean data and include statistics
# df = pd.read_csv("team_goals.csv")
# diff = df.diff()
# stats = pd.DataFrame([diff.mean(), diff.var()], index=['Mean', 'Variance'])
# diff = diff.append(stats)
# diff.to_csv('goal_differences_liga.csv')

df = pd.read_csv("goal_differences_liga.csv")
df["Mean"].boxplot(1:)

