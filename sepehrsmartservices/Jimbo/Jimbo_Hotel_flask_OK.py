import os



os.system("title Jimboo Hotel Flask")

import json
from concurrent.futures import ThreadPoolExecutor, wait, as_completed
# from app_crawl.helpers import convert_to_tooman
from requests import request
import urllib3
import  requests
from Client_Dispatch_requests import executeRequest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time
import random

from threading import Thread
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# from insert_influx import Influxdb
# influx = Influxdb()
import redis
import environ
import uuid

# Initialize environment variables
env = environ.Env(
    DEBUG=(bool, False)
)

# reading .env file
environ.Env.read_env('.env')

REDIS_HOST = env('REDIS_HOST')
REDIS_PORT = env('REDIS_PORT')
REDIS_PASSWORD = env('REDIS_PASSWORD')

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=0, decode_responses=True)

BUILD_TOUR_TIMEOUT = int(env('BUILD_TOUR_TIMEOUT'))
BUILD_TOUR_REFRESH_TIMEOUT = int(env('BUILD_TOUR_REFRESH_TIMEOUT'))

Dic_mapping_destination={
            'KIH':'1640809',
            'GSM':'1640807',
            'MHD' : '1640810',
            'THR': '1641221',
            'SYZ' : '1640811',
            'IFN': '1640808',
            'AZD': '1640806',
            'TBZ' : '1640812',


            'AWZ': '1641237',
            'BND': '1642120',
            'ZBR': '1640813',
            'KER': '1641231',
            'KSH': '1641223',
            'RAS': '1641216',
            'SRY': '1641222',




            # =========
            'ABD': '1641239',
            'BUZ': '1642111',
            'GBT': '1641220',
            'OMH': '1641235',
            'ADU': '1641224',
            'HDM': '1641217',
            'RZR': '1643472',
            'KHD': '1643423',
            'NSH': '1643449',
            # ===========
        }
#===============
# create cookie priodically
# ========= With selenium ========

def create_cookie_with_selenium():
    
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.jimbo.ir/sign-in/')
    print('Signed in...', flush=True)
    try:
        driver.find_element(By.XPATH, '//input[@id="Mobile"]').clear()
        driver.find_element(By.XPATH, '//input[@id="Mobile"]').send_keys('09150028721')
    except:
        ''
    driver.find_element(By.XPATH, '//span[contains(text(),"ورود با رمز ثابت")]/..').click()
    time.sleep(4)
    driver.find_elements(By.XPATH, '//input[@placeholder="رمز عبور ثابت"]')[1].clear()
    driver.find_elements(By.XPATH, '//input[@placeholder="رمز عبور ثابت"]')[1].send_keys('Mst1231020@')

    driver.find_elements(By.XPATH, '//span[text()="ورود"]/..')[-1].click()

    cnt = 0
    max_tries = 30
    success = False
    time.sleep(4)
    while cnt < max_tries:
        if (driver.current_url == "https://www.jimbo.ir/"):
            print('In page mojalal safar...', flush=True)
            # driver.find_element(By.XPATH, '//*[@id="mainBody"]/header/div/div[1]/div/div[1]/div[1]/div/ul/li/span/span')
            # time.sleep(5)
            success = True
            print('cookie ok', flush=True)
            break
        else:
            print('wait until mojalal safar appear...', flush=True)
            time.sleep(4)
            cnt += 1
            continue
    
    if not success:
        return


    cookies_dict = driver.get_cookies()
    # Save cookies to a JSON file
    with open("Jimboo_hotel_cookies.json", "w") as file:
        json.dump(cookies_dict, file)
    driver.quit()
    return cookies_dict

#== for first time ===
if os.path.exists('Jimboo_hotel_cookies.json'):
    ''
else:  # file nist
    create_cookie_with_selenium()
#=================




# Function to create cookies.json every 6 hours
def create_cookies_periodically():
    while True:
        create_cookie_with_selenium()

        # Wait for 6 hours (6 hours * 60 minutes * 60 seconds)
        time.sleep(6 * 60 * 60)


# Start the background thread for cookie deletion
cookie_creation_thread = Thread(target=create_cookies_periodically)
cookie_creation_thread.daemon = True  # Daemonize thread to exit when the main program exits
cookie_creation_thread.start()

#===================

def load_cookies():
    if os.path.exists('Jimboo_hotel_cookies.json'):
        with open('Jimboo_hotel_cookies.json', 'r') as json_file:
            return json.load(json_file)
    else:
        print(' Jimboo_hotel_cookies.json not exists !!!!!! ')
        # return renew_and_save_cookies()


