function test_forgejs(){
  var key = forge.util.hexToBytes('603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4');
  var iv = forge.util.hexToBytes('feffe9928665731c6d6a8f9467308308');

  $.getJSON("/10MB.json", function(json) {      
    console.log("Testing FORGE.JS");

    var myJSON1 = JSON.stringify(json);
    var time_enc = {};
    var time_dec = {};

    var i;
    for (i = 0; i < 10; i++) {
      /// ENCRYPT
      var st_date = new Date();
      var st_time = st_date.getTime();      
      console.log("Encrypting File");        

      var cipher = forge.aes.createEncryptionCipher(key, 'CBC');
      cipher.start(iv);
      cipher.update(forge.util.createBuffer(myJSON1));
      cipher.finish();
      var encrypted = cipher.output;    
      // console.log(encrypted);

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
    
      var cipher = forge.aes.createDecryptionCipher(key, 'CBC');
      cipher.start(iv);
      cipher.update(encrypted);
      cipher.finish();
      var decrypted = cipher.output;    
      // console.log(decrypted);

      var end_date = new Date();
      var end_time = end_date.getTime();
      var diff = end_time - st_time;
      time_dec[i] = diff;
            
      console.log("Decrypted in "+ diff+ " ms");

      /// END DECRYPT
    }

    download(time_enc, 'forge_encrypt_10mb.json');
    download(time_dec, 'forge_decrypt_10mb.json');

    console.log("Successful")              
  });
}