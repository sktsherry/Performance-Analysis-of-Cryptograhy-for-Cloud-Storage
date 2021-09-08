# AES 256 encryption/decryption using pycrypto library
import sys
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Random import get_random_bytes
import json
from tqdm import tqdm
import time

mb = int(sys.argv[1])

if mb == 1:
    json_file = '1attr_1mb.json'
    saving_path = "Results/1MB/AES-256-Local-1MB-{}.json"

if mb == 10:
    json_file = '10attr_10mb_10.json'
    saving_path = "Results/10MB/AES-256-Local-10MB-{}.json"

if mb == 100:
    json_file = '100attr_100mb.json'
    saving_path = "Results/100MB/AES-256-Local-100MB-{}.json"

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

encrypted = encrypt(json_string, password)
# print(encrypted)
for i in range(0,10):    
    start = time.perf_counter()        
    decrypted = decrypt(encrypted, password)
    time.perf_counter() - start, 7
    print(output)
    #print(encrypted)
sys.exit()


# Let us decrypt using our original password
#print("\nJson decrypted = {}".format(bytes.decode(decrypted)))