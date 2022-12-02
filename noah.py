## custom for noah
# rewards login back up - should work
import argparse
import urllib.parse
from datetime import datetime
from inspect import currentframe
from json import load, loads, JSONDecodeError
from math import ceil
from os import system as systemwrite
from platform import system as system_os
from random import randint
from sys import exit, stdout
from time import sleep as wait
from time import time
from typing import Literal

import requests
from selenium import webdriver as webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoSuchWindowException, \
    ElementNotInteractableException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as WDWait
from webdriver_manager.microsoft import EdgeChromiumDriverManager as DriverManager

_ = \
    "███╗   ███╗▄▄███▄▄·    ██████╗ ███████╗██╗    ██╗ █████╗ ██████╗ ██████╗ ███████╗" \
    "████╗ ████║██╔════╝    ██╔══██╗██╔════╝██║    ██║██╔══██╗██╔══██╗██╔══██╗██╔════╝" \
    "██╔████╔██║███████╗    ██████╔╝█████╗  ██║ █╗ ██║███████║██████╔╝██║  ██║███████╗" \
    "██║╚██╔╝██║╚════██║    ██╔══██╗██╔══╝  ██║███╗██║██╔══██║██╔══██╗██║  ██║╚════██║" \
    "██║ ╚═╝ ██║███████║    ██║  ██║███████╗╚███╔███╔╝██║  ██║██║  ██║██████╔╝███████║" \
    "╚═╝     ╚═╝╚═▀▀▀══╝    ╚═╝  ╚═╝╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝"

#################
#  USER CONFIG  #
#################
credentials_file = 'credentials.json'  # If you downloaded the source files, no need to change this.
skip: int = 2  # default: 0  THIS WILL RETURN AN ERROR WHEN ALL ACCOUNTS ARE COMPLETED AND IT TRIES TO DO THE SKIPPED ONES
redundancy: int = 3  # default: 2
cron: str = "HH:MM"  # when to run script daily in format of HH:MM eg. "15:30" = 5:30 pm

#####################
#  ADVANCED CONFIG  #
#####################
version = "1.0.0"
options = Options()
global json, accounts, tacos, verify_request
email = (By.ID, "i0116")
password = (By.ID, "i0118")
next_button = (By.ID, "idSIButton9")
try:
    json = load(open(credentials_file))
    accounts = json['config']['How many accounts are you using?']
    tacos = json['config']['Do you like tacos?']
    verify_request = json['config']['verify request']
except JSONDecodeError:
    print(
        "\033Error: JSON Failed to decode. Your credentials.json is likely incorrectly configured. Try remaking one by us"
        "ing the template on the github page.\033[00m")
    exit("JSONDecodeError")
credentials = []
sa: list
log_name = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
indexerror: int = 0
keyboardinterupt = False
parser = argparse.ArgumentParser(description='M$ Rewards')
parser.add_argument('--delay', dest='delay', default=False, action='store_true',
                    help='Delay, recommended  if you are running the script at the same time every day. Delay will randomly run the script 1-30 minutes later than normal.')
parser.add_argument('--logs', dest='logs', default=False, action='store_true',
                    help='Logs, recommended if you would like to keep a record of the bot to make sure it has been working daily.')
parser.add_argument('--calculatetime', dest='calculatetime', default=False, action='store_true',
                    help='M$ Calculator is a way to calculate how long it will take to purchase an item using M$ Rewards. To use M$ Calculator, you want to change credentials json according to README.md')
parser.add_argument('--fast', dest='fast', default=False, action='store_true',
                    help="Complete script faster. Generally saves about ~10 minutes per account")
parser.add_argument('--bat', dest='bat', default=False, action='store_true',
                    help='If your running from bat script (not neccersary though)')
args = parser.parse_args()
retries: int = 0
if not args.calculatetime:
    try:
        sa = requests.get("https://www.mit.edu/~ecprice/wordlist.10000", verify=verify_request).text.splitlines()
    except requests.exceptions.RequestException:
        print('\033[91m[ERROR] Failed to load word list, try changing "verify request" in credentials.json\033[00m"')
        exit(1)
for i in json['credentials']:
    credentials.append(i)


###############
#  Functions  #
###############
def create_b_instance(mobile_instance: bool) -> webdriver:
    desktop = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.34',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.34'
    ]
    mobile = [
        'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 EdgiOS/44.5.0.10 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 EdgiOS/100.1185.50 Mobile/15E148 Safari/605.1.15',
        'Mozilla/5.0 (Linux; Android 10; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.79 Mobile Safari/537.36 EdgA/100.0.1185.50'
    ]

    acc_value = stepback(accounts, 2)
    if mobile_instance:
        options.add_argument(f"user-agent={mobile[acc_value]}")
        if acc_value == 0:
            options.add_argument("--window-size=640,1136")  # resolution of iphone 5s
        elif acc_value == 1:
            options.add_argument("--window-size=2778,1284")  # resolution of iphone 13 pro max
        elif acc_value == 2:
            options.add_argument("--window-size=1440,2960")  # resolution of pixel 3xl
    else:
        options.add_argument(f"user-agent={desktop[acc_value]}")
        options.add_argument("--window-size=1920,1080")

    preference = {
        "profile.default_content_setting_values.geolocation": 2,
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "webrtc.ip_handling_policy": "disable_non_proxied_udp",
        "webrtc.multiple_routes_enabled": False,
        "webrtc.nonproxied_udp_enabled": False
    }

    options.add_argument('lang=en-AU')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("prefs", preference)
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    if system_os() == 'Linux':
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        cp('[INFO] Linux detected, enabling "--no-sandbox" and "--disable-dev-shm-usage".', "purple")

    try:
        b = webdriver.Edge(service=Service(DriverManager().install()), options=options)
        b.get('https://login.live.com/')
        return b
    except Exception as exception:
        error(
            str(exception) + "\nThis error was caused by an error in automatic webdriver installation, try manually downloading it at the link above and make sure to change its path directory in credentials.json",
            finishprocess=True, exit_code=1)
    wait(2)
    

