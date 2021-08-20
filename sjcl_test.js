function test_sjcl(){
	$.getJSON("/100MB.json", function(json) {

		password="teste"
		var key = sjcl.misc.pbkdf2(password, sjcl.codec.utf8String.toBits('ssssssss'), 1000, 256)

		var p = sjcl.json.defaults;
		var iv  = new Uint8Array(16);
		for (var i = 0; i < iv.length; ++i) {
			iv[i] = 0;
		}
		p.iv = sjcl.codec.bytes.toBits(iv);
		p.salt = [];
		p.mode = "cbc";
		var aes = new sjcl.cipher.aes(key);
		sjcl.beware["CBC mode is dangerous because it doesn't protect message integrity."]()

		console.log("Testing SJCL.JS 100MB") 
	    var myJSON1 = JSON.stringify(json);

	    var j;
    	for (j = 1; j < 10; j++) {
    		console.log(j);
		    var time_enc = {};
		    var time_dec = {};
		    
		    var i;
		    for (i = 0; i < 10; i++) {
		    	var st_date = new Date();
		    	var st_time = st_date.getTime();      
		    	//console.log("Encrypting JSON File");

		    	var encrypted = sjcl.mode.cbc.encrypt(aes, sjcl.codec.utf8String.toBits(myJSON1), p.iv);

		    	var end_date = new Date();
		    	var end_time = end_date.getTime();
		    	var diff = end_time - st_time;
		    	time_enc[i] = diff;
		    	//console.log("Encrypted in " + diff + " ms");

		    	//console.log("Decrypting JSON File");        
		    	var st_date = new Date();
		    	var st_time = st_date.getTime();

		    	var decrypted = sjcl.mode[p.mode].decrypt(aes, encrypted, p.iv);

		    	var end_date = new Date();
	      		var end_time = end_date.getTime();
	      		var diff = end_time - st_time;        
	      		time_dec[i] = diff;

	      		//console.log("Decrypted in "+ diff+ " ms"); 
		    }

		download(time_enc, `sjcl_encrypt_100mb-${j}.json`);
		download(time_dec, `sjcl_decrypt_100mb-${j}.json`);

	    }

    	console.log("Successful") 
	});
}