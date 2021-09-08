# AES 256 encryption/decryption using pycrypto library
import sys
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
import json
from tqdm import tqdm
import time

mb = int(sys.argv[1])

if mb == 1:
    json_file = '1mb.json'
    saving_path = "Results/1MB/{}/AES-256-Local-1MB-{}.json"

if mb == 10:
    json_file = '10mb.json'
    saving_path = "Results/10MB/{}/AES-256-Local-10MB-{}.json"

if mb == 100:
    json_file = '100mb.json'
    saving_path = "Results/100MB/{}/AES-256-Local-100MB-{}.json"

print("\nStarting AES local script")
print("JSON size chosen = {}".format(sys.argv[1]))
print("File = {}".format(json_file))

BLOCK_SIZE = 16
pad = lambda s: bytes(s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE), 'utf-8')
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

# Read and transform json file into string
with open(json_file, encoding='utf-8') as file:
    json_string = json.load(file, strict=False)

json_string = json.dumps(json_string)

# Password to gen private key
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

print("\nEncryption started... ")
for i in tqdm(range(1000), desc="Completed "):
    times = {}
    
    start = time.perf_counter()        
    encrypted = encrypt(json_string, password)        
    times["0"] = round(time.perf_counter() - start, 7)

    with open(saving_path.format("Encrypt", i), 'w') as file:
        json.dump(times, file)

encrypted = encrypt(json_string, password)
print("\nDecryption started... ")
for i in tqdm(range(1000), desc="Completed "):
    times = {}
    start = time.perf_counter()        
    decrypted = decrypt(encrypted, password)        
    times["0"] = round(time.perf_counter() - start, 7)

    with open(saving_path.format("Decrypt", i), 'w') as file:
        json.dump(times, file)