session_IDs = {}

def get_session_id(target):
    start_date = datetime.today() + timedelta(days=7)
    start_date = start_date.strftime("%Y-%m-%d")

    end_date = datetime.today() + timedelta(days=10)
    end_date = end_date.strftime("%Y-%m-%d")

    cookies_dict = load_cookies()
    # cookies_string = '; '.join([f'{name}={value}' for name, value in cookies_dict.items()])
    cookies_string = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies_dict])
    headers = {
        'Content-Type': 'application/json',
        'origin': 'https://www.jimbo.ir',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }
    headers['Cookie']= cookies_string

    url = f"https://www.jimbo.ir/fa/hotel/iran/{target.lower()}/?i={start_date}&o={end_date}&r=1;&n=ir&d={Dic_mapping_destination[target]}&lt=1&dt=2&a=2&c=0#/"
    
    # # Set up Chrome options
    # chrome_options = Options()
    # chrome_options.add_argument("--headless=new")
    # chrome_options.add_argument("--window-size=1920,1080")
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    # chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) " +
    #                 "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

    # driver = webdriver.Chrome(options=chrome_options)
    # driver.get(url)

    # # Wait until the page is fully loaded
    # WebDriverWait(driver, 5).until(
    #     lambda d: d.execute_script("return document.readyState") == "complete"
    # )

    # response = driver.page_source
    # driver.quit()

    res = executeRequest(method='get', url=url, headers=headers, priorityTimestamp=1,
                              use_cache=False, forceGet=1)
    response = json.loads(res)['text']

    # print("response:", response)

    static_session_id = extract_session_id(response).split(',')[0]

    search_url = f"https://www.jimbo.ir/v3/hotelbooking/search/"

    body = {
        "isStaticPage": False,
        "checkIn": f"{start_date}T00:00:00",
        "checkOut": f"{end_date}T00:00:00",
        "systemType": None,
        "room": 1,
        "nationality": "IR",
        "sessionId": static_session_id,
        'highLightedHotels':[],
        "destinations": {
            "id": Dic_mapping_destination[target]
        },
        "occupancies": [
            {
                "adult": 2,
                "childs": 0,
                "ages": []
            }
        ]
    }

    session_IDs[target] = static_session_id

    try:
        # res = requests.post(search_url, json=body, headers=headers, timeout=120)
        res = executeRequest(method='post', url=search_url, headers=headers, priorityTimestamp=1,
                              json_data=body, use_cache=False, forceGet=1)
        print(f"Searching hotels of '{target}' was successful", flush=True)
        return True
    except Exception as e:
        print(f"Error while searching hotels of '{target}': {e}", flush=True)
        return False

def get_session_ids():
    # Using ThreadPoolExecutor with max 3 workers.
    executor = ThreadPoolExecutor(max_workers=3)
    try:
        # Dictionary to hold future-to-target mapping
        future_to_target = {
            executor.submit(get_session_id, target): target
            for target in Dic_mapping_destination.keys()
        }
        
        # Optionally handle results as they are completed.
        for future in as_completed(future_to_target):
            target = future_to_target[future]
            try:
                result = future.result()
                print(f"Task for '{target}' completed successfully, result: {result}", flush=True)
            except Exception as exc:
                print(f"Task for '{target}' raised an exception: {exc}", flush=True)
    finally:
        executor.shutdown(wait=False)
        del executor

# Function to get session IDs of all destinations every 13.5 minutes
def get_session_ids_periodically():
    while True:
        start_cycle = time.time()
        print(f"Starting new cycle of getting session IDs.", flush=True)

        get_session_ids()

        # Calculate elapsed time and sleep for remainder of 13.5 min period (810 seconds)
        elapsed = time.time() - start_cycle
        sleep_time = max(0, 810 - elapsed)
        print(f"Cycle completed in {elapsed:.2f} seconds, sleeping for {sleep_time:.2f} seconds.", flush=True)
        time.sleep(sleep_time)


# Start the background thread for cookie deletion
get_session_ids_thread = Thread(target=get_session_ids_periodically)
get_session_ids_thread.daemon = True  # Daemonize thread to exit when the main program exits
get_session_ids_thread.start()

def convert_to_tooman(price) -> int:
    """
    convert rial price to tooman
    :param price: rial price
    :return: tooman price
    """
    return int(float(price) / 10)


def ready_price(price: str) -> str:
    """
    delete price noise
    :param price: str
    :return: price without noise
    """
    price = price.replace(',', '')
    price = price.replace('ريال', '')
    return convert_persian_number_to_english(price.strip())