def login(userid: int, b: webdriver):
    cp(f"Attempting to log in to {gd(userid)}.", "yellow")
    wait(2 if args.fast else 5)
    WDWait(b, 100).until(ec.element_to_be_clickable(email)).send_keys(gd(userid))
    wait(2 if args.fast else 5)
    WDWait(b, 100).until(ec.element_to_be_clickable(next_button)).click()
    wait(2 if args.fast else 5)
    WDWait(b, 100).until(ec.element_to_be_clickable(password)).send_keys(gd(userid, "password"))
    wait(2 if args.fast else 5)
    WDWait(b, 100).until(ec.element_to_be_clickable(next_button)).click()

    # checks
    if b.title == "We're updating our terms" or element_exist(By.ID, 'iAccrualForm', b=b):
        WDWait(b, 100).until(ec.element_to_be_clickable((By.ID, 'iNext'))).click()

    if b.title == "Your account has been temporarily suspended" or element_exist(By.CLASS_NAME,
                                                                                 "serviceAbusePageContainer  PageContainer",
                                                                                 b=b):
        error("Account Suspended", showlinenumber=False, finishprocess=True)

    if b.title == "Help us protect your account":
        error("Account Locked", showlinenumber=False, finishprocess=True)

    if str(b.current_url).split('?')[0] == "https://account.live.com/proofs/Add":
        error("Account needs additional login info", showlinenumber=False, finishprocess=True)

    cp(f"Successfully logged into {gd(userid)}.", "green")


def logout(userid: int, b: webdriver):
    b.execute_script(f'window.location.href = "https://rewards.bing.com/Signout";')
    cp(f"Successfully logged out of {gd(userid)}.", "green")
    b.execute_script(f'window.location.href = "https://rewards.bing.com/Signout";')
    wait(randint(10, 17) if not args.fast else randint(4, 7))


def search(searches: int, b: webdriver, userid: int):
    search_range = range(1, randint(searches + 1, searches + 10) + 1) if not args.fast else range(0, searches)
    try:
        for _ in search_range:
            d = randint(0, len(sa) - 1)
            b.execute_script(f'window.location.href = "https://bing.com/?q={sa[d]}";')  # haha sad
            sign_in(b, userid)
            sa.pop(d)
            wait(randint(4, 7) if not args.fast else randint(1, 3))
    except Exception as exception:
        error(exception)
        try:
            d = randint(0, len(sa) - 1)
            b.execute_script(f'window.location.href = "https://bing.com/?q={sa[d]}";')  # haha sad v2
            sign_in(b, userid)
            sa.pop(d)
            wait(randint(4, 7) if not args.fast else randint(1, 3))
        except Exception as exception:
            error(exception)

    wait(10)


def cp(text: str, colour: Literal["red", "green", "yellow", "blue", "purple"]) -> None:
    if colour == "red":
        print(f"\033[91m{text}\033[00m")
    elif colour == "green":
        print(f"\033[92m{text}\033[00m")
    elif colour == "yellow":
        print(f"\033[93m{text}\033[00m")
    elif colour == "blue":
        print(f"\033[94m{text}\033[00m")
    elif colour == "purple":
        print(f"\033[95m{text}\033[00m")


def error(text, show_time: bool = True, showlinenumber: bool = True, finishprocess: bool = False, exit_code: int = 0):
    result = f'Error: {text}'

    if showlinenumber:
        result += f"\n  -> Line Number: {currentframe().f_back.f_lineno}"

    if show_time:
        result += f"\n  -> Current Time: {datetime.now().strftime('%H:%M:%S')}"

    cp(result, "red")

    if finishprocess:
        try:
            cp('M$ Rewards closing in five seconds...', 'red')
            wait(5)
            exit(exit_code)
        except KeyboardInterrupt:
            cp('Force exit', "red")


def element_exist(by: By, element: str, b: webdriver) -> bool:
    """if element exists, return true - had to write this because i will very quickly forget wtf im doing"""
    try:
        b.find_element(by, element)
    except NoSuchElementException:
        return False
    return True


def warn(text: str):
    cp(f"[WARNING] {text}", "yellow")


def gd(userid: int, opts: Literal["username", "password"] = "username") -> str:  # gd = get details :)
    return str(credentials[userid][opts])


def dashboard_data(b: webdriver, userid: int) -> dict:
    b.execute_script(f'window.location.href = "https://rewards.bing.com/?signin=1"')
    f, l, s = "var dashboard = ", ";\n        appDataModule.constant(\"prefetchedDashboard\", dashboard);", b.find_element(
        By.XPATH, '/html/body').get_attribute('innerHTML')
    try:
        start = s.index(f) + len(f)
        end = s.index(l, start)
        return loads(s[start:end])
    except Exception as exception:
        error(exception)
        login(userid, b)
        wait(2)
        b.execute_script(f'window.location.href = "https://rewards.bing.com/?signin=1"')
        wait(5)
        try:
            start = s.index(f) + len(f)
            end = s.index(l, start)
            return loads(s[start:end])
        except Exception as exception:
            error(exception)
            login(userid, b)
            wait(2)
            b.execute_script(f'window.location.href = "https://rewards.bing.com/?signin=1"')
            wait(5)


def check_points(b: webdriver, userid: int, prettyprint: bool = True) -> int:
    rg, dd = 'redeemGoal', dashboard_data(b=b, userid=userid)['userStatus']
    points, goal_price = dd['availablePoints'], dd[rg]['price']
    if prettyprint:
        cp(f'[INFO] {gd(userid)} has an account balance of {points} points!', "purple")
        if goal_price <= points:
            cp(f"[VERY GOOD INFO] {gd(userid)} has enough points to redeem {dd[rg]['title']}!", "green")
        else:
            cp(f"[INFO] {gd(userid)} is {round((points / goal_price) * 100, 2)}% of the way to redeeming (a) {dd[rg]['title']}!",
               "purple")
    return int(points)


def logo(legend: bool):
    cp("\n\n███╗   ███╗▄▄███▄▄·    ██████╗ ███████╗██╗    ██╗ █████╗ ██████╗ ██████╗ ███████╗\n████╗ ████║██╔════╝    ██╔══██╗██╔════╝██║    ██║██╔══██╗██╔══██╗██╔══██╗██╔════╝\n██╔████╔██║███████╗    ██████╔╝█████╗  ██║ █╗ ██║███████║██████╔╝██║  ██║███████╗\n██║╚██╔╝██║╚════██║    ██╔══██╗██╔══╝  ██║███╗██║██╔══██║██╔══██╗██║  ██║╚════██║\n██║ ╚═╝ ██║███████║    ██║  ██║███████╗╚███╔███╔╝██║  ██║██║  ██║██████╔╝███████║\n╚═╝     ╚═╝╚═▀▀▀══╝    ╚═╝  ╚═╝╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝",
       "green")
    cp(f"By @Opensourceisgod on Github. v{version}", "blue")
    if legend:
        print("Legend: \033[91m[ERROR] \033[92m[SUCCESS] \033[93m[ATTEMPT] \033[95m[INFO]\n\n")


