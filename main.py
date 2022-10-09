import urllib.parse
from datetime import datetime
from inspect import currentframe
from json import load, loads
from platform import system as psys
from random import randint
from sys import exit
from time import sleep as wait
from typing import Literal
import requests
from selenium import webdriver as w
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as WDWait
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service

q = \
    "███╗   ███╗▄▄███▄▄·    ██████╗ ███████╗██╗    ██╗ █████╗ ██████╗ ██████╗ ███████╗" \
    "████╗ ████║██╔════╝    ██╔══██╗██╔════╝██║    ██║██╔══██╗██╔══██╗██╔══██╗██╔════╝" \
    "██╔████╔██║███████╗    ██████╔╝█████╗  ██║ █╗ ██║███████║██████╔╝██║  ██║███████╗" \
    "██║╚██╔╝██║╚════██║    ██╔══██╗██╔══╝  ██║███╗██║██╔══██║██╔══██╗██║  ██║╚════██║" \
    "██║ ╚═╝ ██║███████║    ██║  ██║███████╗╚███╔███╔╝██║  ██║██║  ██║██████╔╝███████║" \
    "╚═╝     ╚═╝╚═▀▀▀══╝    ╚═╝  ╚═╝╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝"

############
#  CONFIG  #
############
version_number = "0.9.3 BETA"
options = Options()
json = load(open('credentials.json'))
credentials = []
system = psys()
cf = currentframe()
accounts = json['config']['How many accounts are you using?']
tacos = json['config']['Do you like tacos?']
log_name = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
log_status = True
email = (By.ID, "i0116")
password = (By.ID, "i0118")
next_button = (By.ID, "idSIButton9")
uuid = 0
for i in json['credentials']:
    credentials.append(i)


###############
#  Functions  #
###############
def create_b_instance(mobile_instance: Literal[True, False]) -> w:
    desktop = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53'
    mobile = 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 EdgiOS/44.5.0.10 Mobile/15E148 Safari/604.1'
    if mobile_instance:
        options.add_argument(f"user-agent={mobile}")
    else:
        options.add_argument(f"user-agent={desktop}")
    options.add_argument('lang=en-AU')
    options.add_argument('--disable-blink-features=AutomationControlled')
    preference = {"profile.default_content_setting_values.geolocation": 2,
                  "credentials_enable_service": False,
                  "profile.password_manager_enabled": False,
                  "webrtc.ip_handling_policy": "disable_non_proxied_udp",
                  "webrtc.multiple_routes_enabled": False,
                  "webrtc.nonproxied_udp_enabled": False}
    options.add_experimental_option("prefs", preference)
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    if psys() == 'Linux':
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        cp('[INFO] Linux detected, enabling "--no-sandbox" and "--disable-dev-shm-usage".', "purple")
    webdriver_path = json['config']['webdriver location']
    if webdriver_path.endswith(".exe"):
        b = w.Edge(executable_path=webdriver_path, options=options)
    else:
        cp('[WARNING] The specified webdriver path in credentials.json is invalid, M$ Rewards has automatically reverted to the automatic edge driver manager. This could cause issues for users without Administrator. However if you recieve no errors, you are free to run this configuration, otherwise read further. Keep in mind, the full path should be entered, eg. "C://Webdrivers/msedgedriver.exe". If you are unsure what this means, follow the following steps:'
           '1. Go to C: in file explorer'
           '2. Create a folder called "Utility" (this does not require administrator)'
           '3. Download the latest msedgedriver at https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/ and place the file in C://Utility'
           '4. Open credentials.json and paste in "C://Webdrivers/msedgedriver.exe"', "yellow")
        b = w.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)

    return b


def login(userid: int, b: w):
    global uuid
    uuid = userid
    b.get('https://login.live.com/')
    cp(f"Attempting to log in to {gd(userid)}.", "yellow")
    wait(1)
    WDWait(b, 100).until(ec.element_to_be_clickable(email)).send_keys(gd(userid))
    wait(1)
    WDWait(b, 100).until(ec.element_to_be_clickable(next_button)).click()
    wait(1)
    WDWait(b, 100).until(ec.element_to_be_clickable(password)).send_keys(gd(userid, "password"))
    wait(1)
    WDWait(b, 100).until(ec.element_to_be_clickable(next_button)).click()
    wait(2)
    if b.title == "We're updating our terms" or element_exist(By.ID, 'iAccrualForm', b=b):
        WDWait(b, 100).until(ec.element_to_be_clickable((By.ID, 'iNext'))).click()
    if b.title == "Your account has been temporarily suspended" or element_exist(By.CLASS_NAME,
                                                                                 "serviceAbusePageContainer  PageContainer", b=b):
        error("Account Suspended", line_number=False, finish_process=True)
    if b.title == "Help us protect your account":
        error("Account Locked", line_number=False, finish_process=True)
    if str(b.current_url).split('?')[0] == "https://account.live.com/proofs/Add":
        error("Account needs additional login info", line_number=False, finish_process=True)
    cp(f"Successfully logged into {gd(userid)}.", "green")


