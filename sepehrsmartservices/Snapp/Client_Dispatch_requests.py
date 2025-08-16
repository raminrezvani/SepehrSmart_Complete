import os
import requests
import concurrent.futures
import time
import json
import redis
from itertools import cycle
import hashlib
import environ
import socket
import random

# Initialize environment variables
env = environ.Env(
    DEBUG=(bool, False)
)

# reading .env file
environ.Env.read_env('.env')

APP_WORKERS = int(env('APP_WORKERS'))
REDIS_HOST = env('REDIS_HOST')
REDIS_PORT = env('REDIS_PORT')
REDIS_PASSWORD = env('REDIS_PASSWORD')

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=0, decode_responses=True)

# Define servers and ports
servers = [
    # ("130.185.77.24", [6000, 6001, 6002, 6003, 6004, 6005]),
    ("45.149.76.168", [6000, 6001, 6002, 6003, 6004, 6005]),
    # ("185.252.28.58", [6000, 6001, 6002, 6003, 6004, 6005]),
    ("185.252.30.120", [6000, 6001, 6002, 6003, 6004, 6005]),
    ("188.121.102.104", [6000, 6001, 6002, 6003, 6004, 6005]),
    ("185.252.31.31", [6000, 6001, 6002, 6003, 6004, 6005]),
]

healthy_servers = []  # List to store healthy servers
healthy_servers_cycle = cycle(healthy_servers)
last_update_time = 0  # Timestamp of the last update of healthy servers
is_checking_health = False
worker_id = int(os.getenv('WORKER_ID', 0))
HEALTH_CHECK_INTERVAL = 900 # interval between each health check in seconds (15 minutes)
HEALTH_CHECK_TIMEOUT = 2 # in seconds
REQUEST_TIMEOUT = 35

# Round-robin cycle for selecting servers
server_cycle = cycle([server for server, _ in servers])

# Dictionary to store which server is assigned to each priorityTimestamp
timestamp_server_map = {}

# Dictionary to store round-robin port selection for each server
server_port_cycles = {
    server: cycle(ports) for server, ports in servers
}


def get_cache_key(method, url, params, cookies, headers, data, json_data,isSepehr):
    """Generate a unique Redis cache key based on request parameters."""
    if (isSepehr=='0'):
        request_string = json.dumps({
            'method': method,
            'url': url,
            'params': params,
            'cookies': cookies,
            'headers': headers,
            'data': data,
            'json': json_data,
        }, sort_keys=True)
        return "request_cache:" + hashlib.md5(request_string.encode()).hexdigest()
    if (isSepehr=='1'):
        request_string = json.dumps({
            'method': method,
            'url': url,
            'cookies': cookies,
            'headers': headers,
            'data': data,
            'json': json_data,
        }, sort_keys=True)
        return "request_cache:" + hashlib.md5(request_string.encode()).hexdigest()



def fetch_and_cache_response(full_url, serverparams, cache_key, priorityTimestamp, selected_port):
    """Fetch response from server and cache it with priorityTimestamp."""
    response = requests.get(full_url, params=serverparams, timeout=REQUEST_TIMEOUT)
    if response.status_code == 200:
        print(
            f"Sent request to {full_url} with priority {priorityTimestamp}, Response: {response.status_code}, port=== {selected_port}")

        # Store response with priorityTimestamp in Redis as a JSON object
        cache_data = {
            "response": response.text,
            "priorityTimestamp": priorityTimestamp
        }
        redis_client.setex(cache_key, 3600, json.dumps(cache_data))  # Cache for 1 hour
        return response.text
    else:
        return []  # Return empty list on failure, per original code



def check_server_health(server_ip, ports):
    """
    Check the health of a specific server by attempting to connect to a random port.

    :param server_ip: The IP address of the server to check.
    :param ports: List of available ports for the server.
    :return: True if the server is reachable within 2 seconds, False otherwise.
    """
    # Select a random port from the available ports
    port = random.choice(ports)
    
    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Set a timeout of 2 seconds
    sock.settimeout(HEALTH_CHECK_TIMEOUT)
    
    try:
        # Attempt to connect to the server
        sock.connect((server_ip, port))
        print(f"Success: Connected to {server_ip} on port {port}.")
        return True  # Connection successful
    except (socket.timeout, socket.error):
        print(f"WARNING: Failure: Could not connect to {server_ip} on port {port}.")
        return False  # Connection failed or timed out
    finally:
        sock.close()  # Ensure the socket is closed



def update_healthy_servers():
    """Check the health of all servers and update the list of healthy servers."""
    global healthy_servers, last_update_time, is_checking_health, healthy_servers_cycle
    should_check = True
    if is_checking_health:
        should_check = False
        time.sleep(HEALTH_CHECK_TIMEOUT)
        if is_checking_health:
            should_check = True

    if should_check:
        is_checking_health = True
        with concurrent.futures.ThreadPoolExecutor() as executor:
            health_checks = {
                executor.submit(check_server_health, server_ip, ports): server_ip
                for server_ip, ports in servers
            }
            
            new_healthy_servers = []
            for future in concurrent.futures.as_completed(health_checks):
                server_ip = health_checks[future]
                is_healthy = future.result()
                if is_healthy:
                    new_healthy_servers.append(server_ip)

            healthy_servers = sorted(new_healthy_servers)  # Update the global list of healthy servers
            healthy_servers_cycle = cycle(healthy_servers)
            last_update_time = time.time()  # Update the last update time
            is_checking_health = False
            print(f"Updated healthy servers: {healthy_servers}")
    else:
        print(f"Don't need to check health.")
        return