def complete_daily_set(b: webdriver, userid: int):
    d = dashboard_data(b=b, userid=userid)['dailySetPromotions']
    todaydate, todaypack = datetime.today().strftime('%m/%d/%Y'), []
    for datedate, data in d.items():
        if datedate == todaydate:
            todaypack = data
    for activity in todaypack:
        if not activity['complete']:
            card_number = int(activity['offerId'][-1:])
            if activity['promotionType'] == "urlreward":
                cp(f'[INFO] Completing daily set {str(card_number)} (search)', "purple")
                daily_set_search(card_number, b, userid=userid)
            if activity['promotionType'] == "quiz":
                if activity['pointProgressMax'] == 50 and activity['pointProgress'] == 0:
                    cp(f'[INFO] Completing daily set {str(card_number)} (this or that)', "purple")
                    daily_set_this_or_that(card_number, b, userid)
                elif (activity['pointProgressMax'] == 40 or activity['pointProgressMax'] == 30) and activity[
                    'pointProgress'] == 0:
                    cp(f'[INFO] Completing daily set {str(card_number)} (quiz)', "purple")
                    daily_set_quiz(card_number, b=b, userid=userid)
                elif activity['pointProgressMax'] == 10 and activity['pointProgress'] == 0:
                    search_url = urllib.parse.unquote(
                        urllib.parse.parse_qs(urllib.parse.urlparse(activity['destinationUrl']).query)['ru'][0])
                    search_url_query = urllib.parse.parse_qs(urllib.parse.urlparse(search_url).query)
                    filters = {}
                    for f in search_url_query['filters'][0].split(" "):
                        f = f.split(':', 1)
                        filters[f[0]] = f[1]
                    if "PollScenarioId" in filters:
                        cp(f'[INFO] Completing daily set {str(card_number)} (poll)', "purple")
                        daily_set_survey(card_number, b=b, userid=userid)
                    else:
                        cp(f'[INFO] Completing daily set {str(card_number)} (quiz)', "purple")
                        daily_set_variable_activity(card_number, b=b, userid=userid)


def daily_set_search(card_number: int, b: webdriver, userid: int):
    wait(5)
    b.find_element(By.XPATH,
                   f'//*[@id="app-host"]/ui-view/mee-rewards-dashboard/main/div/mee-rewards-daily-set-section/div/mee-card-group/div/mee-card[{str(card_number)}]/div/card-content/mee-rewards-daily-set-item-content/div/a/div/span').click()
    wait(1)
    b.switch_to.window(window_name=b.window_handles[1])
    sign_in(b, userid)
    wait(4)
    b.close()
    wait(2)
    b.switch_to.window(window_name=b.window_handles[0])
    wait(2)


def daily_set_survey(card_number: int, b: webdriver, userid: int):
    wait(5)
    b.find_element(By.XPATH,
                   f'//*[@id="app-host"]/ui-view/mee-rewards-dashboard/main/div/mee-rewards-daily-set-section/div/mee-card-group/div/mee-card[{str(card_number)}]/div/card-content/mee-rewards-daily-set-item-content/div/a/div/span').click()
    wait(1)
    b.switch_to.window(window_name=b.window_handles[1])
    wait(8)
    sign_in(b, userid)
    wait(4)
    # Accept cookie popup
    if element_exist(By.ID, 'bnp_container', b=b):
        b.find_element(By.ID, 'bnp_btn_accept').click()
        wait(2)
    # Click on later on Bing wallpaper app popup
    if element_exist(By.ID, 'b_notificationContainer_bop', b=b):
        b.find_element(By.ID, 'bnp_hfly_cta2').click()
        wait(2)
    b.find_element(By.ID, "btoption" + str(randint(0, 1))).click()
    wait(4)
    b.close()
    wait(2)
    b.switch_to.window(window_name=b.window_handles[0])
    wait(2)


def daily_set_quiz(card_number: int, b: webdriver, userid: int):
    wait(5)
    b.find_element(By.XPATH,
                   f'//*[@id="app-host"]/ui-view/mee-rewards-dashboard/main/div/mee-rewards-daily-set-section[1]/div/mee-card-group[1]/div[1]/mee-card[{str(card_number)}]/div[1]/card-content[1]/mee-rewards-daily-set-item-content[1]/div[1]/a[1]/div[3]/span[1]').click()
    wait(3)
    b.switch_to.window(window_name=b.window_handles[1])
    sign_in(b, userid)
    wait(12)

    if not wait_until_q_loads(b=b):
        cu = b.current_window_handle
        for handle in b.window_handles:
            if handle != cu:
                b.switch_to.window(handle)
                wait(0.5)
                b.close()
                wait(0.5)
        b.switch_to.window(cu)
        wait(0.5)
        b.get('https://rewards.bing.com/')
        try:
            wait(2)
            login(userid, b)
        except NoSuchElementException:
            pass
        return
    # Accept cookie popup
    if element_exist(By.ID, 'bnp_container', b=b):
        b.find_element(By.ID, 'bnp_btn_accept').click()
        wait(2)
    b.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
    WDWait(b, 100).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]')))
    wait(3)
    number_of_questions = b.execute_script("return _w.rewardsQuizRenderInfo.maxQuestions")
    numberop = b.execute_script("return _w.rewardsQuizRenderInfo.numberOfOptions")
    for question in range(number_of_questions):
        if numberop == 8:
            answers = []
            for asdfghjkl in range(8):
                if b.find_element(By.ID, "rqAnswerOption" + str(asdfghjkl)).get_attribute(
                        "iscorrectoption").lower() == "true":
                    answers.append("rqAnswerOption" + str(asdfghjkl))
            for answer in answers:
                # Click on later on Bing wallpaper app popup
                if element_exist(By.ID, 'b_notificationContainer_bop', b=b):
                    b.find_element(By.ID, 'bnp_hfly_cta2').click()
                    wait(2)
                b.find_element(By.ID, answer).click()
                wait(5)
                if not wait_until_q_loads(b=b, quiz_question="questions"):
                    return
            wait(5)
        elif numberop == 4:
            correct_correct_option = b.execute_script("return _w.rewardsQuizRenderInfo.correctAnswer")
            for asdfghjkl in range(4):
                if b.find_element(By.ID, "rqAnswerOption" + str(asdfghjkl)).get_attribute(
                        "data-option") == correct_correct_option:
                    # Click on later on Bing wallpaper app popup
                    if element_exist(By.ID, 'b_notificationContainer_bop', b=b):
                        b.find_element(By.ID, 'bnp_hfly_cta2').click()
                        wait(2)
                    b.find_element(By.ID, "rqAnswerOption" + str(asdfghjkl)).click()
                    wait(5)
                    if not wait_until_q_loads(b=b, quiz_question="questions"):
                        return
                    break
            wait(5)
    wait(5)
    b.close()
    wait(2)
    b.switch_to.window(window_name=b.window_handles[0])
    wait(2)