def logout(userid: int, b: w):
    b.execute_script(f'window.location.href = "https://rewards.bing.com/Signout";')
    cp(f"Successfully logged out of {gd(userid)}.", "green")
    b.execute_script(f'window.location.href = "https://rewards.bing.com/Signout";')
    wait(randint(15, 20))


def search(searches: int, b: w):
    sa = requests.get("https://www.mit.edu/~ecprice/wordlist.10000").text.splitlines()  # sa = search array
    try:
        for abcdefghijklmnopqrstuvwxyz in range(1, randint(searches + 1, searches + 10) + 1):
            d = randint(0, len(sa) - 1)
            b.execute_script(f'window.location.href = "https://bing.com/?q={sa[d]}";')  # haha sad
            sign_in(b)
            sa.pop(d)
            wait(randint(4, 7))
    except Exception as e:
        error(e)
        try:
            d = randint(0, len(sa) - 1)
            b.execute_script(f'window.location.href = "https://bing.com/?q={sa[d]}";')  # haha sad v2
            sign_in(b)
            sa.pop(d)
            wait(randint(4, 11))
        except Exception as e:
            error(e)

    wait(randint(34, 64))


def cp(text: str, colour: Literal["red", "green", "yellow", "blue", "purple"], write_log: bool = False) -> None:
    if colour == "red":
        print(f"\033[91m{text}\033[00m")
    elif colour == "green":
        print(f"\033[92m{text}\033[00m")
    elif colour == "yellow":
        print(f"\033[93m{text}\033[00m")
    elif colour == "blue":
        print(f"\033[94m{text}\033[00m")
    else:
        print(f"\033[95m{text}\033[00m")
    if write_log:
        return


def error(text, current_time: bool = True, line_number: bool = True, finish_process: bool = False, exit_code: int = 0):
    result = f'Error: {text}'
    if line_number:
        result += f"\n  -> Line Number: {cf}"
    if current_time:
        result += f"\n  -> Current Time: {datetime.now().strftime('%H:%M:%S')}"
    if finish_process:
        input('Press any key to close...')
        exit(exit_code)


def element_exist(_by: By, element: str, b: w) -> bool:
    """if element exists, return true - had to write this because i will very quickly forget wtf im doing"""
    try:
        b.find_element(_by, element)
    except NoSuchElementException:
        return False
    return True


# def log(logs: str = "n/a", initialize: bool = False) -> None:
#     if initialize:
#         try:
#             with open(f'logs/{log_name}', 'w') as f:
#                 f.write('[Initialize] Logs initialized.\n')
#         except FileNotFoundError:
#             error("Unable to write logs. M$ Rewards will continue to run, however no information will be recorded."
#                   "If you would like to exit now, please CTRL+C in the next five seconds.")
#             wait(5)
#     else:
#         if log_status:
#             try:
#                 f = open("logs/{log_name}", "a")
#                 f.write(f'[{datetime.now().strftime("%H:%M:%S")}] {logs}')
#                 f.close()
#             except Exception as e:
#                 error(f'Logs failed to update. ({e})', line_number=True)
#         else:
#             cp("[WARNING] Logs failed to update.", "yellow")


def gd(uid: int, opt: Literal["username", "password"] = "username") -> str:  # gd = get details :)
    return str(credentials[uid][opt])


def dashboard_data(b: w, open_link: bool = True) -> dict:
    if open_link:
        b.execute_script(f'window.location.href = "https://rewards.microsoft.com/"')
    f, l, s = "var dashboard = ", ";\n        appDataModule.constant(\"prefetchedDashboard\", dashboard);", b.find_element(
        By.XPATH, '/html/body').get_attribute('innerHTML')
    try:
        start = s.index(f) + len(f)
        end = s.index(l, start)
        return loads(s[start:end])
    except ValueError:
        return {}


def check_points(b: w, userid: int, prettyprint: bool = True) -> int:
    rg, dd = 'redeemGoal', dashboard_data(b=b)['userStatus']
    points, goal_price = dd['availablePoints'], dd[rg]['price']
    if prettyprint:
        cp(f'[INFO] {gd(userid)} has an account balance of {points} points!', "purple")
        if goal_price <= points:
            cp(f"[VERY GOOD INFO] {gd(userid)} has enough points to redeem {dd[rg]['title']}!", "green")
        else:
            cp(f"[INFO] {gd(userid)} is {points / goal_price}% of the way to redeeming (a) {dd[rg]['title']}!",
               "purple")
    return int(points)