def convert_persian_number_to_english(number: str):
    """
    check string if it has persian number, change it to english number
    :param number: any string
    :return:
    """
    numbers = {
        "۱": "1",
        "۲": "2",
        "۳": "3",
        "۴": "4",
        "۵": "5",
        "۶": "6",
        "۷": "7",
        "۸": "8",
        "۹": "9",
        "۰": "0",
    }
    # ---
    result = [
        numbers[num] if num in list(numbers.keys()) else num for num in number
    ]
    # --- response
    return "".join(result)

#
# def get_authorization():
#     print(f'-----Jimbo Authotization -----')
#     headers = {
#         'accept': '*/*',
#         'accept-language': 'en-US,en;q=0.9',
#         'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
#         # 'cookie': 'analytics_campaign={%22source%22:%22google%22%2C%22medium%22:%22organic%22}; analytics_token=22ffd8a1-e581-be11-efe1-43157fd04a08; SERVERID=fanavaweb3; _yngt_iframe=1; _yngt=4ada5a09-9baf9-95841-17f60-061524e7f4766; __RequestVerificationToken=eL5-NSSEy-Y7wsshrCV-Nsuii8fFBwElkwFha527YS7ZtleRU0K-NGgBh3-qw2scrJWcAKwZBlZTiN0g6GLWWF1Gqqa0wTkwkVmxWcvt3t41; analytics_session_token=76f4fa94-1961-f7df-3e1c-27997364cf77; yektanet_session_last_activity=8/9/2024; _gid=GA1.2.703081956.1723190029; Authentication=13jVmKckM0NT0eI3jcq3mTIwaVU_Hb87ZV3LNPOvGBtV8c5vHn4SlqlbpmolUCHfYQ99n4NzDZX88J22cCeXFSLX3HWRi1LqBwZ8WMjpzYT5CWUXxVHsQ5fGpVecaPH2c8ONr4kFeqBZLSscscr8h6RlAxG8qvlf3EoXEYW0CSqdldlYl7ti43LQbcQwPBsTwQF7Ehd5hQGzGNbCMVjOXRxsMj0Z5kdhijdW0BsM9iBL8Esfe7tCgobeNoLi7O_SlE-iCkZXJfcKAGM72f2YKK9b-lANv7CdhmQWbBq3eF4KPvI4c-he9kyfI9nEewEqioXKQ-kKJBFRJFGfmppH1_aLMowINAVfP0upf8RkbkkbYn7E6XzEPdkmmFxmfy052poag5-48lBb0rsI18P0tQUT9a-GinT1OtvG1jcVhZvK-IIlyZLzFxP9Ecv5bGwp0eEPExYtoxRyn7xHh28MM4908cbVmc9D3dZW7JufQ0L6E8Unjo6hZxc_2rnpqKX8YPYnrckJ1__v2TK2hJCBjBDqYUjxDJAttkbZlmmq39lTJMxXqiI-MYtsnb0hXqI0huKBgdGr_fuF0vc2TgBFq2gwdd8xFT2OfZVM68W_PORW7yNNPeMscrpbSI49RLMvNWmzTKNsIQx8UlXwBUKCxTUPXwnxk06aLqpBGdRq5em3jIfwb4n9kRcE2Jghl1I-wx68EOV5-oGeVG7VLGETf8fX9nNp1qBSclYx1ZppeCrR2wWR92_qpVe6T4JbzmMwrYdmWKoDGvsXZhqC3asRs2vu2veWZFP8IOlxR6BeTrxcmTVq2B65Z3rwliFGTBrMGBawyMuhoYA_eBNlO0dZuC-0XNKg-HHMTTdDXmQc2bpVfhiP31gTOau2e6KLkm3Zf1Y_uJgKKgCmJU1HDL92VuIUkUmz9pHuCv6eMNiJW2v0gLD_NaRS0NHP6CuwOJxgzYetcgIbZaQTg0v-lfkbmA; _dc_gtm_UA-174237991-1=1; _ga=GA1.2.191314830.1719310326; _ga_N9ZBHQ0R9X=GS1.1.1723189964.3.1.1723190107.45.0.0',
#         'origin': 'https://www.jimbo.ir',
#         'priority': 'u=1, i',
#         'referer': 'https://www.jimbo.ir/sign-in/',
#         'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
#         'sec-ch-ua-mobile': '?0',
#         'sec-ch-ua-platform': '"Windows"',
#         'sec-fetch-dest': 'empty',
#         'sec-fetch-mode': 'cors',
#         'sec-fetch-site': 'same-origin',
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
#         'x-requested-with': 'XMLHttpRequest',
#     }
#
#     data = {
#         'mobile': '09153148721',
#         'password': '@MST8451030yf',
#         'countryCode': 'IR',
#         'g-recaptcha-response':'03AFcWeA7MtvAispnmY6sIcjIwpxRDN2H5yw3kmtaObON4gwgFXT33l8IiGZYjyJPXvweoyJXQXKYtiGs6yMnxMiER_9LVY5l4nVi9lnQ2AL-ceng5uBiii3SFe4gHbpY9DqMyg5odbRPjo8jwKNOFbWSoA8Xncp5ATZ7ODcKQU2jlfO59GfgGPf3BsWqLB9GD4psVeMIu8yVAQhWC03o09duF8_zBSHAMoHmmcQkUS9YSfEAknI5oRBeGeICEoRSYXzQgUP3kdwhSxJpL6Aendwlp1lydG6BHQnK_5RVhAd6w76tBJxYtGMOQknXN3DhnYgMEcadAIx2J7d57kpk9iPhkLYOXNzfKMUFVNmcHwpI-vJ01_MkSUeDbYRe0W7dA5MQ9e-tOxrgNQph_WpBZiRmQpOLbRM4gA97-OPVhSJ0azK4y505_dWpeMLfkoUMcRdRJVE9o78pzgi-oNmJfMHxyfcfUvHfSE6_lZl5zM7_N16s_0wQsMh_k_SOTNGW4KzSGFFxr_PL2A57DdJ9WAZeB9faf-Vd_CWHG91jqvf2tJZddSXD5S-aKInQx51qvx8_yBWgMIpLxTJGtgildYNEVkybTKxNHfNJDpeiFb8WP4aUKRc6l-Pt-IPkRAyqy0JPF6Iu7FkfZ5347-wl8vMqCXXXi9aPeca_ZTeE7bU9-FGl-TOClxJAJFka7J7a3CxHtPtlQTtJBcwjqwmmd8EskttNZRxZiwBuVfcwDND9xV_1koyG02lDuuGVkGFwiZ5veOEAC_klK-HY9iJHSOTuTcTeaW-H9gUBdmfEVcuzaEuayVxNy-YkUH8wNwfVXsWYqG0wcerxMdCHuezvjwJD99Wf90nNGsg'
#     }
#
#     # req = requests.post('https://www.jimbo.ir/fa/v2/signinbymobile/', headers=headers, data=data)
#     req = executeRequest(method='post',url='https://www.jimbo.ir/fa/v2/signinbymobile/', headers=headers, data=data)
#     req = req.json()
#
#     influx.capture_logs(1, 'Jimboo')
#
#
#     cookies = [f"{key}={value}" for key, value in req['cookies'].items()]
#
#     headers['Cookie'] = '; '.join(cookies)
#
#     # req = requests.get( "https://www.jimbo.ir/account/getcompanies/", headers=headers)
#     req = executeRequest(method='get',url='https://www.jimbo.ir/account/getcompanies/', headers=headers)
#     req = req.json()
#
#     influx.capture_logs(1, 'Jimboo')
#
#
#     data = json.loads(req['text'])
#
#     company_id = data['model'][0]['id']
#
#     data = F"id={company_id}"
#
#     # req = requests.post("https://www.jimbo.ir/account/signinbycompany/", headers=headers, data=data)
#     req = executeRequest(method='post',url='https://www.jimbo.ir/account/signinbycompany/', headers=headers,data=data)
#     req = req.json()
#
#     influx.capture_logs(1, 'Jimboo')
#     return req['cookies']

