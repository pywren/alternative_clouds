from requests import post, get
import string
import random
from multiprocessing.pool import ThreadPool

gcf_name = "list"
region_name = "us-central1"
project = "pywrenTest"

def random_string(N):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

def generate_payload(): 
    return {'storage_info' : random_string(40),
            'func_key' : random_string(40),
            'data_key' : random_string(40),
            'output_key' : random_string(40),
            'status_key' : random_string(40),
            'callset_id': random_string(40),
            'job_max_runtime' : random_string(40),
            'data_byte_range' : random_string(40),
            'call_id' : random_string(40),
            'use_cached_runtime' : random_string(40),
            'pywren_version' : random_string(40),
            'runtime_url' : random_string(40) }

def invoke():
    URL ="https://{}-{}.cloudfunctions.net/{}".format(region_name, project, gcf_name)
    HEADERS = {"Content-Type":"application/json"}
    res = post(URL, headers=HEADERS, json = generate_payload())
    print res.status_code
    print res.content
    return res.status_code

NUM_THREADS = 200
pool = ThreadPool(NUM_THREADS)

results = []
for i in range(NUM_THREADS):
    cb = pool.apply_async(invoke, ())
    results.append(cb)

res = [c.get() for c in results]
pool.close()

pool.join()

print res
