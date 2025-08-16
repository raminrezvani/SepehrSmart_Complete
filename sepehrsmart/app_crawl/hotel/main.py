from .Crawl_Alaedin_ALL_OK import Alaedin
# from .Crawl_trivago_Selenium_OK import Trivago
from .Crawl_Snapp_api_OK import Snapp
from .DNS_utls import DNS_mapping
# from .Hotel_flytoday import FlyToday
from .booking import Booking
# from .alwin import Alwin24
from .alwin_calling_OK import Alwin
from .jimbo import Jimbo
from .moghim24 import Moghim24
from .eghamat24 import Eghamat24
from app_crawl.helpers import (add_dict_to_redis, get_dict_to_redis, check_redis_key, ready_sepehr_gsm_hotel_name,
                               ready_sepehr_hotel_name)
from app_crawl.gsm.data import hotels_GSM
from concurrent.futures import ThreadPoolExecutor
from app_crawl.cookie.cookie_data import (RAHBAL, HRC, DAYAN, OMID_OJ, SEPID_PARVAZ, PARMIS, HAMSAFAR, MEHRAB,
                                          TAK_SETAREH, IMAN, FLAMINGO, SHAYAN_GASHT, DOLFIN, YEGANE_FARD,ERAM2MHD,TOURISTKISH,SAFIRAN,HAMOOD,MOEINDARBARI,DARVISHI, IMAN_AMIN_ZIBA_GSM)
from app_crawl.kih.data import hotels
from concurrent.futures import ThreadPoolExecutor, as_completed
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, wait
# from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from django.conf import settings
import requests
import json
import traceback
import time
# executorHotel=ThreadPoolExecutor(max_workers=100)
import logging
import redis
import asyncio

from hotel_providers_api.settings import list_process_threads

REDIS_HOST=settings.REDIS_HOST
REDIS_PORT=settings.REDIS_PORT
REDIS_PASSWORD=settings.REDIS_PASSWORD

# logger = logging.getLogger('django')
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=0)

SEPEHR_SERVICE_URL = f"{settings.PROVIDER_SERVICES['SEPEHR']['BASE_URL']}{settings.PROVIDER_SERVICES['SEPEHR']['ENDPOINTS']['HOTEL_SEARCH']}"
DELTABAN_SERVICE_URL = f"{settings.PROVIDER_SERVICES['DELTABAN']['BASE_URL']}{settings.PROVIDER_SERVICES['DELTABAN']['ENDPOINTS']['HOTEL_SEARCH']}"

BUILD_TOUR_TIMEOUT = int(settings.BUILD_TOUR_TIMEOUT)
BUILD_TOUR_REFRESH_TIMEOUT = int(settings.BUILD_TOUR_REFRESH_TIMEOUT)

_loop = asyncio.new_event_loop()
asyncio.set_event_loop(_loop)