def executeRequest(method, url,
                   params=None, cookies=None,
                   headers=None, data=None,
                   json_data=None,
                   verify=False,
                   priorityTimestamp=1,
                   use_cache='true',
                   forceGet=0,
                   isSepehr='0'):

    if str(use_cache).lower()=='false':
        use_cache=0
    if str(use_cache).lower()=='true':
        use_cache=1

    # Just for more information
    print("-"*75, "Worker ID:", worker_id)

    """Execute a request with caching, priorityTimestamp, and forceGet logic."""
    cache_key = get_cache_key(method, url, params, cookies, headers, data, json_data,isSepehr)

    # Check Redis for cached response
    cached_data = redis_client.get(cache_key)
    if cached_data:
        print(f"Cache hit for {url} )")


    # Check if we need to update the healthy servers (if more than 10 minutes have passed)
    current_time = time.time()
    if current_time - last_update_time > HEALTH_CHECK_INTERVAL:
        print("Updating healthy servers due to timeout.")
        update_healthy_servers()

    # If there are no healthy servers, return early
    if not healthy_servers:
        print(f"ERROR: No healthy servers available for timestamp {priorityTimestamp}.")
        return

    # If this priorityTimestamp doesn't have a server assigned, pick the next one in round-robin
    if priorityTimestamp not in timestamp_server_map:
        next_server = healthy_servers[ (len(timestamp_server_map) * APP_WORKERS + worker_id) % len(healthy_servers)]
        timestamp_server_map[priorityTimestamp] = next_server

    selected_server = timestamp_server_map[priorityTimestamp]


    # ---------------
    # for priorityTimestamp==1: (to round robin serve)
    #--------------
    if (priorityTimestamp == 1 or priorityTimestamp == '1'):
        selected_server = next(healthy_servers_cycle)
    # -----------------


    # Select a port from the server's round-robin port cycle
    selected_port = next(server_port_cycles[selected_server])

    # Construct the request URL
    full_url = f"http://{selected_server}:{selected_port}/remoteRequest"

    # Prepare the request parameters
    serverparams = {
        'url': url,
        'params': json.dumps(params) if params is not None else '{}',
        'cookies': json.dumps(cookies) if cookies is not None else '{}',
        'headers': json.dumps(headers) if headers is not None else '{}',
        'method': method,
        'data': json.dumps(data) if data is not None else '{}',
        'json': json.dumps(json_data) if json_data is not None else '{}',
        'priorityTimestamp': priorityTimestamp,
    }
    print(f'Timestamp ======= {priorityTimestamp}')
    # Handle forceGet logic
    if forceGet==1:
        print(f"ForceGet=True: Skipping cache, fetching new response with priority {priorityTimestamp}")
        return fetch_and_cache_response(full_url, serverparams, cache_key, priorityTimestamp, selected_port)


    # print(f'Redis timestamp === {}')
    if use_cache==1 and cached_data:
        print('caching and haveData...')
        # Use cached response if use_cache=True and cache exists
        cache_data = json.loads(cached_data)
        cached_response = cache_data["response"]
        cached_priority = cache_data["priorityTimestamp"]
        print(f"Cache hit for {url} with priority {cached_priority}")
        return cached_response
    elif use_cache==0 and cached_data:
        print('not caching and checkTimestamp...')
        # When use_cache=False, check priorityTimestamp
        cache_data = json.loads(cached_data)
        cached_priority = cache_data["priorityTimestamp"]
        print(f' eauality ;::::: {cached_priority}  !!!!  {priorityTimestamp}')

        time_difference_seconds = float(priorityTimestamp) - float(cached_priority)

        if time_difference_seconds>5*60:   # 20 second for caching ....

            print(
                f"Skipping cache with older priority {cached_priority}, fetching new response with {priorityTimestamp}---Timeee== {time_difference_seconds}")
            return fetch_and_cache_response(full_url, serverparams, cache_key, priorityTimestamp, selected_port)
        else:
            print(f"Using cached response with priority {cached_priority} (newer or equal to {priorityTimestamp})")
            return cache_data["response"]
    else:
        print('not data...')
        # No cache exists or forceGet=False with no cache, fetch new response
        return fetch_and_cache_response(full_url, serverparams, cache_key, priorityTimestamp, selected_port)

#
# # Example usage:
# if __name__ == "__main__":
#     response = executeRequest(
#         method="GET",
#         url="https://example.com",
#         priorityTimestamp=1677655000,
#         use_cache=True,
#         forceGet=False
#     )
#     print(response)