def daily_set_variable_activity(card_number: int, b: webdriver, userid: int):
    wait(2)
    b.find_element(By.XPATH,
                   f'//*[@id="app-host"]/ui-view/mee-rewards-dashboard/main/div/mee-rewards-daily-set-section/div/mee-card-group/div/mee-card[{str(card_number)}]/div/card-content/mee-rewards-daily-set-item-content/div/a/div/span').click()
    wait(1)
    b.switch_to.window(window_name=b.window_handles[1])
    sign_in(b, userid)
    wait(8)
    # Accept cookie popup
    if element_exist(By.ID, 'bnp_container', b=b):
        b.find_element(By.ID, 'bnp_btn_accept').click()
        wait(2)
    try:
        b.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
        WDWait(b, 10).until(
            ec.visibility_of_element_located((By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]')))
    except (NoSuchElementException, TimeoutException):
        try:
            counter = str(b.find_element(By.XPATH, '//*[@id="QuestionPane0"]/div[2]').get_attribute('innerHTML'))[
                      :-1][1:]
            noq = max([int(s) for s in counter.split() if s.isdigit()])
            for question in range(noq):
                # Click on later on Bing wallpaper app popup
                if element_exist(By.ID, 'b_notificationContainer_bop', b=b):
                    b.find_element(By.ID, 'bnp_hfly_cta2').click()
                    wait(2)

                b.execute_script(
                    f'document.evaluate("//*[@id=\'QuestionPane{str(question)}\']/div[1]/div[2]/a[{str(randint(1, 3))}]/div", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
                wait(8)
            wait(5)
            b.close()
            wait(2)
            b.switch_to.window(window_name=b.window_handles[0])
            wait(2)
            return
        except NoSuchElementException:
            wait(randint(5, 9))
            b.close()
            wait(2)
            b.switch_to.window(window_name=b.window_handles[0])
            wait(2)
            return
    wait(3)
    ca = b.execute_script("return _w.rewardsQuizRenderInfo.correctAnswer")
    if b.find_element(By.ID, "rqAnswerOption0").get_attribute("data-option") == ca:
        b.find_element(By.ID, "rqAnswerOption0").click()
    else:
        b.find_element(By.ID, "rqAnswerOption1").click()
    wait(10)
    b.close()
    wait(2)
    b.switch_to.window(window_name=b.window_handles[0])
    wait(2)


def daily_set_this_or_that(card_number: int, b: webdriver, userid: int):
    wait(2)
    b.find_element(By.XPATH,
                   f'//*[@id="app-host"]/ui-view/mee-rewards-dashboard/main/div/mee-rewards-daily-set-section/div/mee-card-group/div/mee-card[{str(card_number)}]/div/card-content/mee-rewards-daily-set-item-content/div/a/div/span').click()
    wait(1)
    b.switch_to.window(window_name=b.window_handles[1])
    sign_in(b, userid)
    wait(15)
    if element_exist(By.ID, 'bnp_container', b=b):  # Accept cookie popup
        b.find_element(By.ID, 'bnp_btn_accept').click()
        wait(2)

    if not wait_until_q_loads(b=b):
        cu = b.current_window_handle
        for handle in b.window_handles:
            if handle != cu:
                b.switch_to.window(handle)
                wait(0.5)
                b.close()
                wait(0.5)
        b.switch_to.window(cu)
        wait(0.5)
        b.get('https://rewards.bing.com/')
        try:
            wait(2)
            login(userid, b)
        except NoSuchElementException:
            pass
        return

    b.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
    WDWait(b, 10).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]')))
    wait(5)

    for question in range(10):
        if element_exist(By.ID, 'b_notificationContainer_bop', b=b):  # Click on later on Bing wallpaper app popup
            b.find_element(By.ID, 'bnp_hfly_cta2').click()
            wait(2)

        answer_encode_key = b.execute_script("return _G.IG")
        answer1 = b.find_element(By.ID, "rqAnswerOption0")
        a1title = answer1.get_attribute('data-option')
        a1code = get_answer_code(answer_encode_key, a1title)

        answer2 = b.find_element(By.ID, "rqAnswerOption1")
        a2title = answer2.get_attribute('data-option')
        a2code = get_answer_code(answer_encode_key, a2title)

        correct_answer_code = b.execute_script("return _w.rewardsQuizRenderInfo.correctAnswer")

        if a1code == correct_answer_code:
            answer1.click()
            wait(15)
        elif a2code == correct_answer_code:
            answer2.click()
            wait(15)

    wait(5)
    b.close()
    wait(2)
    b.switch_to.window(window_name=b.window_handles[0])
    wait(2)


def get_answer_code(key: str, string: str) -> str:
    t = 0
    for gac in range(len(string)):
        t += ord(string[gac])
    t += int(key[-2:], 16)
    return str(t)


def wait_until_q_loads(b: webdriver, quiz_question: Literal["quiz", "questions"] = "quiz"):
    tries = 0
    refreshcount = 0
    while True:
        try:
            if quiz_question == "quiz":
                b.find_element(By.XPATH, '//*[@id="currentQuestionContainer"]')
            elif quiz_question == "questions":
                _ = b.find_elements(By.CLASS_NAME, 'rqECredits')[0]
            return True
        except NoSuchElementException:
            if tries < 10:
                tries += 1
                wait(0.5)
            else:
                if refreshcount < 5:
                    b.refresh()
                    refreshcount += 1
                    tries = 0
                    wait(5)
                else:
                    return False


def complete_punch_card(url: str, cpromo: dict, b: webdriver):
    b.get(url)
    for child in cpromo:
        if not child['complete']:
            if child['promotionType'] == "urlreward":
                b.execute_script("document.getElementsByClassName('offer-cta')[0].click()")
                wait(1)
                b.switch_to.window(window_name=b.window_handles[1])
                wait(randint(13, 17))
                b.close()
                wait(2)
                b.switch_to.window(window_name=b.window_handles[0])
                wait(2)
            if child['promotionType'] == "quiz" and child['pointProgressMax'] >= 50:
                b.find_element(By.XPATH,
                               '//*[@id="rewards-dashboard-punchcard-details"]/div[2]/div[2]/div[7]/div[3]/div[1]/a').click()
                wait(1)
                b.switch_to.window(window_name=b.window_handles[1])
                wait(15)
                b.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
                wait(5)
                WDWait(b, 100).until(
                    ec.visibility_of_element_located((By.XPATH, '//*[@id="currentQuestionContainer"]')))
                noq = b.execute_script("return _w.rewardsQuizRenderInfo.maxQuestions")
                aq = b.execute_script(
                    "return _w.rewardsQuizRenderInfo.CorrectlyAnsweredQuestionCount")
                noq -= aq
                for question in range(noq):
                    answer = b.execute_script("return _w.rewardsQuizRenderInfo.correctAnswer")
                    b.find_element(By.XPATH, f'//input[@value="{answer}"]').click()
                    wait(15)
                wait(5)
                b.close()
                wait(2)
                b.switch_to.window(window_name=b.window_handles[0])
                wait(2)
                b.refresh()
                break
            elif child['promotionType'] == "quiz" and child['pointProgressMax'] < 50:
                b.execute_script("document.getElementsByClassName('offer-cta')[0].click()")
                wait(1)
                b.switch_to.window(window_name=b.window_handles[1])
                wait(8)
                counter = str(
                    b.find_element(By.XPATH, '//*[@id="QuestionPane0"]/div[2]').get_attribute('innerHTML'))[:-1][1:]
                noq = max([int(s) for s in counter.split() if s.isdigit()])
                for question in range(noq):
                    b.execute_script(
                        f'document.evaluate("//*[@id=\'QuestionPane{str(question)}\']/div[1]/div[2]/a[{str(randint(1, 3))}]/div", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
                    wait(10)
                wait(5)
                b.close()
                wait(2)
                b.switch_to.window(window_name=b.window_handles[0])
                wait(2)
                b.refresh()
                break


def complete_punch_cards(b: webdriver, userid: int):
    puc = dashboard_data(b, userid)['punchCards']
    for punchCard in puc:
        if punchCard['parentPromotion'] is not None and punchCard['childPromotions'] is not None and \
                punchCard['parentPromotion']['complete'] is False and punchCard['parentPromotion'][
            'pointProgressMax'] != 0:
            url = punchCard['parentPromotion']['attributes']['destination']
            if b.current_url.startswith('https://rewards.'):
                path = url.replace('https://rewards.bing.com', '')
                new_url = 'https://rewards.bing.com/dashboard/'
                uc = path[11:15]
                dest = new_url + uc + path.split(uc)[1]
            else:
                path = url.replace('https://account.microsoft.com/rewards/dashboard/', '')
                new_url = 'https://account.microsoft.com/rewards/dashboard/'
                uc = path[:4]
                dest = new_url + uc + path.split(uc)[1]
            complete_punch_card(dest, punchCard['childPromotions'], b)
    wait(2)
    b.get('https://rewards.bing.com/dashboard/')
    wait(2)


def complete_more_promotion_search(card_number: int, b: webdriver):
    b.find_element(By.XPATH,
                   f'//*[@id="app-host"]/ui-view/mee-rewards-dashboard/main/div/mee-rewards-more-activities-card/mee-card-group/div/mee-card[{str(card_number)}]/div/card-content/mee-rewards-more-activities-card-item/div/a/div/span').click()
    wait(1)
    b.switch_to.window(window_name=b.window_handles[1])
    wait(15)
    b.close()
    wait(2)
    b.switch_to.window(window_name=b.window_handles[0])
    wait(2)


def complete_more_promotion_quiz(card_number: int, b: webdriver):
    b.find_element(By.XPATH,
                   f'//*[@id="app-host"]/ui-view/mee-rewards-dashboard/main/div/mee-rewards-more-activities-card/mee-card-group/div/mee-card[{str(card_number)}]/div/card-content/mee-rewards-more-activities-card-item/div/a/div/span').click()
    wait(1)
    b.switch_to.window(window_name=b.window_handles[1])
    wait(8)
    cqn = b.execute_script("return _w.rewardsQuizRenderInfo.currentQuestionNumber")
    if cqn == 1 and element_exist(By.XPATH, '//*[@id="rqStartQuiz"]', b):
        b.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
    WDWait(b, 100).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]')))
    wait(3)
    numberoq = b.execute_script("return _w.rewardsQuizRenderInfo.maxQuestions")
    questions = numberoq - cqn + 1
    numberop = b.execute_script("return _w.rewardsQuizRenderInfo.numberOfOptions")
    for question in range(questions):
        if numberop == 8:
            answers = []
            for asdfghjkl in range(8):
                if b.find_element(By.ID, "rqAnswerOption" + str(asdfghjkl)).get_attribute(
                        "iscorrectoption").lower() == "true":
                    answers.append("rqAnswerOption" + str(asdfghjkl))
            for answer in answers:
                b.find_element(By.ID, answer).click()
                wait(5)
                if not wait_until_q_loads(b=b, quiz_question="questions"):
                    return
            wait(5)
        elif numberop == 4:
            correct_correct_option = b.execute_script("return _w.rewardsQuizRenderInfo.correctAnswer")
            for asdfghjkl in range(4):
                if b.find_element(By.ID, "rqAnswerOption" + str(asdfghjkl)).get_attribute(
                        "data-option") == correct_correct_option:
                    b.find_element(By.ID, "rqAnswerOption" + str(asdfghjkl)).click()
                    wait(5)
                    if not wait_until_q_loads(b=b, quiz_question="questions"):
                        return
                    break
            wait(5)
    wait(5)
    b.close()
    wait(2)
    b.switch_to.window(window_name=b.window_handles[0])
    wait(2)


def complete_more_promotions_abc(card_number: int, b: webdriver):
    b.find_element(By.XPATH,
                   f'//*[@id="app-host"]/ui-view/mee-rewards-dashboard/main/div/mee-rewards-more-activities-card/mee-card-group/div/mee-card[{str(card_number)}]/div/card-content/mee-rewards-more-activities-card-item/div/a/div/span').click()
    wait(1)
    b.switch_to.window(window_name=b.window_handles[1])
    wait(8)
    counter = str(b.find_element(By.XPATH, '//*[@id="QuestionPane0"]/div[2]').get_attribute('innerHTML'))[:-1][1:]
    noq = max([int(s) for s in counter.split() if s.isdigit()])
    for question in range(noq):
        b.execute_script(
            f'document.evaluate("//*[@id=\'QuestionPane{str(question)}\']/div[1]/div[2]/a[{str(randint(1, 3))}]/div", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
        wait(8)
    wait(5)
    b.close()
    wait(2)
    b.switch_to.window(window_name=b.window_handles[0])
    wait(2)


def complete_more_promotion_this_or_that(card_number: int, b: webdriver):
    b.find_element(By.XPATH,
                   f'//*[@id="app-host"]/ui-view/mee-rewards-dashboard/main/div/mee-rewards-more-activities-card/mee-card-group/div/mee-card[{str(card_number)}]/div/card-content/mee-rewards-more-activities-card-item/div/a/div/span').click()
    wait(1)
    b.switch_to.window(window_name=b.window_handles[1])
    wait(8)
    cqn = b.execute_script("return _w.rewardsQuizRenderInfo.currentQuestionNumber")
    number_of_questions_left = 10 - cqn + 1
    if cqn == 1 and element_exist(By.XPATH, '//*[@id="rqStartQuiz"]', b=b):
        b.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
    WDWait(b, 100).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]')))
    wait(3)
    for question in range(number_of_questions_left):
        aek = b.execute_script("return _G.IG")

        answer1 = b.find_element(By.ID, "rqAnswerOption0")
        a1t = answer1.get_attribute('data-option')
        a1c = get_answer_code(aek, a1t)

        answer2 = b.find_element(By.ID, "rqAnswerOption1")
        a2t = answer2.get_attribute('data-option')
        a2c = get_answer_code(aek, a2t)

        cad = b.execute_script("return _w.rewardsQuizRenderInfo.correctAnswer")

        if a1c == cad:
            answer1.click()
            wait(8)
        elif a2c == cad:
            answer2.click()
            wait(8)
    wait(5)
    b.close()
    wait(2)
    b.switch_to.window(window_name=b.window_handles[0])
    wait(2)


def complete_more_promotions(b: webdriver, userid: int):
    mp = dashboard_data(b=b, userid=userid)['morePromotions']
    itera = 0
    for promotion in mp:
        itera += 1
        if promotion['complete'] is False and promotion['pointProgressMax'] != 0:
            if promotion['promotionType'] == "urlreward":
                complete_more_promotion_search(itera, b=b)
            elif promotion['promotionType'] == "quiz":
                if promotion['pointProgressMax'] == 10:
                    complete_more_promotions_abc(itera, b=b)
                elif promotion['pointProgressMax'] == 30 or promotion['pointProgressMax'] == 40:
                    complete_more_promotion_quiz(itera, b=b)
                elif promotion['pointProgressMax'] == 50:
                    complete_more_promotion_this_or_that(itera, b=b)
            else:
                if promotion['pointProgressMax'] == 100 or promotion['pointProgressMax'] == 200:
                    complete_more_promotion_search(itera, b=b)
        if promotion['complete'] is False and promotion['pointProgressMax'] == 100 and promotion[
            'promotionType'] == "" and promotion['destinationUrl'] == "https://rewards.bing.com":
            complete_more_promotion_search(itera, b=b)


def sign_in(b: webdriver, userid: int):
    """for those stupid times when it doesn't register you signing in"""
    if str(b.current_url).split('?')[0] == "https://www.bing.com/rewards/signin":
        # desktop_browser.findElement(By.xpath("//a[@href='/docs/configuration']")).click();
        WDWait(b, 100).until(ec.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/span/a"))).click()
        cp("[INFO] Re-signed in, due to a bug in Microsoft Rewards.", "purple")
        wait(1)

    if str(b.current_url).split('?')[0] == "https://login.live.com/login.srf":
        WDWait(b, 100).until(ec.element_to_be_clickable(password)).send_keys(gd(userid, "password"))
        WDWait(b, 100).until(ec.element_to_be_clickable(next_button)).click()


def mobile_sign_in(userid: int, b: webdriver):
    b.execute_script(f'window.location.href = "https://bing.com/?q={sa[randint(0, len(sa) - 1)]}";')
    wait(2)
    b.find_element(By.ID, 'mHamburger').click()
    wait(5)

    try:
        WDWait(b, 100).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="HBSignIn"]/a[1]'))).click()
    except NoSuchElementException:
        return

    wait(3)

    try:
        if b.find_element(By.ID, 'id_s').text == "Sign in":
            WDWait(b, 100).until(ec.element_to_be_clickable((By.ID, 'id_s'))).click()
    except NoSuchElementException:
        pass

    try:
        if b.find_element(By.ID, 'hb_n').text.lower().replace(" ", "") in gd(userid,
                                                                             "username"):  # or not element_exist(By.ID, 'hb_s', desktop_browser=desktop_browser):
            return
        else:
            WDWait(b, 100).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="id_prov_cont"]'))).click()
            wait(0.5)
            WDWait(b, 100).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="hb_idproviders"]/a'))).click()
            wait(4)
            cp('[INFO] Bing did not automatically connect to your specified M$ Rewards account, it has automatically been resolved now.',
               "purple")
    except NoSuchElementException:
        pass