def logo():
    cp("███╗   ███╗▄▄███▄▄·    ██████╗ ███████╗██╗    ██╗ █████╗ ██████╗ ██████╗ ███████╗\n████╗ ████║██╔════╝    ██╔══██╗██╔════╝██║    ██║██╔══██╗██╔══██╗██╔══██╗██╔════╝\n██╔████╔██║███████╗    ██████╔╝█████╗  ██║ █╗ ██║███████║██████╔╝██║  ██║███████╗\n██║╚██╔╝██║╚════██║    ██╔══██╗██╔══╝  ██║███╗██║██╔══██║██╔══██╗██║  ██║╚════██║\n██║ ╚═╝ ██║███████║    ██║  ██║███████╗╚███╔███╔╝██║  ██║██║  ██║██████╔╝███████║\n╚═╝     ╚═╝╚═▀▀▀══╝    ╚═╝  ╚═╝╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝",
       "green")
    cp(f"By @Opensourceisgod on Github. V{version_number}", "blue")
    print("Legend: \033[91m[ERROR] \033[92m[SUCCESS] \033[93m[ATTEMPT] \033[95m[INFO]\n\n")


def complete_daily_set(b: w):
    d = dashboard_data(b=b)['dailySetPromotions']
    todaydate, todaypack = datetime.today().strftime('%m/%d/%Y'), []
    for datedate, data in d.items():
        if datedate == todaydate:
            todaypack = data
    for activity in todaypack:
        if not activity['complete']:
            card_number: int = int(activity['offerId'][-1:])
            if activity['promotionType'] == "urlreward":
                cp(f'[INFO] Completing daily set {str(card_number)} (search)', "purple")
                daily_set_search(card_number, b)
            if activity['promotionType'] == "quiz":
                if activity['pointProgressMax'] == 50 and activity['pointProgress'] == 0:
                    cp(f'[INFO] Completing daily set {str(card_number)} (this or that)', "purple")
                    daily_set_this_or_that(card_number, b)
                elif (activity['pointProgressMax'] == 40 or activity['pointProgressMax'] == 30) and activity[
                    'pointProgress'] == 0:
                    cp(f'[INFO] Completing daily set {str(card_number)} (quiz)', "purple")
                    daily_set_quiz(card_number, b=b)
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
                        daily_set_survey(card_number, b=b)
                    else:
                        cp(f'[INFO] Completing daily set {str(card_number)} (quiz)', "purple")
                        daily_set_variable_activity(card_number, b=b)


def daily_set_search(card_number: int, b: w):
    wait(5)
    b.find_element(By.XPATH,
                   f'//*[@id="app-host"]/ui-view/mee-rewards-dashboard/main/div/mee-rewards-daily-set-section/div/mee-card-group/div/mee-card[{str(card_number)}]/div/card-content/mee-rewards-daily-set-item-content/div/a/div/span').click()
    wait(1)
    b.switch_to.window(window_name=b.window_handles[1])
    sign_in(b)
    wait(4)
    b.close()
    wait(2)
    b.switch_to.window(window_name=b.window_handles[0])
    wait(2)


def daily_set_survey(card_number: int, b: w):
    wait(5)
    b.find_element(By.XPATH, f'//*[@id="app-host"]/ui-view/mee-rewards-dashboard/main/div/mee-rewards-daily-set-section/div/mee-card-group/div/mee-card[{str(card_number)}]/div/card-content/mee-rewards-daily-set-item-content/div/a/div/span').click()
    wait(1)
    b.switch_to.window(window_name=b.window_handles[1])
    wait(8)
    sign_in(b)
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


def daily_set_quiz(card_number: int, b: w):
    wait(5)
    b.find_element(By.XPATH,
                   f'//*[@id="app-host"]/ui-view/mee-rewards-dashboard/main/div/mee-rewards-daily-set-section[1]/div/mee-card-group[1]/div[1]/mee-card[{str(card_number)}]/div[1]/card-content[1]/mee-rewards-daily-set-item-content[1]/div[1]/a[1]/div[3]/span[1]').click()
    wait(3)
    b.switch_to.window(window_name=b.window_handles[1])
    sign_in(b)
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
        b.get('https://rewards.microsoft.com/')
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