#
# def renew_and_save_cookies():
#     #========= With selenium ========
#     driver = webdriver.Chrome()
#     driver.get('https://www.jimbo.ir/sign-in/')
#     print('Signed in...')
#     try:
#         driver.find_element(By.XPATH, '//input[@id="Mobile"]').clear()
#         driver.find_element(By.XPATH, '//input[@id="Mobile"]').send_keys('09153148721')
#     except:
#         ''
#     driver.find_element(By.XPATH, '//span[contains(text(),"ورود با رمز ثابت")]/..').click()
#     time.sleep(1)
#     driver.find_elements(By.XPATH, '//input[@placeholder="رمز عبور ثابت"]')[1].clear()
#     driver.find_elements(By.XPATH, '//input[@placeholder="رمز عبور ثابت"]')[1].send_keys('@MST8451030yf')
#
#     driver.find_elements(By.XPATH, '//span[text()="ورود"]/..')[-1].click()
#
#     time.sleep(1)
#     while(True):
#         if (driver.current_url == "https://www.jimbo.ir/account/companies/?returnUrl=/"):
#             print('In page mojalal safar...')
#             driver.find_element(By.XPATH, '//button[contains(text(),"مجلل سفر طلایی")]').click()
#             time.sleep(5)
#             print('cookie ok')
#             break
#         else:
#             print('wait until mojalal safar appear...')
#             time.sleep(1)
#             continue
#
#
#
#     cookies_dict = driver.get_cookies()
#     # Save cookies to a JSON file
#     with open("Jimboo_hotel_cookies.json", "w") as file:
#         json.dump(cookies_dict, file)
#     driver.quit()
#     return cookies_dict
#
#     #============ OLD code with requests ===========
#     # cookies = get_authorization()
#     # cookies_dict = {cookie.name: cookie.value for cookie in cookies}
#     # with open('Jimboo_hotel_cookies.json', 'w') as json_file:
#     #     json.dump(cookies_dict, json_file)
#     # return cookies_dict

