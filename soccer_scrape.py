import time
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_premier():
    #Create lists for each variable
    Teams = []
    Score = []
    Formation = []
    Scored = []
    Assisted = []
    Posession = []
    OnTarget = []
    Shots = []
    Touches = []
    Passes = []
    Tackles = []
    Clearances = []
    Corners = []
    Offsides = []
    Yellows = []
    Fouls = []

    variables = [Posession, OnTarget, Shots, Touches, Passes, 
                 Tackles, Clearances, Corners, Offsides, Yellows, Fouls]

    #make driver headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")

    driver = webdriver.Chrome(chrome_options = chrome_options)
    driver.get("https://www.premierleague.com/results")

    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "current")))

    #accept cookies and close ads
    driver.find_element_by_xpath('/html/body/section/div/div').click()
    driver.find_element_by_xpath('//*[@id="advertClose"]').click()

    #filter to only 2017-2018 and get html
    driver.find_element_by_xpath('//*[@id="mainContent"]/div[2]/div[1]/section/div[2]/div[2]').click()
    driver.find_element_by_xpath('//*[@id="mainContent"]/div[2]/div[1]/section/div[2]/ul/li[3]').click()

    time.sleep(1)

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

    matches = driver.page_source
    driver.close()

    print("got matches")

    #collect all match links
    matchLinks = []
    matchSoup = BeautifulSoup(matches, 'html.parser')
    matchElements = matchSoup.find_all(class_ = 'matchFixtureContainer')

    for i in range(len(matchElements)):
        link = "https://www.premierleague.com/match/"
        link = link + matchElements[i]["data-comp-match-item"]
        matchLinks.append(link)

    assert(len(matchLinks) == 380)
    print("# matches = " + str(len(matchLinks)))

    #iterate through match links and populate data
    for n in range(301, len(matchElements)):

        #create new driver for each
        driver = webdriver.Chrome(chrome_options = chrome_options)
        driver.get(matchLinks[n])


        #wait until the html code that you want has appeared
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "mcTabs")))

        formTab = driver.find_element_by_class_name('matchCentreSquadLabelContainer')
        formTab.click()    
        time.sleep(1)
        matchFormation = driver.page_source

        #driver.find_elements_by_xpath("//*[contains(text(), 'Stats')]")
        driver.find_element_by_xpath("//li[@data-tab-index='2']").click()
        time.sleep(1)
        matchStats = driver.page_source
        driver.close()

        formationS = BeautifulSoup(matchStats, 'html.parser')

        #find teams, score and formation
        teams = formationS.find_all('span', class_ = 'long')
        Teams.append([teams[0].string, teams[1].string])

        score = formationS.find(class_ = 'score fullTime')
        Score.append([score.contents[0], score.contents[2]])

        formations = formationS.find_all(class_ = 'matchTeamFormation')
        for j in range(2):
            formations[j] = formations[j].string
        Formation.append(formations)

        #find people who scored/assisted
        events = formationS.find(class_ = 'matchEvents matchEventsContainer')
        scored1 = []
        scored2 = []
        for a in events.find_all('a'):
            if a.parent.parent['class'][0] == 'home':
                for k in range(a.parent.contents[2].count(',') + 1):
                    scored1.append(a.string)
            else:
                for j in range(a.parent.contents[2].count(',') + 1):
                    scored2.append(a.string)

        Scored.append([scored1, scored2])

        assists = formationS.find(class_ = 'assists')
        assists1 = []
        assists2 = []
        for a in assists.find_all('a'):
            if a.parent.parent['class'][0] == 'home':
                for i in range(a.parent.contents[2].count(',') + 1):
                    assists1.append(a.string)
            else:
                for i in range(a.parent.contents[2].count(',') + 1):
                    assists2.append(a.string)
        Assisted.append([assists1, assists2])


        #collect other stats
        statsSoup = BeautifulSoup(matchStats, 'html.parser')
        statsContainer = statsSoup.find(class_ = "matchCentreStatsContainer")

        #iterate through stats table
        stats = statsContainer.find_all('tr')

        for k in range(len(variables)):
            if(k >= len(stats)):
                variables[k].append(0)
                continue

            if(stats[k].string == 'Red cards'):
                statistics = stats[k+1].find_all('p')
            else:
                statistics = stats[k].find_all('p')
            temp = []

            for l in range(len(statistics)):
                if l%3 != 1: #delete name of statistic
                    temp.append(statistics[l].string)

            variables[k].append(temp)


        if(n%50 == 0 and n!=0):
            df = pd.DataFrame({
            'Teams': Teams,
            'Score': Score,
            'Formation': Formation,
            'Scored': Scored,
            'Assisted': Assisted,
            'Posession': Posession,
            'OnTarget': OnTarget,
            'Shots': Shots,
            'Touches': Touches,
            'Passes': Passes,
            'Tackles': Tackles,
            'Clearances': Clearances,
            'Corners': Corners,
            'Offsides': Offsides,
            'Yellows': Yellows,
            'Fouls': Fouls
            })

            df.to_csv('dump16-17' + str(n) + '.csv')

        print("completed page " + str(matchLinks[n]) + '  ' + str(n))


    print("got data")
    #create data frame from lists
    df = pd.DataFrame({
        'Teams': Teams,
        'Score': Score,
        'Formation': Formation,
        'Scored': Scored,
        'Assisted': Assisted,
        'Posession': Posession,
        'OnTarget': OnTarget,
        'Shots': Shots,
        'Touches': Touches,
        'Passes': Passes,
        'Tackles': Tackles,
        'Clearances': Clearances,
        'Corners': Corners,
        'Offsides': Offsides,
        'Yellows': Yellows,
        'Fouls': Fouls
        })


    writer = pd.ExcelWriter('soccer_data16-17.xlsx')
    df.to_excel(writer, 'Sheet1')
    writer.save()

    print("done")


#handles any internet speed errors or random miscounts
while True:
    try:
        scrape_premier()
        break
    except:
        print("Error occured: trying again")
