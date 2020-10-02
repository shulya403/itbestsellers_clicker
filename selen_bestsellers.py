from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import *
import requests
import random
import time
from datetime import datetime
import pandas as pd
from datetime import datetime as dt
import sys

class Clicker(object):

    def __init__(self):

        #proxy_ = "93.171.164.251:8080"
        proxy_ = [
            "109.248.249.33:8081",
            "178.49.188.53:8080",
            "91.217.42.2:8080",
            "79.120.3.122:80",
            "176.32.185.22:8080"
            # "139.180.165.197:3128",
            # "169.57.1.84:8123",
            # "163.172.168.124:3128",
            # "35.169.156.54:3128",
            # "169.57.1.84:25",
            # "169.57.1.85:25",
            # "173.192.128.238:25"
        ]

        for i in range(len(proxy_)):
            options = webdriver.ChromeOptions()
            # options.add_argument('--headless')
            options.add_argument("--window-size=1920,1080")
            #options.add_argument('--proxy-server=%s' % proxy_[i])

            try:
                self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
                self.driver.get("https://www.itbestsellers.ru/")
                # site = self.driver.find_element_by_tag_name("title").text
                # print("site:", site)
                # print(EC.presence_of_element_located((By.TAG_NAME, "title")))
                self.element = WebDriverWait(self.driver, 1).\
                    until(EC.presence_of_element_located((By.NAME, "itbs_top_adv")))
                #self.element.click()
                #self.driver.get("https://yandex.ru/internet/")
                # self.element = WebDriverWait(self.driver, 1).\
                #     until(EC.presence_of_element_located((By.CLASS_NAME, "parameter-header__title")))
                if self.element:
                    print("Сработал: ", proxy_[i])

            except Exception:
                try:
                    response = requests.get("https://yandex.ru/internet/",
                                            proxies={"https": proxy_[i]})
                    print(response.status_code, proxy_[i])
                except requests.exceptions.ProxyError:
                    print("Requests none", proxy_[i])

class Clicker_simple(object):

    exclude = [
        "Номера",
        "Форумы",
        "Об издании",
        "студия iMake",
        "RSS",
        "Подписка на рассылки",
        "Авторизация",
        "bestsellers@itbestsellers.ru",
        "",
        "Создание сайта",
        "Подписка на издание"

    ]

    def __init__(self, counter=0, logfile="log.xlsx", ip="мой домашний"):
        self.options = webdriver.ChromeOptions()
        # self.options.add_argument('--headless')
        self.options.add_argument("--window-size=1920,1080")
        # self.options.add_argument('--proxy-server=%s' % proxy_[i])

        try:
            self.logfile = logfile
            self.df = pd.read_excel(self.logfile, index_col=0)
            if not self.df.empty:
                self.df_counter = len(self.df)
            else:
                self.df_counter = 0
        except Exception as Err:
            print(Err)
            self.df = pd.DataFrame(columns=['Time', 'Page', 'ip'])
            self.df_counter = 0

        self.counter = counter
        self.ip = ip

    def click_random_2(self, delay):


        try:
            self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)
            self.driver.get("https://www.itbestsellers.ru/")
        except Exception:
            print("не вышло")
            #self.driver.close()
            return self.counter

        for i in range(random.randint(1, 6)):
            banner = random.randint(1, 100)
            if banner == 2:
                link_ = self.driver.find_element_by_name("itbs_top_adv")
                link_.click()
                self.Log("BANNER CLICK - itbs_top_adv")
                self.counter += 1
            else:
                try:
                    list_articles_links = self.driver.find_elements_by_tag_name('a')

                    if list_articles_links:
                    #     for i in list_articles_links:
                    #         print(list_articles_links.index(i), i.text)

                        link_ = random.choice(list_articles_links)

                        page_ = link_.text
                        if link_ and (page_ not in self.exclude):
                            print(self.counter, page_)
                            link_.click()
                            self.Log(page_)

                            self.counter += 1
                            time.sleep(random.randint(3, delay))
                    else:
                            print('ничего не нашел')

                except IndexError:
                    print('ничего не нашел')

            self.driver.get("https://www.itbestsellers.ru/")

        self.driver.close()

        return self.counter

    def banner_click(self, adv):
        link_ = self.driver.find_element_by_name(adv)
        link_.click()

        # print(self.counter, "BANNER CLICK - {}".format(adv))
        # adv_page_clicks = random.randint(0, 6)
        # if adv_page_clicks < 4:
        #     adv_page_clicks = 0
        # elif adv_page_clicks < 6:
        #     adv_page_clicks = 1
        # else:
        #     adv_page_clicks = 2
        #
        # for i in range(adv_page_clicks):
        #     link_adv = link_.find_element_by_tag_name('a')

        #    self.random_link_click(random.randint(1, 7))


    def random_link_click(self, delay):

        time.sleep(delay)

        list_links = self.driver.find_elements_by_tag_name('a')

        if list_links:

            link_ = random.choice(list_links)
            try:
                page_ = link_.text
                if page_ not in self.exclude:
                    link_.click()
                    print(self.counter, page_)
                    self.Log(page_)
            except:
                print("Плохой линк")



    def click_random_3(self,
                       delay,
                       page="https://www.itbestsellers.ru/",
                       q=6, #макс число просмотров пользователем
                       ban=100):



        if page == "https://www.itbestsellers.ru/":
            self.counter += 1
            self.Log("HOME itbestsellers.ru")
            print(self.counter, "HOME itbestsellers.ru")

        for i in range(random.randint(1, q)):

            banner = random.randint(1, ban)

            if banner == 2:

                self.banner_click("itbs_top_adv")
                self.counter += 1

            elif banner == 3:

                self.banner_click("itbs_right_adv")
                self.counter += 1

            self.counter += 1

            self.random_link_click(delay)

        return self.counter

    def Log(self, text_):

        counter_ = self.df_counter + self.counter
        self.df.loc[counter_, 'Page'] = text_
        self.df.loc[counter_, 'Time'] = datetime.now()
        self.df.loc[counter_, 'ip'] = self.ip
        # try:
        #     myip = requests.get("https://ramziv.com/ip").text
        #     if myip:
        #         self.df.loc[counter_, 'ip'] = myip
        # except Exception:
        #     print("Глюк ramiz")
        #     pass
        if ((counter_ % 10) == 0):
            try:
                self.df.to_excel(self.logfile)
            except PermissionError:
                pass