def extract_session_id(response_text):
    return response_text.split('sessionId')[1].split(',"basic"')[0].replace(':', '').replace('"', '')



from datetime import datetime,timedelta
class Jimbo:
    def __init__(self, target, start_date, end_date, adults,isAnalysiss,hotelstarAnalysis=[],priorityTimestamp=1,use_cache=True,forInfo=0, is_refresh=False):
        self.target = target
        self.start_date = start_date
        self.end_date = end_date
        self.adults = adults
        # self.isAnalysis=isAnalysis


        self.isAnalysis=isAnalysiss[0] if isAnalysiss is tuple else isAnalysiss ,
        self.isAnalysis = self.isAnalysis[0] if isinstance(self.isAnalysis, tuple) else self.isAnalysis

        self.hotelstarAnalysis=hotelstarAnalysis
        self.priorityTimestamp=priorityTimestamp
        self.use_cache = use_cache
        self.is_refresh = is_refresh


        self.executor = ThreadPoolExecutor(max_workers=200)
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.static_session_id=''
        self.cookies = []
        self.mapping_destination={
            'KIH':'1640809',
            'GSM':'1640807',
            'MHD' : '1640810',
            'THR': '1641221',
            'SYZ' : '1640811',
            'IFN': '1640808',
            'AZD': '1640806',
            'TBZ' : '1640812',


            'AWZ': '1641237',
            'BND': '1642120',
            'ZBR': '1640813',
            'KER': '1641231',
            'KSH': '1641223',
            'RAS': '1641216',
            'SRY': '1641222',




            # =========
            'ABD': '1641239',
            'BUZ': '1642111',
            'GBT': '1641220',
            'OMH': '1641235',
            'ADU': '1641224',
            'HDM': '1641217',
            'RZR': '1643472',
            'KHD': '1643423',
            'NSH': '1643449',
            # ===========
        }
        self.url = f"https://www.jimbo.ir/fa/hotel/iran/{target.lower()}/?i={self.start_date}&o={self.end_date}&r=1;&n=ir&d={self.mapping_destination[self.target]}&lt=1&dt=2&a=2&c=0#/"
        #---- Load cookies
        self.cookies_dict = load_cookies()


        if (forInfo==0):
            #---- Load hotels info from Json
            with open(f'Jimboo_hotels/Jimboo_hotel_info_{self.target}.json','r') as f:
                a=f.read()
                self.hotels=json.loads(a)

        #--- Load SessionID
        self.get_sessionID()
    def get_sessionID(self):
        force = 1
        sess=requests.session()

        # cookies_string = '; '.join([f'{name}={value}' for name, value in cookies_dict.items()])
        cookies_string = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in self.cookies_dict])

        self.headers['Cookie']= cookies_string

        # while True:

        #     #---------------
        #     # try:
        #     #     req = sess.get(self.url, headers=self.headers)
        #     # except:
        #     #     time.sleep(1)
        #     #     continue
        #     #
        #     # self.static_session_id = extract_session_id(req.text).split(',')[0]

        #     # #=--------- new Approach ----
        #     # sessionID_kol=extract_session_id(req.text).split(',')[0]
        #     # for htl in self.hotels:
        #     #     url_htl=f'https://www.jimbo.ir/fa/hotel/iran/
        #     #     %DA%A9%DB%8C%D8%B4/%D9%87%D8%AA%D9%84-%D9%BE%D8%A7%D9%86%DB%8C%D8%B0-%DA%A9%DB%8C%D8%B4/
        #     #     ?i=2025-04-07&o=2025-04-10&r=1&n=ir&d=2115449&a=2&c=0&
        #     #     si=73c52868921946369c4e9458cc278397#    # sessionID_kol
        #     #     /shouldSelectPackage'
        #     # #----------------

        #     url = f'https://www.jimbo.ir/v3/hotelbooking/search/'

        #     body = {
        #         "isStaticPage": False,
        #         "checkIn": f"{self.start_date}T00:00:00",
        #         "checkOut": f"{self.end_date}T00:00:00",
        #         "systemType": None,
        #         "room": 1,
        #         "nationality": "IR",
        #         "sessionId": self.static_session_id,
        #         # "sessionId": "c96f2b5a164f415e8f27fd3a6cdd3cc9",
        #         "destinations": {
        #             "id": "1641375"
        #         },
        #         "occupancies": [
        #             {
        #                 "adult": self.adults,
        #                 "childs": 0,
        #                 "ages": []
        #             }
        #         ]
        #     }
        #     # req = sess.post(url, json=body, headers=self.headers)
        #     #
        #     # self.static_session_id = extract_session_id(req.text).split(',')[0]


        #     #----------

        #     # self.static_session_id = extract_session_id(req.text).split(',')[0]
        #     # break
        #     #-------------
        # #
        #     req = executeRequest(method='get', url=self.url, headers=self.headers,
        #                          priorityTimestamp=self.priorityTimestamp,
        #                          use_cache=self.use_cache,forceGet=force
        #     )
        #     # req = req.json()
        #     req = json.loads(req)


        #     # influx.capture_logs(1, 'Jimboo')
        #     if req['status_code'] != 200:
        #         print(f'Jimbo Error cookie --- Status_Code: {req["status_code"]}')
        #         force = 1
        #         # cookies_dict = renew_and_save_cookies()  # Renew cookies
        #     else:
        #         break
        
        # # Set up Chrome options
        # chrome_options = Options()
        # chrome_options.add_argument("--headless=new")
        # chrome_options.add_argument("--window-size=1920,1080")
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--disable-dev-shm-usage")
        # chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        # chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) " +
        #                 "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

        # driver = webdriver.Chrome(options=chrome_options)
        # driver.get(self.url)

        # # Wait until the page is fully loaded
        # WebDriverWait(driver, 5).until(
        #     lambda d: d.execute_script("return document.readyState") == "complete"
        # )
        # # time.sleep(35)
        # # https://www.jimbo.ir/fa/hotel/iran/%DA%A9%DB%8C%D8%B4/%D9%87%D8%AA%D9%84-%D9%84%D9%8A%D9%84%D9%8A%D9%88%D9%85?i=2025-05-25&o=2025-05-26&r=1&n=ir&d=1641375&a=2&c=0&si=bca6182ff6634067a342c5929ebef3f0
        # # bca6182ff6634067a342c5929ebef3f0

        # response = driver.page_source

        # print("response:", response)

        # self.static_session_id = extract_session_id(response).split(',')[0]
        self.static_session_id = session_IDs[self.target]

        # url = f"https://www.jimbo.ir/v3/hotelbooking/search/"

        # body = {
        #     "isStaticPage": False,
        #     "checkIn": f"{self.start_date}T00:00:00",
        #     "checkOut": f"{self.end_date}T00:00:00",
        #     "systemType": None,
        #     "room": 1,
        #     "nationality": "IR",
        #     "sessionId": self.static_session_id,
        #     'highLightedHotels':[],
        #     "destinations": {
        #         "id": self.mapping_destination[self.target]
        #     },
        #     "occupancies": [
        #         {
        #             "adult": self.adults,
        #             "childs": 0,
        #             "ages": []
        #         }
        #     ]
        # }

        # try:
        #     res = requests.post(url, json=body, headers=self.headers, timeout=42)
        # except Exception as e:
        #     print(f"Error while searching hotel: {e}")

    def generate_random_session_id(self):
        # uuid4() generates a random UUID.
        # The 'hex' attribute returns the UUID as a 32-character hexadecimal string (without dashes).
        return uuid.uuid4().hex

    def get_hotels_info_writeJson(self):
        #_-- for all destination
        url = f"https://www.jimbo.ir/v3/hotelbooking/search/"

        body = {
            "isStaticPage": False,
            "checkIn": f"{self.start_date}T00:00:00",
            "checkOut": f"{self.end_date}T00:00:00",
            "systemType": None,
            "room": 1,
            "nationality": "IR",
            "sessionId": self.static_session_id,
            'highLightedHotels':[],
            "destinations": {
                "id": self.mapping_destination[self.target]
            },
            "occupancies": [
                {
                    "adult": self.adults,
                    "childs": 0,
                    "ages": []
                }
            ]
        }

        req = requests.post(url, json=body, headers=self.headers)
        # req = executeRequest(method='post', url=url,json_data=body, headers=self.headers,
        #                      priorityTimestamp=self.priorityTimestamp)
        # # req = req.json()
        # req=json.loads(req)


        # influx.capture_logs(1, 'Jimboo')
        if req.status_code != 200:
            self.get_hotels_info_writeJson()

        #--------- parse ---

        req_json=json.loads(req.text)
        hotels = req_json['model']['hotelBookingItineraries']
        lst_hotel_info=[]
        for htl in hotels:
            htl_info={}
            htl_info['star']=str(int(htl['hotel']['rating']))
            htl_info['hotel_name']=htl['hotel']['title']
            htl_info["min_price"]=0
            htl_info["provider"]="Jimboo"
            htl_info["rooms"]=[]
            htl_info['hotelId']=htl['hotelId']
            lst_hotel_info.append(htl_info)

        if not os.path.exists('Jimboo_hotels'):
            os.makedirs('Jimboo_hotels')  # Creates the folder

        json.dump(lst_hotel_info,open(f'Jimboo_hotels/Jimboo_hotel_info_{self.target}.json','w'))
        return ''

        # return json.loads(req['text'])

    def get_room_data(self, data):

        sleep_time = random.uniform(0, 8)
        print(f"Sleeping for {sleep_time:.2f} seconds to avoid sending concurrent requests to Jimbo")
        time.sleep(sleep_time)

        url = f'https://www.jimbo.ir/v3/hotelbooking/search/'

        # session_id = self.generate_random_session_id()
        # print("data['hotelId']:", data['hotelId'])
        # print("session_id:", session_id)
        print("self.static_session_id:", self.static_session_id)

        body = {
            "isStaticPage": False,
            "checkIn": f"{self.start_date}T00:00:00",
            "checkOut": f"{self.end_date}T00:00:00",
            "systemType": None,
            "room": 1,
            "nationality": "IR",
            # "sessionId": self.generate_random_session_id(),
            "sessionId": self.static_session_id,
            # "sessionId": "7bf68ee7353347bba9f688dd9c63167a",
            "destinations": {
                "id": data['hotelId']
            },
            "occupancies": [
                {
                    "adult": self.adults,
                    "childs": 0,
                    "ages": []
                }
            ]
        }

        force_fetch = 0
        if self.is_refresh:
            force_fetch = 1
        # req = requests.post(url, json=body, headers=self.headers)
        req = executeRequest(method='post', url=url,json_data=body, headers=self.headers,
                             priorityTimestamp=self.priorityTimestamp,
                             use_cache=self.use_cache, forceGet=force_fetch)
        # req = req.json()
        req = json.loads(req)


        # influx.capture_logs(1, 'Jimboo')

        try:
            if req['status_code'] == 200:
                data = json.loads(req['text'])
                return [
                    {
                        "price": convert_to_tooman(room['totalPrice']),
                        "name": room['rooms'][0]['roomTypeTitle'],
                        'capacity':room['rooms'][0]['adultCount'],
                        "provider": "Jimboo",
                        "buy_link": "https://jimbo.ir/"
                    }
                    for room in data['model']['hotelBookingItineraries'][0]['packages']
                    # if room.get('nonRefundable') is not None
                ]

            else:
                print("req['status_code']:", req['status_code'])
                return None
        except Exception as e:
            print(f"Error fetching room data for '{data['hotel_name']}': {e}")
            return None

    def get_result(self):
        result = []

        def hotel_handler(hotel):
            result.append({
                "hotel_name": hotel['hotel_name'],
                "hotel_star": hotel['star'],
                "min_price": 0,
                "provider":"Jimboo",
                "rooms": self.get_room_data(hotel)
            })



        Selecthotels=[]
        #======== Check for hotel names or star ratings
        if self.isAnalysis!='0':
            # Create a set of all hotel names for faster lookup
            all_hotel_names = {hotel['hotel_name'] for hotel in self.hotels}
            selected_hotels = set()  # Using set to avoid duplicates

            # Check Redis for hotel name mappings
            for hotel_star in self.hotelstarAnalysis:
                redis_key = f"asli_hotel:{hotel_star}"
                redis_data = redis_client.get(redis_key)
                if redis_data:
                    mapped_hotels = json.loads(redis_data)
                    # Add hotels that exist in our current hotels list
                    selected_hotels.update(hotel for hotel in mapped_hotels if hotel in all_hotel_names)

            if selected_hotels:
                # If we found mapped hotels, filter the hotels list
                Selecthotels = [hotel for hotel in self.hotels if hotel['hotel_name'] in selected_hotels]
            else:
                # Fallback to original star rating and name check
                Selecthotels = [hotel for hotel in self.hotels
                         if (str(hotel['star']) in self.hotelstarAnalysis)
                         or (hotel['hotel_name'] in self.hotelstarAnalysis)]

            print(f'Jimboo Analysis')
        else:
            print(f'Jimboo RASII')

        #============



        # #---------- Check for 5-Star hotels
        # if self.isAnalysis=='1':
        #     hotels=[htl for htl in self.hotels if str(int(htl['star'])) in self.hotelstarAnalysis]
        #     print('Jimboo Analysis')
        # else:
        #     print('Jimboo RASII')
        #
        # #-------------------

        # for hotel in self.hotels:
        #     hotel_handler(hotel)

        if len(Selecthotels)!=0:
            future = [self.executor.submit(hotel_handler, hotel) for hotel in Selecthotels]
        else:
            future = [self.executor.submit(hotel_handler, hotel) for hotel in self.hotels]


        # # self.executor.map(hotel_handler, hotels)
        # future = [self.executor.submit(hotel_handler, hotel) for hotel in self.hotels]

        # wait(future)
        # results = [f.result() for f in future]  # This will wait and get results

        try:
            completed, pending = wait(future, timeout=BUILD_TOUR_TIMEOUT)
            print("\n\n")
            print("number of completed tasks:", len(completed))
            print("number of uncompleted tasks:", len(pending))
            print("\n\n")
        finally:
            self.executor.shutdown(wait=False)

        return result

