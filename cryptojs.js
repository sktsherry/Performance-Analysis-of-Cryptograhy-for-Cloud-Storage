function test_cryptojs(){
  var cryptojs_key = CryptoJS.enc.Hex.parse('603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4');
  var cryptojs_iv = CryptoJS.enc.Hex.parse('feffe9928665731c6d6a8f9467308308'); 

  $.getJSON("/10MB.json", function(json) {      
    console.log("Testing CRYPTOJS.JS") 

    var myJSON1 = JSON.stringify(json);
    var time_enc = {};
    var time_dec = {};
    
    var i;
    for (i = 0; i < 10; i++) { 
      /// ENCRYPT
      var st_date = new Date();
      var st_time = st_date.getTime();      
      
      console.log("Encrypting File");        

      var cryptojs_ciphertxt = CryptoJS.AES.encrypt(myJSON1, cryptojs_key, {
        iv: cryptojs_iv, // parse the cryptojs_iv 
        padding: CryptoJS.pad.Pkcs7,
        mode: CryptoJS.mode.CBC
      });

      var end_date = new Date();
      var end_time = end_date.getTime();
      var diff = end_time - st_time;
      time_enc[i] = diff;
      
      console.log("Encrypted in " + diff + " ms");
      // console.log(cryptojs_ciphertxt.toString());

      /// END ENCRYPT
        
      /// DECRYPT

      console.log("Decrypting File");        

      var st_date = new Date();
      var st_time = st_date.getTime();
    
      var cryptojs_dec = CryptoJS.AES.decrypt(cryptojs_ciphertxt, cryptojs_key, {
        iv: cryptojs_iv, // parse the cryptojs_iv 
        padding: CryptoJS.pad.Pkcs7,
        mode: CryptoJS.mode.CBC
      });

      var end_date = new Date();
      var end_time = end_date.getTime();
      var diff = end_time - st_time;
      time_dec[i] = diff;
            
      console.log("Decrypted in "+ diff+ " ms");
      // console.log(cryptojs_dec.toString(CryptoJS.enc.Utf8))

      /// END DECRYPT
    }

    download(time_enc, 'cryptojs_encrypt_10mb.json');
    download(time_dec, 'cryptojs_decrypt_10mb.json');

    console.log("Successful")              
  });
}