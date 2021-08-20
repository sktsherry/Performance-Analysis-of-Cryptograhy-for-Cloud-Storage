default:
	emcc aes.c \
		-s WASM=1 \
		-O3 \
		-s "EXPORTED_FUNCTIONS=['_aes_setkey_dec', '_aes_setkey_enc', '_aes_crypt_cbc', '_aes_crypt_ctr']" \
		-o aes.js