# #===========calling========
# book=Booking('KIH', '2024-08-24', '2024-08-27', '2')
# book.get_result()
# print('finish')
# # result = get_booking_tours("2024-08-15", 3)



#=== for first time = (create hotel info )
 # with open(f'Jimboo_hotel_info_{self.target}.json','r') as f:
lst_targets=list(Dic_mapping_destination.keys())
start_date = datetime.today() + timedelta(days=4)
start_date = start_date.strftime("%Y-%m-%d")

end_date = datetime.today() + timedelta(days=7)
end_date = end_date.strftime("%Y-%m-%d")

isAnalysiss=False
adults='2'
import concurrent.futures
for tg in lst_targets:
    if os.path.exists(f'Jimboo_hotels/Jimboo_hotel_info_{tg}.json'):
        ''
    else:
    #     with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    #         futures = [executor.submit(process_target, tg, start_date, end_date, adults, isAnalysiss) for tg in
    #                    lst_targets]
    #         concurrent.futures.wait(futures)  # Ensures all threads complete

        ins = Jimbo(tg, start_date, end_date, adults, isAnalysiss, hotelstarAnalysis=[],forInfo=1)


        ins.get_hotels_info_writeJson()
        print(f'Jimboo_hotels/Jimboo_hotel_info_{tg}.json  is created!')

