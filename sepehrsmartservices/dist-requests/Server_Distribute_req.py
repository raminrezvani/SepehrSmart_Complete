import os
from flask import Flask, request, jsonify, make_response
import requests
import json
import itertools
import queue
import threading
from concurrent.futures import Future
import time
import gzip
import sys
from io import BytesIO

os.system("title Distribute Requests")

# Set up the task queue and worker threads
NUM_WORKER_THREADS = 125  # Number of worker threads per process
TIMEOUT = 55
task_queue = queue.PriorityQueue()
task_counter = itertools.count()  # Unique counter for tie-breaking in the queue
thread_info = {}  # Dictionary to store thread info: {ident: {'creation_time': float, 'is_running': bool, 'thread': Thread}}
threads_to_stop = set()  # Set of thread idents marked for termination
thread_info_lock = threading.Lock()  # Lock for thread_info and threads_to_stop

# Define the ExeRequest class
class ExeRequest:
    def __init__(self, method, url, params, cookies, headers, data, json_data, start_time):
        self.method = method
        self.url = url
        self.params = params
        self.cookies = cookies
        self.headers = headers
        self.data = data
        self.json_data = json_data
        self.future = Future()
        self.start_time = start_time  # Time when the request was received
        self.retries = 0  # Number of retry attempts

# Function to execute the HTTP request
def execute_request(method, url, params, cookies, headers, data, json_data):
    try:
        if method.lower() == 'get':
            return requests.get(url, params=params, cookies=cookies, headers=headers, data=data, json=json_data, timeout=TIMEOUT)
        elif method.lower() == 'post':
            return requests.post(url, params=params, cookies=cookies, headers=headers, data=data, json=json_data, timeout=TIMEOUT)
        else:
            raise ValueError(f"Unsupported method: {method}")
    except requests.RequestException as e:
        raise e

def make_gzip_response(data, status_code=200):
    json_data = json.dumps(data).encode('utf-8')
    accept_encoding = request.headers.get('Accept-Encoding', '')
    if 'gzip' in accept_encoding.lower():
        out = BytesIO()
        with gzip.GzipFile(fileobj=out, mode='w') as f:
            f.write(json_data)
        compressed_data = out.getvalue()
        response = make_response(compressed_data, status_code)
        response.headers['Content-Encoding'] = 'gzip'
        response.headers['Content-Length'] = len(compressed_data)
    else:
        response = make_response(json_data, status_code)
    response.headers['Content-Type'] = 'application/json'
    response.headers['Vary'] = 'Accept-Encoding'
    return response

# Worker function with stop flag checking
def worker():
    my_ident = threading.current_thread().ident
    with thread_info_lock:
        thread_info[my_ident] = {
            'creation_time': time.time(),
            'is_running': False,
            'thread': threading.current_thread()
        }
    while True:
        try:
            priority, count, exeRequest = task_queue.get(timeout=1)
            print(f"Thread '{my_ident}' received a task!", flush=True)
            with thread_info_lock:
                # if my_ident in threads_to_stop:
                #     break
                thread_info[my_ident]['is_running'] = True
            # Process the request
            max_tries = 2
            retry_delay = 1
            while exeRequest.retries < max_tries:
                try:
                    response = execute_request(
                        exeRequest.method,
                        exeRequest.url,
                        exeRequest.params,
                        exeRequest.cookies,
                        exeRequest.headers,
                        exeRequest.data,
                        exeRequest.json_data
                    )
                    result_payload = {
                        'status_code': response.status_code,
                        'text': response.text,
                        'cookies': response.cookies.get_dict()
                    }
                    response.close()
                    exeRequest.future.set_result(result_payload)
                    del response, result_payload
                    break
                except Exception as e:
                    exeRequest.retries += 1
                    current_time = time.time()
                    if current_time - exeRequest.start_time >= TIMEOUT:
                        exeRequest.future.set_exception(TimeoutError(f"Request timed out after {TIMEOUT} seconds"))
                        break
                    if exeRequest.retries >= max_tries:
                        exeRequest.future.set_exception(e)
                        break
                    time.sleep(retry_delay)
            else:
                if not exeRequest.future.done():
                    exeRequest.future.set_exception(Exception("All retry attempts failed"))
            task_queue.task_done()
            del exeRequest
            with thread_info_lock:
                thread_info[my_ident]['is_running'] = False
                if my_ident in threads_to_stop:
                    break
        except queue.Empty:
            with thread_info_lock:
                if my_ident in threads_to_stop:
                    break

    # Cleanup on exit
    with thread_info_lock:
        del thread_info[my_ident]
        threads_to_stop.discard(my_ident)
        print(f"Thread '{my_ident}' deleted successfully!", flush=True)

# Start a single worker thread
def start_worker():
    thread = threading.Thread(target=worker, daemon=True)
    thread.start()

# Start initial worker threads
def start_workers(num_threads=NUM_WORKER_THREADS):
    for _ in range(num_threads):
        start_worker()

# Thread manager to kill and replace 20% of threads every 6 minutes
def thread_manager():
    while True:
        time.sleep(6 * 60)  # 6 minutes
        with thread_info_lock:
            idle_threads = [
                (ident, info)
                for ident, info in thread_info.items()
                if not info['is_running'] and info['thread'].is_alive()
            ]
            idle_threads.sort(key=lambda x: x[1]['creation_time'])
            to_kill = idle_threads[:25]  # Kill up to 25 (20% of 125)
            for ident, _ in to_kill:
                threads_to_stop.add(ident)
                print(f"Thread '{ident}' added to deletion list!", flush=True)
        # Replace killed threads
        for _ in range(len(to_kill)):
            start_worker()

# Initialize Flask app
app = Flask(__name__)

# Define the /remoteRequest endpoint
@app.route('/remoteRequest', methods=['GET'])
def remoteRequest():
    # Extract query parameters with defaults
    url = request.args.get('url', '')
    if not url:
        return jsonify({'error': 'URL parameter is required'}), 400
    
    method = request.args.get('method', 'GET')
    params = json.loads(request.args.get('params', '{}'))
    cookies = json.loads(request.args.get('cookies', '{}'))
    headers = json.loads(request.args.get('headers', '{}'))
    data = json.loads(request.args.get('data', '{}')) if method.lower() == 'post' else None
    json_data = json.loads(request.args.get('json', '{}')) if method.lower() == 'post' else None
    priority = float(request.args.get('priorityTimestamp', time.time()))  # Lower values = higher priority
    start_time = time.time()  # Record the time when the request was received

    # Create an ExeRequest object and queue it
    exe_request = ExeRequest(method, url, params, cookies, headers, data, json_data, start_time)
    count = next(task_counter)
    task_queue.put((priority, count, exe_request))

    # Wait for the result with a timeout
    try:
        result = exe_request.future.result(timeout=TIMEOUT)
        return jsonify(result)
    except TimeoutError:
        return jsonify({'error': 'Request timed out'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500

start_workers()
# Start the thread manager
manager_thread = threading.Thread(target=thread_manager, daemon=True)
manager_thread.start()

if __name__ == '__main__':
    port = int(sys.argv[1]) # Get port from command line
    app.run(host='0.0.0.0', port=port)