class Hotel:
    def __init__(self, source, target, start_date, end_date, adults,use_cache, provider, isAnalysiss=False,
                 hotelstarAnalysis=[],priorityTimestamp=1):
        self.source = source
        self.target = target
        self.start_date = start_date
        self.end_date = end_date
        self.adults = adults
        self.redis_expire = 10*60  # 3 minutes
        self.use_cache=use_cache
        # self.isAnalysis=isAnalysis[0] if isAnalysis is tuple else isAnalysis ,   # because isAnalysis is a tuple
        self.isAnalysis=isAnalysiss
        # self.isAnalysis = isAnalysis[0][0] if isAnalysis is tuple else isAnalysis,  # because isAnalysis is a tuple
        # self.isAnalysis = self.isAnalysis[0] if self.isAnalysis is tuple else self.isAnalysis,  # because isAnalysis is a tuple

        self.hotelstarAnalysis=hotelstarAnalysis
        self.priorityTimestamp=priorityTimestamp
        self.provider = provider



        # ---- read from redis ---
        # (RAHBAL, HRC, DAYAN, OMID_OJ, SEPID_PARVAZ, PARMIS, HAMSAFAR, MEHRAB,
        #  TAK_SETAREH, IMAN, FLAMINGO, SHAYAN_GASHT, DOLFIN, YEGANE_FARD, ERAM2MHD, TOURISTKISH, SAFIRAN, HAMOOD,
        #  MOEINDARBARI, DARVISHI)
        # ???????????????????????????????
        
        try:
            self.DARVISHI = json.loads(redis_client.get('darvishi'))
        except:
            print(f'providerCode  darvishi __ not in Redis')
            self.DARVISHI=DARVISHI

        try:
            self.MOEINDARBARI = json.loads(redis_client.get('moeindarbari'))
        except:
            print(f'providerCode  moeindarbari __ not in Redis')
            self.MOEINDARBARI = MOEINDARBARI
        
        try:
            self.IMAN_AMIN_ZIBA_GSM = json.loads(redis_client.get('iman_amin_ziba_gsm'))
        except:
            print(f'providerCode  iman_amin_ziba_gsm __ not in Redis')
            self.IMAN_AMIN_ZIBA_GSM = IMAN_AMIN_ZIBA_GSM

        try:
            self.IMAN = json.loads(redis_client.get('iman'))
        except:
            print(f'providerCode  iman __ not in Redis')
            self.IMAN=IMAN

        try:
            self.FLAMINGO = json.loads(redis_client.get('flamingo'))
        except:
            print(f'providerCode  flamingo __ not in Redis')
            self.FLAMINGO = FLAMINGO



        try:
            self.YEGANE_FARD = json.loads(redis_client.get('yegane_fard'))
        except:
            print(f'providerCode  yegane_fard __ not in Redis')
            self.YEGANE_FARD = YEGANE_FARD


        try:
            self.HAMOOD = json.loads(redis_client.get('hamood'))
        except:
            print(f'providerCode  hamood __ not in Redis')
            self.HAMOOD = HAMOOD

        try:
            self.SAFIRAN = json.loads(redis_client.get('safiran'))
        except:
            print(f'providerCode  safiran __ not in Redis')
            self.SAFIRAN = SAFIRAN

        try:
            self.DOLFIN = json.loads(redis_client.get('dolfin'))
        except:
            print(f'providerCode  dolfin __ not in Redis')
            self.DOLFIN = DOLFIN


        try:
            self.RAHBAL = json.loads(redis_client.get('rahbal'))
        except:
            print(f'providerCode  rahbal __ not in Redis')
            self.RAHBAL = RAHBAL

        try:
            self.HRC = json.loads(redis_client.get('hrc'))
        except:
            print(f'providerCode  hrc __ not in Redis')
            self.HRC = HRC

        try:
            self.DAYAN = json.loads(redis_client.get('dayan'))
        except:
            print(f'providerCode  dayan __ not in Redis')
            self.DAYAN = DAYAN
        try:
            self.OMID_OJ = json.loads(redis_client.get('omid_oj'))
        except:
            print(f'providerCode  omid_oj __ not in Redis')
            self.OMID_OJ = OMID_OJ

        try:
            self.SEPID_PARVAZ = json.loads(redis_client.get('sepid_parvaz'))
        except:
            print(f'providerCode  sepid_parvaz __ not in Redis')
            self.SEPID_PARVAZ = SEPID_PARVAZ
        try:
            self.PARMIS = json.loads(redis_client.get('parmis'))
        except:
            print(f'providerCode  parmis __ not in Redis')
            self.PARMIS = PARMIS
        try:
            self.MEHRAB = json.loads(redis_client.get('mehrab'))
        except:
            print(f'providerCode  mehrab __ not in Redis')
            self.MEHRAB = MEHRAB

        try:
            self.HAMSAFAR = json.loads(redis_client.get('hamsafar'))
        except:
            print(f'providerCode  hamsafar __ not in Redis')
            self.HAMSAFAR = HAMSAFAR

        try:
            self.TAK_SETAREH = json.loads(redis_client.get('tak_setareh'))
        except:
            print(f'providerCode  tak_setareh __ not in Redis')
            self.TAK_SETAREH = TAK_SETAREH

        try:
            self.TOURISTKISH = json.loads(redis_client.get('kimiya'))
        except:
            print(f'providerCode  kimiya __ not in Redis')
            self.TOURISTKISH = TOURISTKISH

        try:
            self.ERAM2MHD = json.loads(redis_client.get('eram2mhd'))
        except:
            print(f'providerCode  eram2mhd __ not in Redis')
            self.ERAM2MHD = ERAM2MHD


        try:
            self.SHAYAN_GASHT = json.loads(redis_client.get('shayan_gasht'))
        except:
            print(f'providerCode  shayan_gasht __ not in Redis')
            self.SHAYAN_GASHT = SHAYAN_GASHT

        # ???????????????????????????
        # ------------




    #==== Threaded version ====
    from concurrent.futures import ThreadPoolExecutor
    from collections import defaultdict

    from concurrent.futures import ThreadPoolExecutor, as_completed
    from collections import defaultdict
    import traceback

    async def _get_result_async(self, task):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, task.get_result)

    async def call_sepehr_service(self, cookie, provider_name):
        loop = asyncio.get_running_loop()
        # Run the synchronous _call_sepehr_service in a thread
        result = await loop.run_in_executor(None, self._call_sepehr_service, cookie, provider_name)
        return result
    
    # Replace the direct sepehr_get_result calls with this helper function
    def _call_sepehr_service(self, cookie, provider_name):
        try:
            payload = {
                "target": self.target,
                "start_date": self.start_date,
                "end_date": self.end_date,
                "adults": self.adults,
                "cookie": cookie,
                "provider_name": provider_name,
                "is_analysis": self.isAnalysis,
                "hotelstar_analysis": self.hotelstarAnalysis,
                "priority_timestamp": self.priorityTimestamp
            }

            response = requests.post(
                SEPEHR_SERVICE_URL,
                json=payload,
                timeout=BUILD_TOUR_TIMEOUT
            )

            if response.ok:
                result = response.json()
                if result.get('status'):
                    return result.get('data', [])
            return []
        except Exception as e:
            print(f"Error calling Sepehr service for {provider_name}: {str(e)}")
            return []

    async def call_deltaban_service(self):
        loop = asyncio.get_running_loop()
        # Run the synchronous _call_deltaban_service in a thread
        result = await loop.run_in_executor(None, self._call_deltaban_service)
        return result
    
    # Add this method to Hotel class
    def _call_deltaban_service(self):
        try:
            payload = {
                "target": self.target,
                "start_date": self.start_date,
                "end_date": self.end_date,
                "adults": self.adults,
                "is_analysis": self.isAnalysis,
                "hotelstar_analysis": self.hotelstarAnalysis,
                "priority_timestamp": self.priorityTimestamp,
                "use_cache": self.use_cache
            }

            timeout = BUILD_TOUR_TIMEOUT
            if self.provider and isinstance(self.provider, str) and self.provider.lower() == "deltaban":
                payload['is_refresh'] = True
                timeout = BUILD_TOUR_REFRESH_TIMEOUT

            response = requests.post(
                DELTABAN_SERVICE_URL,
                json=payload,
                timeout=timeout
            )

            if response.ok:
                result = response.json()
                if result.get('status'):
                    return result.get('data', [])
            return []
        except Exception as e:
            print(f"Error calling Deltaban service: {str(e)}")
            return []

    def read_data_ALLDestination(self, data):
        print('start mapping .....')
        ds = DNS_mapping(self.target)
        result = defaultdict(lambda: {"rooms": []})  # Avoid KeyErrors

        def process_hotel(hotel):
            try:

                if ('ساسان' in hotel['hotel_name']):
                    print('hotel sasan')

                hotel_name_redis_key = f"hotel_name:{hotel['hotel_name']}_{self.target}"
                hotel_name_redis = redis_client.get(hotel_name_redis_key)
                if not hotel_name_redis:

                    hotelname, hotelStar = ds.check_hotelName(hotel['hotel_name'], self.target)
                    redis_client.set(hotel_name_redis_key, json.dumps((hotelname, hotelStar)))

                    #---- for asli hotel name ----------
                    asli_hotelname=f"asli_hotel:{hotelname}"
                    res_redis_aslihotelname=redis_client.get(asli_hotelname)
                    if not res_redis_aslihotelname:
                        redis_client.set(asli_hotelname, json.dumps([hotel['hotel_name']]))
                    else:
                        existing_list = json.loads(res_redis_aslihotelname)
                        if hotel['hotel_name'] not in existing_list:  # Avoid duplicates
                            existing_list.append(hotel['hotel_name'])
                            redis_client.set(asli_hotelname, json.dumps(existing_list))
                    #-----------------------


                else:
                    hotelname, hotelStar=json.loads(hotel_name_redis)

                # hotelname, hotelStar = ds.check_hotelName(hotel['hotel_name'], self.target)
                if not hotelname:
                    return None  # Skip if no valid hotel name

                default_data = {
                    "hotel_name": hotelname,
                    "hotel_star": hotelStar,
                    "min_price": float('inf'),
                    "rooms": [],
                    "provider": hotel['provider']
                }

                hotel_name = hotelname.strip()
                hotel_rooms = []
                for room in hotel['rooms']:
                    try:
                        room['price'] = int(room['price'])
                    except:
                        room['price'] = 999999999  # Avoid JSON float error

                    hotel_rooms.append(room)

                return hotel_name, default_data, hotel_rooms
            except Exception as e:
                # print(f"Traceback details:\n{traceback.format_exc()}")

                return None

        with ThreadPoolExecutor(max_workers=40) as executor:
            futures = {executor.submit(process_hotel, hotel): hotel for hotel_list in data for hotel in hotel_list}

            for future in as_completed(futures):
                result_data = future.result()
                if result_data:
                    hotel_name, default_data, hotel_rooms = result_data
                    if hotel_name not in result:
                        result[hotel_name].update(default_data)
                    result[hotel_name]['rooms'].extend(hotel_rooms)

        # Calculate min price for each hotel
        for hotel_name, hotel_data in result.items():
            min_price = min((float(room['price']) for room in hotel_data['rooms']), default=999999999)
            hotel_data['min_price'] = min_price

        # Sort hotels by min_price
        sorted_hotels = sorted(result.items(), key=lambda x: x[1]['min_price'])
        return [hotel[1] for hotel in sorted_hotels]



    async def get_ALLDestination_data(self,iter):
        global BUILD_TOUR_TIMEOUT

        try:
            t1 = datetime.now()
            results = []

            is_refresh = False
            if self.provider and isinstance(self.provider, str) and self.provider != "":
                is_refresh = True

            hotel_tasks = {
                "deltaban": 1,
                "alwin": Alwin(self.target, self.start_date, self.end_date, self.adults,iter,self.isAnalysis,self.hotelstarAnalysis,self.priorityTimestamp,self.use_cache, is_refresh),
                "snapp" : Snapp(self.target, self.start_date, self.end_date, self.adults,self.isAnalysis,self.hotelstarAnalysis,self.priorityTimestamp,self.use_cache, is_refresh),
                "alaedin": Alaedin(self.target, self.start_date, self.end_date, self.adults,self.isAnalysis,self.hotelstarAnalysis,self.priorityTimestamp,self.use_cache),
                "eghamat": Eghamat24(self.target, self.start_date, self.end_date, self.adults,self.isAnalysis,self.hotelstarAnalysis,self.priorityTimestamp,self.use_cache, is_refresh),
                "booking": Booking(self.target, self.start_date, self.end_date, self.adults,iter,self.isAnalysis,self.hotelstarAnalysis,self.priorityTimestamp,self.use_cache, is_refresh),
                "jimboo": Jimbo(self.target, self.start_date, self.end_date, self.adults,iter,self.isAnalysis,self.hotelstarAnalysis,self.priorityTimestamp,self.use_cache, is_refresh),
                # # #
                "darvishi": 1,
                "moeindarbari": 1,
                "iman_amin_ziba_gsm": 1,
                "rahbal":1,
                "hrc": 1,
                "dayan": 1,
                "omid_oj": 1,
                "sepid_parvaz":1,
                "parmis":1,
                "mehrab": 1,
                "hamsafar":1,
                "tak_setareh":1,
                "kimiya": 1,
                "eram2mhd": 1,
                "shayan_gasht": 1,
                "iman": 1,
                "flamingo": 1,
                "yegane_fard": 1,
                "hamood": 1,
                "safiran": 1,
                "dolfin": 1
            }

            filtered_hotel_tasks = {}
            if self.provider and isinstance(self.provider, str) and self.provider != "":
                filtered_hotel_tasks = {self.provider.lower(): hotel_tasks[self.provider.lower()]} if self.provider.lower() in hotel_tasks else {}
            
            if filtered_hotel_tasks == {}:
                filtered_hotel_tasks = hotel_tasks
            else:
                BUILD_TOUR_TIMEOUT = BUILD_TOUR_REFRESH_TIMEOUT

            # print(f' time Create hotel_tasks --- {(datetime.now()-t1).total_seconds()} ')
            print(f' time Create hotel_tasks --- {(datetime.now()-t1).total_seconds()}' )
            provider_status = {}
            startTime = datetime.now()

            # Dictionary to map tasks to their keys
            task_dict = {}

            # Task creation with preserved if-else logic
            for key, task in filtered_hotel_tasks.items():
                if key == 'darvishi' and task == 1:
                    task_dict[asyncio.create_task(
                        self.call_sepehr_service(self.DARVISHI, 'darvishi')
                    )] = 'darvishi'
                elif key == 'moeindarbari' and task == 1:
                    task_dict[asyncio.create_task(
                        self.call_sepehr_service(self.MOEINDARBARI, 'moeindarbari')
                    )] = 'moeindarbari'
                elif key == 'iman_amin_ziba_gsm' and task == 1:
                    task_dict[asyncio.create_task(
                        self.call_sepehr_service(self.IMAN_AMIN_ZIBA_GSM, 'iman_amin_ziba_gsm')
                    )] = 'iman_amin_ziba_gsm'
                elif key == 'rahbal' and task == 1:
                    task_dict[asyncio.create_task(
                        self.call_sepehr_service(self.RAHBAL, 'rahbal')
                    )] = 'rahbal'
                elif key == 'hrc' and task == 1:
                    task_dict[asyncio.create_task(
                        self.call_sepehr_service(self.HRC, 'hrc')
                    )] = 'hrc'
                elif key == 'dayan' and task == 1:
                    task_dict[asyncio.create_task(
                        self.call_sepehr_service(self.DAYAN, 'dayan')
                    )] = 'dayan'
                elif key == 'omid_oj' and task == 1:
                    task_dict[asyncio.create_task(
                        self.call_sepehr_service(self.OMID_OJ, 'omid_oj')
                    )] = 'omid_oj'
                elif key == 'sepid_parvaz' and task == 1:
                    task_dict[asyncio.create_task(
                        self.call_sepehr_service(self.SEPID_PARVAZ, 'sepid_parvaz')
                    )] = 'sepid_parvaz'
                elif key == 'parmis' and task == 1:
                    task_dict[asyncio.create_task(
                        self.call_sepehr_service(self.PARMIS, 'parmis')
                    )] = 'parmis'
                elif key == 'mehrab' and task == 1:
                    task_dict[asyncio.create_task(
                        self.call_sepehr_service(self.MEHRAB, 'mehrab')
                    )] = 'mehrab'
                elif key == 'hamsafar' and task == 1:
                    task_dict[asyncio.create_task(
                        self.call_sepehr_service(self.HAMSAFAR, 'hamsafar')
                    )] = 'hamsafar'
                elif key == 'tak_setareh' and task == 1:
                    task_dict[asyncio.create_task(
                        self.call_sepehr_service(self.TAK_SETAREH, 'tak_setareh')
                    )] = 'tak_setareh'
                elif key == 'kimiya' and task == 1:
                    task_dict[asyncio.create_task(
                        self.call_sepehr_service(self.TOURISTKISH, 'kimiya')
                    )] = 'kimiya'
                elif key == 'eram2mhd' and task == 1:
                    task_dict[asyncio.create_task(
                        self.call_sepehr_service(self.ERAM2MHD, 'eram2mhd')
                    )] = 'eram2mhd'
                elif key == 'shayan_gasht' and task == 1:
                    task_dict[asyncio.create_task(
                        self.call_sepehr_service(self.SHAYAN_GASHT, 'shayan_gasht')
                    )] = 'shayan_gasht'
                elif key == 'iman' and task == 1:
                    task_dict[asyncio.create_task(
                        self.call_sepehr_service(self.IMAN, 'iman')
                    )] = 'iman'
                elif key == 'flamingo' and task == 1:
                    task_dict[asyncio.create_task(
                        self.call_sepehr_service(self.FLAMINGO, 'flamingo')
                    )] = 'flamingo'
                elif key == 'yegane_fard' and task == 1:
                    task_dict[asyncio.create_task(
                        self.call_sepehr_service(self.YEGANE_FARD, 'yegane_fard')
                    )] = 'yegane_fard'
                elif key == 'hamood' and task == 1:
                    task_dict[asyncio.create_task(
                        self.call_sepehr_service(self.HAMOOD, 'hamood')
                    )] = 'hamood'
                elif key == 'safiran' and task == 1:
                    task_dict[asyncio.create_task(
                        self.call_sepehr_service(self.SAFIRAN, 'safiran')
                    )] = 'safiran'
                elif key == 'dolfin' and task == 1:
                    task_dict[asyncio.create_task(
                        self.call_sepehr_service(self.DOLFIN, 'dolfin')
                    )] = 'dolfin'
                elif key == 'deltaban' and task == 1:
                    task_dict[asyncio.create_task(
                        self.call_deltaban_service()
                    )] = 'deltaban'
                else:
                    task_dict[asyncio.create_task(
                        self._get_result_async(task)
                    )] = key

            print(f' time Assign tasks --- {(datetime.now() - startTime).total_seconds()}')

            #---New
            result_notExistProviders=[]
            if not self.isAnalysis:
                # Wait for tasks with a 30-second timeout
                # Convert task_dict.keys() to a set for asyncio.wait compatibility
                tasks = set(task_dict.keys())
                loop = asyncio.get_event_loop()
                deadline = loop.time() + BUILD_TOUR_TIMEOUT  # 30-second timeout

                # Process tasks as they complete within the timeout
                while tasks and loop.time() < deadline:
                    timeout = deadline - loop.time()
                    if timeout <= 0:
                        break
                    
                    done, pending = await asyncio.wait(
                        tasks,
                        timeout=timeout,
                        return_when=asyncio.FIRST_COMPLETED
                    )
                    for task in done:
                        key = task_dict[task]
                        try:
                            result = task.result()  # Get result since task is done
                            if isinstance(result, dict):
                                if len(result['data']) != 0:
                                    results.append(result)
                                else:
                                    result_notExistProviders.append({
                                        'NotExistProvider': key,
                                        'data': [],
                                        'status': 'اتمام زمان'
                                    })
                            else:
                                # Assuming result is a list of dicts with 'rooms' key
                                flag_data = any(it['rooms'] and len(it['rooms']) != 0 for it in result)
                                if flag_data:
                                    results.append(result)
                                    print(f'Length hotel results of {key} --- {len(result)}')
                                else:
                                    result_notExistProviders.append({
                                        'NotExistProvider': key,
                                        'data': [],
                                        'status': 'اتمام زمان'
                                    })
                            print(f'Processed {key} --- {(datetime.now() - t1).total_seconds()}')
                        except Exception as e:
                            print(f"Error in {key}: {e}")
                    tasks = pending

                # Cancel any remaining tasks after timeout
                for task in tasks:
                    task.cancel()
                    key = task_dict[task]
                    result_notExistProviders.append({
                        'NotExistProvider': key,
                        'data': [],
                        'status': 'اتمام زمان'
                    })
                    print(f"Timeout: {key} did not complete within {BUILD_TOUR_TIMEOUT} seconds")
                
                print(f' time hotel processing completed --- {(datetime.now() - t1).total_seconds()}')
            else:
                t1=datetime.now()
                # Process tasks as they complete without timeout
                tasks = list(task_dict.keys())
                while tasks:
                    done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                    for task in done:
                        key = task_dict[task]
                        try:
                            result = await task
                            if isinstance(result, dict):
                                if len(result['data']) != 0:
                                    results.append(result)
                            else:
                                results.append(result)
                                print(f' Length hotel results --- {len(result)}')
                            print(f' time hotel isinstance(result, dict) --- {(datetime.now() - t1).total_seconds()}')
                        except Exception as e:
                            print(f"Error in {key}: {e}")
                print(f' time hotel as_completed --- {(datetime.now() - t1).total_seconds()}')


            # just for debugging
            print("\n\n----------------------------")
            print("\t\t/sepehrsmart/app_crawl/hotel/main.py line 580 -> list_process_threads():", list_process_threads())
            print("----------------------------\n\n")

            t1=datetime.now()
            temp=self.read_data_ALLDestination(results)
            # print(f' time read_data_ALLDestination --- {(datetime.now() - t1).total_seconds()} ')
            print(f' time read_data_ALLDestination --- {(datetime.now() - t1).total_seconds()}')

            # just for debugging
            print("\n\n----------------------------")
            print("\t\t/sepehrsmart/app_crawl/hotel/main.py line 587 -> list_process_threads():", list_process_threads())
            print("----------------------------\n\n")

            #----------------------
            # add result_notExistProviders
            temp.extend(result_notExistProviders)
            #------------------


            return temp

        except Exception as e:
            # Log the error and the line number
            print(f"An error occurred: {e}")
            tb = traceback.format_exc()  # Get the full traceback as a string
            print(f"Traceback details:\n{tb}")

            return []

    #====


    def get_result(self,iter):

        if (len(self.hotelstarAnalysis)!=0):
            redis_key = f"{self.source}_{self.target}_{self.start_date}_{self.end_date}_{','.join(self.hotelstarAnalysis)}"
        else:
            redis_key = f"{self.source}_{self.target}_{self.start_date}_{self.end_date}_{self.adults}"



        t1=datetime.now()
        # Check cache first
        if self.use_cache:
            cached_result = get_dict_to_redis(redis_key) if check_redis_key(redis_key) else None
            if cached_result is not None:
                return cached_result
        print(f' time hotel redis_cache --- {(datetime.now() - t1).total_seconds()}')

        t1=datetime.now()
        # Fetch new data
        # result = asyncio.run(self.get_ALLDestination_data(iter))
        result = _loop.run_until_complete(self.get_ALLDestination_data(iter))
        print(f' time hotel get_ALLDestination_data --- {(datetime.now() - t1).total_seconds()}')

        # just for debugging
        print("\n\n----------------------------")
        print("\t\t/sepehrsmart/app_crawl/hotel/main.py line 630 -> list_process_threads():", list_process_threads())
        print("----------------------------\n\n")

        # Cache the result asynchronously if valid
        # Optimized Threading: Uses a single worker since Redis operations are I/O bound.
        #Faster Lookups: Only checks Redis once and avoids redundant keys
        t1 = datetime.now()
        if result:
            if self.provider and isinstance(self.provider, str) and self.provider != "":
                print("don't caching results because it's just for a specific provider")
            else:
                print('start caching ..........')
                with ThreadPoolExecutor(max_workers=1) as executor:
                    executor.submit(add_dict_to_redis, redis_key, result, self.redis_expire)

        # just for debugging
        print("\n\n----------------------------")
        print("\t\t/sepehrsmart/app_crawl/hotel/main.py line 641 -> list_process_threads():", list_process_threads())
        print("----------------------------\n\n")

        print(f' time hotel beforeSend --- {(datetime.now() - t1).total_seconds()}')

        return result


    def get_result_old(self,iter):


        redis_key = f"{self.source}_{self.target}_{self.start_date}_{self.end_date}_{self.adults}"
        if self.use_cache and check_redis_key(redis_key):
            return get_dict_to_redis(redis_key)
        else:

            result = self.get_ALLDestination_data(iter)
            #== Multi Thread ===
            print('start caching ..........')
            if len(result):
                with ThreadPoolExecutor(max_workers=100) as executorr:
                    executorr.submit(add_dict_to_redis, redis_key, result, self.redis_expire)  # bayad doing ha delete shavad!! (OK)
            #=====
            #

            return result
