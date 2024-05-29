from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import re
import pandas as pd 


url = 'https://www.apwin.com/'
browser = webdriver.Chrome()
browser.get(url=url)

sleep(3)
site = browser.page_source
soup = BeautifulSoup(site,'html.parser')

games = soup.find_all('div',class_='apw-accordion-content')
qtd_games=len(games)

list_=[]
dict_={}

for i in range(0,qtd_games):

    chanpionship = soup.find_all('div',class_=re.compile(r'apw-accordion-title [0-9a-z- ]+ has-background-primary-light',flags=re.I))[i]
    chanpionship = chanpionship.find('h3',class_='is-flex-grow-1').get_text(' ',strip=True)
    games = soup.find_all('div',class_='apw-accordion-content')
    
    for j in games[i]:
        try:
            game = j.get_text(' ',strip=True)
            team_home = game[5:].replace(' ','-').replace('-x-',' ').split()[0].replace('-',' ').strip()
            team_away = game[5:].replace(' ','-').replace('-x-',' ').split()[1].replace('-',' ').strip()
            time_ = re.findall(r'[0-9:]+',game)[0]
            
            dict_['time']=time_
            dict_['team_home']=team_home
            dict_['team_away']=team_away
            dict_['chanpionship']=chanpionship
            list_.append(dict_.copy())

        except:
            pass
    

df =  pd.DataFrame(list_)
df.to_excel('GamesDay.xlsx',index=False)

sleep(2)
browser.close()