def another_stupid_sign_in(userid: int, b: webdriver):
    b.execute_script(f'window.location.href = "https://bing.com/?q={sa[randint(0, 9999)]}";')
    wait(2)

    try:
        if b.find_element(By.ID, 'id_s').text == "Sign in":
            WDWait(b, 100).until(ec.element_to_be_clickable((By.ID, 'id_s'))).click()
    except NoSuchElementException:
        pass

    try:
        if b.find_element(By.ID, 'id_n').text.lower().replace(" ", "") in gd(userid):
            return
        else:
            try:
                WDWait(b, 100).until(ec.element_to_be_clickable((By.ID, 'id_n'))).click()
            except ElementClickInterceptedException:
                WDWait(b, 100).until(ec.element_to_be_clickable((By.ID, 'id_p'))).click()
            finally:
                wait(0.5)
                WDWait(b, 100).until(
                    ec.element_to_be_clickable((By.XPATH, '//*[@id="b_idProviders"]/li[1]/a/span[2]'))).click()
                wait(4)
                cp('[INFO] Bing did not automatically connect to your specified M$ Rewards account, it has automatically be'
                   'en resolved now.', "purple")
                b.switch_to.window(window_name=b.window_handles[0])
    except NoSuchElementException:
        pass

    wait(2)
    b.execute_script('window.location.href = "https://rewards.bing.com/?signin=1"')
    wait(3)

    if "/welcome" in b.current_url:
        wait(3)
        WDWait(b, 100).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="raf-signin-link-id"]'))).click()
        try:
            wait(2)
            login(userid, b)
        except NoSuchElementException:
            pass
        cp('[INFO] Microsoft Rewards did not automatically connect to your specified M$ Rewards account, it has automatically been resolved now.',
           "purple")


