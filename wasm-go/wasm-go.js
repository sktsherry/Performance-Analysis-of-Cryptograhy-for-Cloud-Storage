function test_wasm_go(){
  $.getJSON("/10MB.json", function(json) {
    console.log("Testing WASM (Go)") 

    var myJSON1 = JSON.stringify(json);
    var time_enc = {};
    var time_dec = {};
  
    var i;
    for (i = 0; i < 10; i++) {
      /// ENCRYPT
      console.log("Encrypting FIle");        
      var st_date = new Date();
      var st_time = st_date.getTime();

      var encryp = encrypt(myJSON1)
          
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
    
      decrypt(encryp)
    
      var end_date = new Date();
      var end_time = end_date.getTime();
      var diff = end_time - st_time;
      time_dec[i] = diff;
          
      console.log("Decrypted in "+ diff+ " ms");
      
      /// END DECRYPT
    }

    download(time_enc, 'wasm_go_encrypt_10mb.json');
    download(time_dec, 'wasm_go_decrypt_10mb.json');
  });
}