def daily_set_variable_activity(card_number: int, b: w):
    wait(2)
    b.find_element(By.XPATH, f'//*[@id="app-host"]/ui-view/mee-rewards-dashboard/main/div/mee-rewards-daily-set-section/div/mee-card-group/div/mee-card[{str(card_number)}]/div/card-content/mee-rewards-daily-set-item-content/div/a/div/span').click()
    wait(1)
    b.switch_to.window(window_name=b.window_handles[1])
    sign_in(b)
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


def daily_set_this_or_that(card_number: int, b: w):
    wait(2)
    b.find_element(By.XPATH,
                   f'//*[@id="app-host"]/ui-view/mee-rewards-dashboard/main/div/mee-rewards-daily-set-section/div/mee-card-group/div/mee-card[{str(card_number)}]/div/card-content/mee-rewards-daily-set-item-content/div/a/div/span').click()
    wait(1)
    b.switch_to.window(window_name=b.window_handles[1])
    sign_in(b)
    wait(15)
    # Accept cookie popup
    if element_exist(By.ID, 'bnp_container', b=b):
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
        b.get('https://rewards.microsoft.com/')
        return
    b.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
    WDWait(b, 10).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]')))
    wait(5)
    for question in range(10):
        # Click on later on Bing wallpaper app popup
        if element_exist(By.ID, 'b_notificationContainer_bop', b=b):
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


def wait_until_q_loads(b: w, quiz_question: Literal["quiz", "questions"] = "quiz"):
    tries = 0
    refreshcount = 0
    while True:
        try:
            if quiz_question == "quiz":
                b.find_element(By.XPATH, '//*[@id="currentQuestionContainer"]')
            elif quiz_question == "questions":
                b.find_elements(By.CLASS_NAME, 'rqECredits')[0]
            return True
        except Exception as e:
            error(e)
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


def complete_punch_card(url: str, cpromo: dict, b: w):
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


def complete_punch_cards(b: w):
    puc = dashboard_data(b)['punchCards']
    for punchCard in puc:
        if punchCard['parentPromotion'] is not None and punchCard['childPromotions'] is not None and \
                punchCard['parentPromotion']['complete'] is False and punchCard['parentPromotion'][
            'pointProgressMax'] != 0:
            url = punchCard['parentPromotion']['attributes']['destination']
            if b.current_url.startswith('https://rewards.'):
                path = url.replace('https://rewards.microsoft.com', '')
                new_url = 'https://rewards.microsoft.com/dashboard/'
                uc = path[11:15]
                dest = new_url + uc + path.split(uc)[1]
            else:
                path = url.replace('https://account.microsoft.com/rewards/dashboard/', '')
                new_url = 'https://account.microsoft.com/rewards/dashboard/'
                uc = path[:4]
                dest = new_url + uc + path.split(uc)[1]
            complete_punch_card(dest, punchCard['childPromotions'], b)
    wait(2)
    b.get('https://rewards.microsoft.com/dashboard/')
    wait(2)


def complete_more_promotion_search(card_number: int, b: w):
    b.find_element(By.XPATH,
                   f'//*[@id="app-host"]/ui-view/mee-rewards-dashboard/main/div/mee-rewards-more-activities-card/mee-card-group/div/mee-card[{str(card_number)}]/div/card-content/mee-rewards-more-activities-card-item/div/a/div/span').click()
    wait(1)
    b.switch_to.window(window_name=b.window_handles[1])
    wait(15)
    b.close()
    wait(2)
    b.switch_to.window(window_name=b.window_handles[0])
    wait(2)


def complete_more_promotion_quiz(card_number: int, b: w):
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


def complete_more_promotions_abc(card_number: int, b: w):
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


def complete_more_promotion_this_or_that(card_number: int, b: w):
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


def complete_more_promotions(b: w):
    mp = dashboard_data(b=b)['morePromotions']
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
            'promotionType'] == "" and promotion['destinationUrl'] == "https://rewards.microsoft.com":
            complete_more_promotion_search(itera, b=b)