def calculate(microsoft_gift_card: bool, purchase_cost: int, acc: int, daily_points: int):
    needed_gift_cards = ceil(purchase_cost / 5)
    needed_points_per_account = 0
    if acc == 1:
        if microsoft_gift_card:
            needed_points_per_account += needed_gift_cards * 4750
        else:
            needed_points_per_account += needed_gift_cards * 6750
        estimated_time = ceil(needed_points_per_account / daily_points)
        excess_value = purchase_cost - (needed_gift_cards * 5)
        print(
            f'It will take {estimated_time} days to get {needed_gift_cards} $5 gift cards to purchase your item that costs ${purchase_cost}, therefore an excess giftcard value of ${excess_value}')
        return estimated_time
    elif acc >= 2:
        gift_cards_needed_per_account = ceil(needed_gift_cards / acc)

        if microsoft_gift_card:
            needed_points_per_account += gift_cards_needed_per_account * 4750
        else:
            needed_points_per_account += gift_cards_needed_per_account * 6750
        estimated_time = ceil(needed_points_per_account / daily_points)
        excess_value = (gift_cards_needed_per_account * 5 * acc) - purchase_cost
        cp(f'It is estimated that it will take {estimated_time} days to get {needed_gift_cards} $5 gift cards ({gift_cards_needed_per_account} giftcards on each of the {acc} accounts) to purchase your item that costs ${purchase_cost}, leaving you an excess giftcard value of ${excess_value}!',
           "green")
        return estimated_time
    else:
        error("invalid account number")


