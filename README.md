# Server-side vs client-side cryptography performance comparison 

## Server-side benchmarking experiment

### PyCrypto without concurrency

* `cd aes-without-ray/`
*  run benchmarking with `python3 script.py (param: mb size as integer)`

### Pycrypto with concurrency

* `cd aes-with-ray/Scripts/`
*  run benchmarking with `python3 script.py`
* change file sizes inside script

## Browser-based AES benchmarking experiment

### Running the experiment

* `python3 -m http.server 8003`
* go to `http://localhost:8003/` in a web browser
* click the buttons