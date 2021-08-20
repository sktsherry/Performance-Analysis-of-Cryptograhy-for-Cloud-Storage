function test_asm(){
  var k = asmCrypto.hex_to_bytes('603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4'); 
  var iv = asmCrypto.hex_to_bytes('feffe9928665731c6d6a8f9467308308');

  $.getJSON("/10MB.json", function(json) {      
    console.log("Testing ASMCRYPTO.JS") 

    var myJSON1 = JSON.stringify(json);
    var clear = new TextEncoder().encode(myJSON1);
    var time_enc = {};
    var time_dec = {};
    
    var i;
    for (i = 0; i < 10; i++) { 
      /// ENCRYPT
      var st_date = new Date();
      var st_time = st_date.getTime();      
      console.log("Encrypting File");        

      enc = asmCrypto.AES_CBC.encrypt(clear, k, true, iv);
      // console.log(enc);

      var end_date = new Date();
      var end_time = end_date.getTime();
      var diff = end_time - st_time;
      time_enc[i] = diff;

      console.log("Encrypted in " + diff + " ms");

      /// END ENCRYPT
        
      /// DECRYPT
      console.log("Decrypting JSON File");        
      var st_date = new Date();
      var st_time = st_date.getTime();
    
      dec = asmCrypto.AES_CBC.decrypt(enc, k, true, iv);
      var decrypt = new TextDecoder().decode(dec);

      var end_date = new Date();
      var end_time = end_date.getTime();
      var diff = end_time - st_time;        
      time_dec[i] = diff;

      // console.log(decrypt)            
      console.log("Decrypted in "+ diff+ " ms"); 
      
      /// END DECRYPT
    }

    download(time_enc, 'asmcrypto_encrypt_10mb.json');
    download(time_dec, 'asmcrypto_decrypt_10mb.json');

    console.log("Successful")    
  });
}