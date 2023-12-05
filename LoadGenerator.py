#!/usr/bin/env python
# coding: utf-8

# In[18]:


import requests
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
total_success = 0
total_failure = 0
total_time = 0

def make_api_request():
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

# Loop to make requests indefinitely
while True:
    # Make an API request
    result =make_api_request()

    total_success += result['success']
    total_failure += result['failed']
    total_time += result['response_time']

    time_to_sleep = 1 / frequency - result['response_time']
    if time_to_sleep > 0:
        time.sleep(time_to_sleep)

    # Calculate average response time
    if total_success > 0:
        average_response_time = total_time / total_success
    else:
        average_response_time = 0

    #print(f"Total successful requests: {success_count}")
    print(f"Total failed requests: {total_failure}")
    print(f"Average response time: {average_response_time:.4f} seconds")

#print(type(frequency))


# In[ ]:




