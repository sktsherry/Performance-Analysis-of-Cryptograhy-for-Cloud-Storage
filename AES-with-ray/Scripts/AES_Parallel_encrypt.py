# AES 256 encryption/decryption using pycrypto library
 
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
from tqdm import tqdm
import json
import time
import sys
import ray

print("Starting Script and Ray...")
ray.init()

PROCESS_NUMBER = 1
BLOCK_SIZE = 16
pad = lambda s: bytes(s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE), 'utf-8')
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

MB_FILE = 100

with open('100mb.json', encoding='utf-8') as file:
    json_string = json.load(file, strict=False)

json_string = json.dumps(json_string)
#password = input("Enter encryption password: ")
password = '0123456789abcdef'

def encrypt(raw, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    raw = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))
     
     
def decrypt(enc, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]))

@ray.remote
def measure_time_individual(parallel_number, path):
    times = {}
    start = time.perf_counter()    
    encrypted = encrypt(json_string, password)    
    times[parallel_number] = round(time.perf_counter() - start, 7)
    with open(path.format(MB_FILE, MB_FILE, parallel_number), 'w') as file:
        json.dump(times, file)
    return

@ray.remote
def measure_time_total():    
    encrypted = encrypt(json_string, password)    
    return

# @ray.remote
# def measure_time_per_user(parallel_number, path, request_time):
#     times = {}
#     start = time.perf_counter()
#     # First let us encrypt secret message
#     encrypted = encrypt(json_string, password)
#     #print("\nJson encrypted = {}".format(encrypted))
#     #times[parallel_number] = round(time.perf_counter() - request_time, 7)
#     times[parallel_number] = round(time.perf_counter() - request_time, 7)
#     with open(path.format(MB_FILE, parallel_number), 'w') as file:
#         json.dump(times, file)
#     return

if __name__ == "__main__":

    ###### Warm up
    print("\n\n\nWarming up...")
    for w in tqdm(range(10), desc="Completed "):
        encrypt(json_string, password)


    # Experiments
    ############################
    # path_1_individual = "../Results-Encrypt/{}MB/individual_proc/1_proc/AES-256-Parallel-1MB-{}.json"
    path_1_total = "../Results-Encrypt/{}MB/total_proc/AES-256-Parallel-total-1.json".format(MB_FILE)
    # # path_10_per_user = "../Results-Encrypt/{}MB/per_user/10_proc/AES-256-Parallel-per-user-1MB-{}.json"    

    # print("\n\n\nRunning AES-256 for 1 process")
    # for j in tqdm(range(1000), desc="Completed "):
    #     proc_1 = []
    #     for i in range(1):
    #         json_id = j * 10 + i
    #         proc_1.append(measure_time_individual.remote(json_id, path_1_individual)) 
    #     ray.get(proc_1)


    # times = {}
    # print("\nRunning AES-256 for 1 process")
    # for k in tqdm(range(1000), desc="Completed "):
    #     proc_1 = []
    #     for i in range(1):
    #         proc_1.append(measure_time_total.remote())
    #     start = time.perf_counter()
    #     ray.get(proc_1)
    #     times[k] = round(time.perf_counter() - start, 7)
    # with open(path_1_total, 'w') as file:
    #         json.dump(times, file)


    path_10_individual = "../Results-Encrypt/{}MB/individual_proc/10_proc/AES-256-Parallel-{}MB-{}.json"
    path_10_total = "../Results-Encrypt/{}MB/total_proc/AES-256-Parallel-total-10.json".format(MB_FILE)
    # path_10_per_user = "../Results-Encrypt/{}MB/per_user/10_proc/AES-256-Parallel-per-user-1MB-{}.json"    

    # print("\n\n\nRunning AES-256 in Parallel individual time with 10 processes")
    # for j in tqdm(range(1000), desc="Completed "):
    #     proc_10 = []
    #     for i in range(10):
    #         json_id = j * 10 + i
    #         proc_10.append(measure_time_individual.remote(json_id, path_10_individual)) 
    #     ray.get(proc_10)


    # times = {}
    # print("\nRunning AES-256 in Parallel total time to 10 processes")
    # for k in tqdm(range(1000), desc="Completed "):
    #     proc_10 = []
    #     for i in range(10):
    #         proc_10.append(measure_time_total.remote())
    #     start = time.perf_counter()
    #     ray.get(proc_10)
    #     times[k] = round(time.perf_counter() - start, 7)
    # with open(path_10_total, 'w') as file:
    #         json.dump(times, file)

    # print("\n\n\nRunning AES-256 in Parallel per-user time with 10 processes")
    # for j in tqdm(range(100), desc="Completed "):
    #     proc_10 = []
    #     for i in range(10):
    #         json_id = j * 10 + i
    #         proc_10.append(measure_time_per_user.remote(json_id, path_10_per_user, time.perf_counter())) 
    #     ray.get(proc_10)


    # ############################
    # ############################

    path_20_individual = "../Results-Encrypt/{}MB/individual_proc/20_proc/AES-256-Parallel-{}MB-{}.json"
    path_20_total = "../Results-Encrypt/{}MB/total_proc/AES-256-Parallel-total-20.json".format(MB_FILE)

    # print("\n\n\nRunning AES-256 in Parallel individual time with 20 processes")
    # for j in tqdm(range(1000), desc="Completed "):
    #     proc_20 = []
    #     for i in range(20):
    #         json_id = j * 10 + i
    #         proc_20.append(measure_time_individual.remote(json_id, path_20_individual)) 
    #     ray.get(proc_20)


    # times = {}
    # print("\nRunning AES-256 in Parallel total time to 20 processes")
    # for k in tqdm(range(1000), desc="Completed "):
    #     proc_20 = []
    #     for i in range(20):
    #         proc_20.append(measure_time_total.remote())
    #     start = time.perf_counter()
    #     results = ray.get(proc_20)
    #     times[k] = round(time.perf_counter() - start, 7)
    # with open(path_20_total, 'w') as file:
    #         json.dump(times, file)



    ############################
    ############################

    path_30_individual = "../Results-Encrypt/{}MB/individual_proc/30_proc/AES-256-Parallel-{}MB-{}.json"
    path_30_total = "../Results-Encrypt/{}MB/total_proc/AES-256-Parallel-total-30.json".format(MB_FILE) 

    # print("\n\n\nRunning AES-256 in Parallel individual time with 30 processes")
    # for j in tqdm(range(1000), desc="Completed "):
    #     proc_30 = []
    #     for i in range(30):
    #         json_id = j * 10 + i
    #         proc_30.append(measure_time_individual.remote(json_id, path_30_individual)) 
    #     ray.get(proc_30)


    # times = {}
    # print("\nRunning AES-256 in Parallel total time to 30 processes")
    # for k in tqdm(range(1000), desc="Completed "):
    #     proc_30 = []
    #     for i in range(30):
    #         proc_30.append(measure_time_total.remote())
    #     start = time.perf_counter()
    #     ray.get(proc_30)
    #     times[k] = round(time.perf_counter() - start, 7)
    # with open(path_30_total, 'w') as file:
    #         json.dump(times, file)


    ############################
    ############################

    path_40_individual = "../Results-Encrypt/{}MB/individual_proc/40_proc/AES-256-Parallel-{}MB-{}.json"
    path_40_total = "../Results-Encrypt/{}MB/total_proc/AES-256-Parallel-total-40.json".format(MB_FILE)

    # print("\n\n\nRunning AES-256 in Parallel individual time with 40 processes")
    # for j in tqdm(range(1000), desc="Completed "):
    #     proc_40 = []
    #     for i in range(40):
    #         json_id = j * 10 + i
    #         proc_40.append(measure_time_individual.remote(json_id, path_40_individual)) 
    #     ray.get(proc_40)


    # times = {}
    # print("\nRunning AES-256 in Parallel total time to 40 processes")
    # for k in tqdm(range(1000), desc="Completed "):
    #     proc_40 = []
    #     for i in range(40):
    #         proc_40.append(measure_time_total.remote())
    #     start = time.perf_counter()
    #     ray.get(proc_40)
    #     times[k] = round(time.perf_counter() - start, 7)
    # with open(path_40_total, 'w') as file:
    #         json.dump(times, file)


    # ############################
    # ############################

    path_50_individual = "../Results-Encrypt/{}MB/individual_proc/50_proc/AES-256-Parallel-{}MB-{}.json"
    path_50_total = "../Results-Encrypt/{}MB/total_proc/AES-256-Parallel-total-50.json".format(MB_FILE)

    # print("\n\n\nRunning AES-256 in Parallel individual time with 50 processes")
    # for j in tqdm(range(1000), desc="Completed "):
    #     proc_50 = []
    #     for i in range(50):
    #         json_id = j * 10 + i
    #         proc_50.append(measure_time_individual.remote(json_id, path_50_individual)) 
    #     ray.get(proc_50)


    times = {}
    print("\nRunning AES-256 in Parallel total time to 50 processes")
    for k in tqdm(range(10), desc="Completed "):
        proc_50 = []
        for i in range(50):
            proc_50.append(measure_time_total.remote())
        start = time.perf_counter()
        ray.get(proc_50)
        times[k] = round(time.perf_counter() - start, 7)
    with open(path_50_total, 'w') as file:
            json.dump(times, file)

    # ############################
    # ############################


    # # path_100_individual = "../Results-Encrypt/{}MB/individual_proc/100_proc/AES-256-Parallel-10MB-{}.json"
    # # path_100_total = "../Results-Encrypt/10MB/total_proc/AES-256-Parallel-total-100.json"


    # # print("\n\n\nRunning AES-256 in Parallel individual time with 100 processes")
    # # for j in tqdm(range(100), desc="Completed "):
    # #     proc_100 = []
    # #     for i in range(1,101):
    # #         json_id = j * 10 + i
    # #         proc_100.append(measure_time.remote(json_id, path_100_individual)) 
    # #     ray.get(proc_100)


    # # times = {}
    # # print("\nRunning AES-256 in Parallel total time to 100 processes")
    # # for k in tqdm(range(1, 1001), desc="Completed "):
    # #     proc_100 = []
    # #     for i in range(1,101):
    # #         proc_100.append(measure_time.remote(i, path_100_individual))
    # #     start = time.perf_counter()
    # #     ray.get(proc_100)
    # #     times[k] = round(time.perf_counter() - start, 7)
    # # with open(path_100_total, 'w') as file:
    # #         json.dump(times, file)
    # """


    # # Let us decrypt using our original password
    # #decrypted = decrypt(encrypted, password)
    # #print("\nJson decrypted = {}".format(bytes.decode(decrypted)))
    # """