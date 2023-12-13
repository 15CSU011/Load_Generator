#!/usr/bin/env python
# coding: utf-8

import requests
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import time
import os
import re

load_dotenv('.env')

target = os.getenv('target')
frequency = os.getenv('frequency')
frequency = int(frequency)

print(target)
print(frequency)


def make_api_request():
    try:
        response = requests.get(target, timeout=10)
        if response.status_code == 200:
            print('API request successful')
            t = response.text
            result = re.split(r'\s+', t)
            return {
                'success': 1,
                'failed': 0,
                'response_time': int(result[1])
            }
        else:
            print('Failed to make API request')
            return {
                'success': 0,
                'failed': 1,
                'response_time': 0
            }
    except requests.exceptions.Timeout:
        print('Timeout occurred during API request')
        return {
            'success': 0,
            'failed': 1,
            'response_time': 0
        }

def run_in_thread(func, executor, sleep_time):
    return executor.submit(func).result(), sleep_time

def main():
    total_success = 0
    total_failure = 0
    total_time = 0
    executor = ThreadPoolExecutor(max_workers=frequency)
    start_time = time.time()
    

    while True:
        # Make an API request using a thread
        sleep_time = 1 / frequency
        result, sleep_time = run_in_thread(make_api_request, executor, sleep_time)

        total_success += result['success']
        total_failure += result['failed']
        total_time += result['response_time']

        time.sleep(sleep_time)

        # Calculate average response time
        if total_success > 0:
            average_response_time = total_time / total_success
        else:
            average_response_time = 0
        #print(f"Total success requests: {total_success}")
        print(f"Total failed requests: {total_failure}")
        print(f"Average response time: {average_response_time:.4f} seconds")

if __name__ == "__main__":
    main()
