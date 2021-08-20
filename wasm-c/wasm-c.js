function checkInt(value) {
  return parseInt(value) === value;
}

function checkInts(arrayish) {
  if (!checkInt(arrayish.length)) {
    return false;
  }

  for (var i = 0; i < arrayish.length; i++) {
    if (!checkInt(arrayish[i]) || arrayish[i] < 0 || arrayish[i] > 255) {
      return false;
    }
  }

  return true;
}

function coerceArray(arg, copy) {
  // ArrayBuffer view
  if (arg.buffer && ArrayBuffer.isView(arg)) {
    if (copy) {
      if (arg.slice) {
        arg = arg.slice();
      } else {
        arg = Array.prototype.slice.call(arg);
      }
    }

    return arg;
  }

  // It's an array; check it is a valid representation of a byte
  if (Array.isArray(arg)) {
    if (!checkInts(arg)) {
      throw new Error("Array contains invalid value: " + arg);
    }

    return new Uint8Array(arg);
  }

  // Something else, but behaves like an array (maybe a Buffer? Arguments?)
  if (checkInt(arg.length) && checkInts(arg)) {
    return new Uint8Array(arg);
  }

  throw new Error("unsupported array-like object");
}

function createEnv() {
  var memory = new WebAssembly.Memory({ initial: 24576, maximum: 24576 });
  var STACKTOP = 0;
  return {
    env: {
      memory: memory,
      STACKTOP
    }
  };
}

function staticMalloc() {
  var pointer = 2**14;
  return (size) => {
    pointer += size;
    return pointer - size;
  }
}

function aes(keySize) {
  var malloc = staticMalloc();

  var imports = createEnv();
  var byteView = new Uint8Array(imports.env.memory.buffer);

  var encryptionContextPointer = malloc(276);
  var decryptionContextPointer = malloc(276);
  var keyPointer = malloc(keySize / 8);
  var ivPointer = malloc(16);
  // rest of the memory
  var blockPointer = malloc(0);

  var currentMode;

  function loadData(data) {
    var byteData = coerceArray(data);
    byteView.set(byteData, blockPointer);
  }

  return {
    init: (key, iv, mode = 'CBC') => {
      byteView.set(iv, ivPointer);
      byteView.set(key, keyPointer);
      _aes_setkey_enc(encryptionContextPointer, keyPointer, keySize);
      _aes_setkey_dec(decryptionContextPointer, keyPointer, keySize);
      currentMode = mode;
    },
    encrypt: data => {
      loadData(data);
      if(currentMode === 'CBC') {
        _aes_crypt_cbc(encryptionContextPointer, 1, data.length, ivPointer, blockPointer, blockPointer);
      } else {
        _aes_crypt_ctr(encryptionContextPointer, data.length, ivPointer, blockPointer, blockPointer);
      }

      return byteView.subarray(blockPointer, blockPointer + data.length).slice();
    },
    decrypt: data => {
      loadData(data);
      if(currentMode === 'CBC') {
        _aes_crypt_cbc(decryptionContextPointer, 0, data.length, ivPointer, blockPointer, blockPointer);
      } else {
        _aes_crypt_ctr(encryptionContextPointer, data.length, ivPointer, blockPointer, blockPointer);
      }
      return byteView.subarray(blockPointer, blockPointer + data.length).slice();
    }
  };
};

function test_wasm_c(){
  var ivBuffer = coerceArray([0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
  0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f]);

  var keyBuffer = coerceArray([0x60, 0x3d, 0xeb, 0x10, 0x15, 0xca, 0x71, 0xbe,
  0x2b, 0x73, 0xae, 0xf0, 0x85, 0x7d, 0x77, 0x81, 0x1f, 0x35, 0x2c, 0x07, 0x3b,
  0x61, 0x08, 0xd7, 0x2d, 0x98, 0x10, 0xa3, 0x09, 0x14, 0xdf, 0xf4]);

  var crypt = aes(256)
  crypt.init(keyBuffer, ivBuffer);

  $.getJSON("/10MB.json", function(json) {      
    console.log("Testing WASM (C) 100MB") 

    var utf8Encode = new TextEncoder();
    var plainBuffer = coerceArray(utf8Encode.encode(JSON.stringify(json)));

    var j;
    for (j = 0; j < 10; j++) {
      console.log(j);
      var time_enc = {};
      var time_dec = {};

      for (i = 0; i < 10; i++) {
        /// ENCRYPT
        var st_date = new Date();
        var st_time = st_date.getTime(); 

        for (k = 0; k < 10; k++) {
          var cipher = crypt.encrypt(plainBuffer);
        }

        var end_date = new Date();
        var end_time = end_date.getTime();
        var diff = end_time - st_time;
        time_enc[i] = diff;     

        var st_date = new Date();
        var st_time = st_date.getTime();

        for (k = 0; k < 10; k++) {
          var result = crypt.decrypt(cipher);
        }
            
        var end_date = new Date();
        var end_time = end_date.getTime();
        var diff = end_time - st_time;
        time_dec[i] = diff;

        //console.log("Decrypted in "+ diff+ " ms");


        /// END DECRYPT
      }

      download(time_enc, `wasm_c_encrypt_100mb-${j}.json`);
      download(time_dec, `wasm_c_decrypt_100mb-${j}.json`);
    }
  });
}