#=================



#===== CALLING ==============

from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor
import json

app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=100)

@app.route('/Jimbo_hotels', methods=['GET'])
def Jimboo_hotels():
    global BUILD_TOUR_TIMEOUT, BUILD_TOUR_REFRESH_TIMEOUT

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    adults=request.args.get('adults')
    destination=request.args.get('target')
    isAnalysis=request.args.get('isAnalysis')

    hotelstarAnalysis=request.args.get('hotelstarAnalysis')
    hotelstarAnalysis=json.loads(hotelstarAnalysis)
    priorityTimestamp = request.args.get('priorityTimestamp')
    use_cache=request.args.get('use_cache')
    is_refresh_str = request.args.get('is_refresh', 'false')
    is_refresh = False

    if str(is_refresh_str).lower() == 'true':
        BUILD_TOUR_TIMEOUT = BUILD_TOUR_REFRESH_TIMEOUT
        is_refresh = True


    if not start_date or not end_date:
        return jsonify({"error": "Missing start_date or end_date"}), 400

    book = Jimbo(destination, start_date, end_date, adults,isAnalysis,hotelstarAnalysis,priorityTimestamp,use_cache, 0, is_refresh)
    future = executor.submit(book.get_result,)
    result = future.result()
    # Optionally, you can return a response immediately
    return jsonify(result)


import sys
if __name__ == '__main__':
    # port=int(sys.argv[1]) # Get port from command line
    # app.run(debug=True,host='0.0.0.0',port=6060)
    app.run(debug=True, host='0.0.0.0', port=3030)
    # app.run(host='0.0.0.0',port=5020)
    # app.run(host='0.0.0.0',port=port)



# result = get_booking_tours("2024-08-15", 3)