def delay_time_rel():
    hur = int(dt.now().hour)
    if 0 <= hur < 3:
        return 1
    elif 3 <= hur < 6:
        return 0.5
    elif 6 <= hur < 7:
        return 2
    elif 7 <= hur < 9:
        return 4
    elif 9 <= hur < 11:
        return 12
    elif 11 <= hur < 13:
        return 16
    elif 13 <= hur < 17:
        return 20
    elif 17 <= hur < 19:
        return 18
    elif 19 <= hur < 21:
        return 12
    elif 21 <= hur <= 22:
        return 6
    else:
        return 3


if __name__ == '__main__':

    counter_ = 0
    random.seed()

    #print(sys.argv)
    ip, Q, delay, deep, ban = "", 0, 0, 0, 0
    for sysarg in sys.argv[1:]:

        if "-ip" in sysarg:
            ip = str(sysarg.replace("-ip=", ""))
        elif "-q" in sysarg:
            Q = int(sysarg.replace("-q=", ""))
        elif "-del" in sysarg:
            delay = int(sysarg.replace("-del=", ""))
        elif "-deep" in sysarg:
            deep = int(sysarg.replace("-deep=", ""))
        elif "-ban" in sysarg:
            ban = int(sysarg.replace("-ban=", ""))
    if ip == "":
        ip = input("ip>")
    if Q == 0:
        Q = 300
    if delay == 0:
        delay = 20
    if deep == 0:
        deep = 6
    if ban == 0:
        ban = 100

    go = Clicker_simple(counter_, logfile="log.xlsx", ip=ip)
    debug = input("Работа?")
    if debug.lower() == "n":
        lag = 1
    else:
        lag = 60

    for i in range(Q):

        delay_ = int(lag / delay_time_rel())
        time.sleep(delay_)

        try:
            go.driver = webdriver.Chrome(ChromeDriverManager().install(), options=go.options)
            go.driver.get("https://www.itbestsellers.ru/")
        except Exception:
            print("не вышло")
            #self.driver.close()
        print(i, delay_)

        counter_ = go.click_random_3(page="https://www.itbestsellers.ru/", delay=delay, ban=ban)
        try:
            go.driver.quit()
        except Exception:
            pass