def stepback(number: int, maximum: int) -> int:
    """if number is higher than x return back to 0 and repeat.
    eg. if number = 7 and maximum = 2 the result is 1
    because 0 1 2  0 1 2  0 1  (it's starting at 0)"""
    iteration, result = 0, 0
    if (number <= maximum) or (number <= 0):
        return number

    for _ in range(0, number):
        if result == maximum:
            result = 0
        else:
            result += 1

    return result


def closebrowser(b: webdriver):
    loop: bool = True
    while loop:
        try:
            b.close()
        except NoSuchWindowException:
            loop = False


class Timer:
    def __init__(self):
        self.timer_start = 0
        self.timer_end = 0

    def start(self):
        """Start Timer"""
        self.timer_start = time()

    def end(self):
        """End Timer (Optional)"""
        self.timer_end = time()

    def result(self, print_result: bool = True, colour: Literal["red", "green", "yellow", "blue", "purple"] = "blue"):
        """Print Result"""
        if self.timer_end == 0:
            self.timer_end = time()

        if self.timer_start == 0:
            return error("Timer.start() non-existant. Start the timer stupid.")
        secs = self.timer_end - self.timer_start
        mins = secs // 60
        sec = secs % 60
        hours = mins // 60
        mins = mins % 60
        elapsed_time = f"\nElapsed Time: {int(hours)} hours, {int(mins)} minutes, and {int(sec)} seconds\n"
        if print_result:
            cp(elapsed_time, colour)
        return elapsed_time


class Terminal:
    def __init__(self, start_text: str = "", end_text: str = ""):
        self.start = start_text
        self.end = end_text
        self.cls = "cls"

    def write(self, text: str):
        stdout.write(self.start + text + self.end)

    def clear(self):
        systemwrite(self.cls)