def sign_in(b: w) -> None:
    """for those stupid times when it doesn't register you signing in"""
    if str(b.current_url).split('?')[0] == "https://www.bing.com/rewards/signin":
        # b.findElement(By.xpath("//a[@href='/docs/configuration']")).click();
        WDWait(b, 100).until(ec.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/span/a"))).click()
        cp("[INFO] Re-signed in, due to a bug in Microsoft Rewards.", "purple")
        wait(1)
    if str(b.current_url).split('?')[0] == "https://login.live.com/login.srf":
        WDWait(b, 100).until(ec.element_to_be_clickable(password)).send_keys(gd(uuid, "password"))
        WDWait(b, 100).until(ec.element_to_be_clickable(next_button)).click()


def mobile_sign_in(userid: int, b: w):
    sa = requests.get("https://www.mit.edu/~ecprice/wordlist.10000").text.splitlines()
    b.execute_script(f'window.location.href = "https://bing.com/?q={sa[randint(0, len(sa) - 1)]}";')
    wait(2)
    b.find_element(By.ID, 'mHamburger').click()  # //*[@id="mHamburger"]
    wait(1)
    logged_in_account = b.find_element(By.ID, 'hb_n').text
    if logged_in_account.lower().replace(" ", "") in gd(userid, "username"):
        return
    else:
        WDWait(b, 100).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="id_prov_cont"]'))).click()
        wait(0.5)
        WDWait(b, 100).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="hb_idproviders"]/a'))).click()
        wait(4)
        cp('[INFO] Bing did not automatically connect to your specified M$ Rewards account, it has automatically been resolved now.', "purple")


def another_stupid_sign_in(userid: int, b: w):
    sa = requests.get("https://www.mit.edu/~ecprice/wordlist.10000").text.splitlines()
    b.execute_script(f'window.location.href = "https://bing.com/?q={sa[765]}";')
    wait(2)
    logged_in_account = b.find_element(By.ID, 'id_n').text
    if logged_in_account.lower().replace(" ", "") in gd(userid, "username"):
        return
    else:
        WDWait(b, 100).until(ec.element_to_be_clickable((By.ID, 'id_n'))).click()
        wait(0.5)
        WDWait(b, 100).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="b_idProviders"]/li[1]/a/span[2]'))).click()
        wait(4)
        cp('[INFO] Bing did not automatically connect to your specified M$ Rewards account, it has automatically been resolved now.',
           "purple")


#######################
#  HOPE FOR THE BEST  #
#######################
def main(u: int = 0):
    # Mobile search - first in case something fails on desktop search
    def mobile():
        b = create_b_instance(mobile_instance=True)

        try:
            login(u, b)
        except Exception as e:
            error(e)
            try:
                login(u, b)
            except Exception as e:
                error(e)

        wait(5)

        try:
            mobile_sign_in(u, b)
        except Exception as e:
            error(e)
            try:
                mobile_sign_in(u, b)
            except Exception as e:
                error(e)

        wait(5)
        search(30, b)
        wait(20)

        try:
            logout(u, b)
        except Exception as e:
            error(e)
            try:
                logout(u, b)
            except Exception as e:
                error(e)

        wait(2)
        try:
            b.close()
        except Exception as e:
            error(e)
            try:
                b.close()
            except Exception as e:
                error(e)

        wait(5)

    # Desktop search
    def desktop():
        b = create_b_instance(mobile_instance=False)

        try:
            login(u, b)
        except Exception as e:
            error(e)
            try:
                login(u, b)
            except Exception as e:
                error(e)

        wait(5)

        try:
            another_stupid_sign_in(u, b)
        except Exception as e:
            error(e)
            another_stupid_sign_in(u, b)
            try:
                login(u, b)
            except Exception as e:
                error(e)

        wait(30)

        try:
            check_points(b, u)
        except Exception as e:
            error(e)
            try:
                check_points(b, u)
            except Exception as e:
                error(e)

        try:
            complete_daily_set(b)
        except Exception as e:
            error(e)
            try:
                complete_daily_set(b)
            except Exception as e:
                error(e)

        wait(60)

        try:
            complete_punch_cards(b)
        except Exception as e:
            error(e)
            try:
                complete_punch_cards(b)
            except Exception as e:
                error(e)

        wait(60)

        try:
            complete_more_promotions(b=b)
        except Exception as e:
            error(e)
            try:
                complete_more_promotions(b=b)
            except Exception as e:
                error(e)

        wait(60)
        search(34, b)
        wait(20)

        try:
            check_points(b, u)
        except Exception as e:
            error(e)
            try:
                check_points(b, u)
            except Exception as e:
                error(e)

        try:
            logout(u, b)
        except Exception as e:
            error(e)
            try:
                logout(u, b)
            except Exception as e:
                error(e)

        wait(2)

        try:
            b.close()
        except Exception as e:
            error(e)
            try:
                b.close()
            except Exception as e:
                error(e)
        cp(f"[SUCCESS] {gd(u)} has completed it's daily Microsoft Reward tasks.", "green")

    desktop()
    mobile()


if __name__ == '__main__':
    logo()
    for mainuserid in range(0, accounts):
        if tacos == "yes":
            main(mainuserid)
        else:
            error("You do not like tacos. Script will not run until you fix your opinion in credentials.json", finish_process=True)