#############
#  Execute  #
#############
def main(retry: int):
    try:
        for mainuserid in range(accounts):
            u = mainuserid + skip

            # Desktop search
            try:
                desktop_browser = create_b_instance(mobile_instance=False)

                try:
                    login(u, desktop_browser)
                except Exception as e:
                    error(e)
                    try:
                        login(u, desktop_browser)
                    except Exception as e:
                        error(e)

                wait(5)

                try:
                    another_stupid_sign_in(userid=u, b=desktop_browser)
                except Exception as e:
                    error(e)
                    try:
                        another_stupid_sign_in(u, desktop_browser)
                    except Exception as e:
                        error(e)

                wait(60 if not args.fast else 10)

                try:
                    check_points(desktop_browser, u)
                except Exception as e:
                    error(e)
                    try:
                        check_points(desktop_browser, u)
                    except Exception as e:
                        error(e)

                try:
                    complete_daily_set(desktop_browser, u)
                except Exception as e:
                    error(e)
                    try:
                        complete_daily_set(desktop_browser, u)
                    except Exception as e:
                        error(e)

                wait(60 if not args.fast else 10)

                try:
                    complete_punch_cards(desktop_browser, u)
                except Exception as e:
                    error(e)
                    try:
                        complete_punch_cards(desktop_browser, u)
                    except Exception as e:
                        error(e)

                wait(60 if not args.fast else 10)

                try:
                    complete_more_promotions(desktop_browser, u)
                except Exception as e:
                    error(e)
                    try:
                        complete_more_promotions(desktop_browser, u)
                    except Exception as e:
                        error(e)

                wait(60 if not args.fast else 10)
                search(34, desktop_browser, u)
                wait(20)

                try:
                    logout(u, desktop_browser)
                except Exception as e:
                    error(e)
                    try:
                        logout(u, desktop_browser)
                    except Exception as e:
                        error(e)

                wait(2)

                try:
                    desktop_browser.close()
                except Exception as e:
                    error(e)
                    try:
                        desktop_browser.close()
                    except Exception as e:
                        error(e)
                cp(f"[SUCCESS] {gd(u)} has completed it's daily desktop Microsoft Reward tasks, now trying mobile searches.",
                   "green")
            except NoSuchWindowException:
                timer.result(print_result=True, colour="red")
                error("M$ Rewards stopped. (Window closed forcefully)", showlinenumber=False, finishprocess=True)
            except TimeoutException or TimeoutError as err:
                timer.result(print_result=True, colour="red")
                error(f"M$ Rewards stopped. (Timed out) Read below for more deatils\n{err}", showlinenumber=False,
                      finishprocess=True)
            except IndexError:
                timer.result(print_result=True, colour="red")
                error(f"M$ Rewards stopped. (Out of index. index: {u})")
            except Exception as e:
                error(e)
                try:
                    desktop_browser = create_b_instance(mobile_instance=False)

                    try:
                        login(u, desktop_browser)
                    except Exception as e:
                        error(e)
                        try:
                            login(u, desktop_browser)
                        except Exception as e:
                            error(e)

                    wait(5)

                    try:
                        another_stupid_sign_in(userid=u, b=desktop_browser)
                    except Exception as e:
                        error(e)
                        try:
                            another_stupid_sign_in(u, desktop_browser)
                        except Exception as e:
                            error(e)

                    wait(60 if not args.fast else 10)

                    try:
                        check_points(desktop_browser, u)
                    except Exception as e:
                        error(e)
                        try:
                            check_points(desktop_browser, u)
                        except Exception as e:
                            error(e)

                    try:
                        complete_daily_set(desktop_browser, u)
                    except Exception as e:
                        error(e)
                        try:
                            complete_daily_set(desktop_browser, u)
                        except Exception as e:
                            error(e)

                    wait(60 if not args.fast else 10)

                    try:
                        complete_punch_cards(desktop_browser, u)
                    except Exception as e:
                        error(e)
                        try:
                            complete_punch_cards(desktop_browser, u)
                        except Exception as e:
                            error(e)

                    wait(60 if not args.fast else 10)

                    try:
                        complete_more_promotions(desktop_browser, u)
                    except Exception as e:
                        error(e)
                        try:
                            complete_more_promotions(desktop_browser, u)
                        except Exception as e:
                            error(e)

                    wait(60 if not args.fast else 10)
                    search(34, desktop_browser, u)
                    wait(20)

                    try:
                        logout(u, desktop_browser)
                    except Exception as e:
                        error(e)
                        try:
                            logout(u, desktop_browser)
                        except Exception as e:
                            error(e)

                    wait(2)

                    try:
                        desktop_browser.close()
                    except Exception as e:
                        error(e)
                        try:
                            desktop_browser.close()
                        except Exception as e:
                            error(e)
                    cp(f"[SUCCESS] {gd(u)} has completed it's daily desktop Microsoft Reward tasks, now trying mobile searches.",
                       "green")
                except Exception as e:
                    error(e)

            # Mobile search
            try:
                mobile_desktop = create_b_instance(mobile_instance=True)

                try:
                    login(u, mobile_desktop)
                except Exception as e:
                    error(e)
                    try:
                        login(u, mobile_desktop)
                    except Exception as e:
                        error(e)

                wait(5)

                try:
                    mobile_sign_in(u, mobile_desktop)
                except Exception as e:
                    error(e)
                    try:
                        mobile_sign_in(u, mobile_desktop)
                    except Exception as e:
                        error(e)

                wait(5)
                search(30, mobile_desktop, u)
                wait(60 if not args.fast else 10)

                wait(5)

                try:
                    mobile_desktop.execute_script('window.location.href = "https://rewards.bing.com/?signin=1"')
                    wait(3)
                    check_points(mobile_desktop, u)
                except ElementNotInteractableException:
                    cp("[Error] Unable to retrieve current points", "red")

                wait(5)

                try:
                    logout(u, mobile_desktop)
                except Exception as e:
                    error(e)
                    try:
                        logout(u, mobile_desktop)
                    except Exception as e:
                        error(e)

                wait(2)
                try:
                    mobile_desktop.close()
                except Exception as e:
                    error(e)
                    try:
                        mobile_desktop.close()
                    except Exception as e:
                        error(e)

                wait(5)
            except NoSuchWindowException:
                timer.result(print_result=True, colour="red")
                error("M$ Rewards stopped. (Window closed forcefully)", showlinenumber=False, finishprocess=True)
            except TimeoutException or TimeoutError as err:
                timer.result(print_result=True, colour="red")
                error(f"M$ Rewards stopped. (Timed out) Read below for more deatils\n{err}", showlinenumber=False,
                      finishprocess=True)
            except IndexError:
                timer.result(print_result=True, colour="red")
                error(f"M$ Rewards stopped. (Out of index. index: {u})")
            except Exception as e:

                error(e)
                try:
                    mobile_desktop = create_b_instance(mobile_instance=True)

                    try:
                        login(u, mobile_desktop)
                    except Exception as e:
                        error(e)
                        try:
                            login(u, mobile_desktop)
                        except Exception as e:
                            error(e)

                    wait(5)

                    try:
                        mobile_sign_in(u, mobile_desktop)
                    except Exception as e:
                        error(e)
                        try:
                            mobile_sign_in(u, mobile_desktop)
                        except Exception as e:
                            error(e)

                    wait(5)
                    search(30, mobile_desktop, u)
                    wait(60 if not args.fast else 10)

                    wait(5)

                    try:
                        mobile_desktop.execute_script('window.location.href = "https://rewards.bing.com/?signin=1"')
                        wait(3)
                        check_points(mobile_desktop, u)
                    except ElementNotInteractableException:
                        cp("[Error] Unable to retrieve current points", "red")

                    wait(5)

                    try:
                        logout(u, mobile_desktop)
                    except Exception as e:
                        error(e)
                        try:
                            logout(u, mobile_desktop)
                        except Exception as e:
                            error(e)

                    wait(2)
                    try:
                        mobile_desktop.close()
                    except Exception as e:
                        error(e)
                        try:
                            mobile_desktop.close()
                        except Exception as e:
                            error(e)

                    wait(5)
                except Exception as e:
                    error(e)
    except KeyboardInterrupt:
        timer.result(print_result=True, colour="red")
        error("M$ Rewards stopped. (Keyboard interrupt)", showlinenumber=False, finishprocess=True)
    # terrible redunancy method but hopefully it's all gucci :)
    except Exception as e:
        error(f"{e}\n  -> Unknown error, please read the above error message or submit it to Github")
        if retry <= 5:
            retry += 1
            main(retry)


if __name__ == '__main__':
    timer = Timer()
    timer.start()

    terminal = Terminal()
    terminal.clear()

    logo(True if args.calculatetime is False else False)

    if args.bat:
        cp("[INFO] Running from .bat", "purple")

    if args.fast:
        cp("[INFO] Fast mode enabled", "purple")

    if skip >= 1:
        warn(f"Skipping {skip} account" if accounts == 1 else f"Skipping {skip} accounts")

    if tacos != "yes":
        error("You do not like tacos. Script will not run until you fix your opinion in credentials.json",
              finishprocess=True)

    if args.delay:
        delay = randint(1, 30) * 60  # 1-30 minutes
        cp(f"[INFO] Delay Enabled (Delayed for {delay} minutes.)", "purple")
        wait(delay)

    if args.calculatetime:
        calculate(
            microsoft_gift_card=json['calculate time config']['redeem as microsoft gift card?'],
            purchase_cost=json['calculate time config'][
                "How much does it cost to buy your item"],
            acc=json['config']['How many accounts are you using?'],
            daily_points=json['calculate time config']['estimated daily points'])

    if args.calculatetime is False:
        for _ in range(redundancy):
            # cron
            if cron == "HH:MM":
                main(retries)
            if cron == ("" or None):
                error("CRON FAILED")
            else:
                while True:
                    if datetime.now().strftime("%H:%M") == cron:
                        main(retries)
                    wait(30)

    terminal.write(f"\n{timer.result(False)}" if args.calculatetime is False else "")
    input("Click 'enter' to exit... ")
