package main

import (
    "bytes"
    "crypto/aes"
    "crypto/cipher"
    "encoding/base64"
    "encoding/hex"
    "syscall/js"
    "errors"
    "strings"
)

var key, _ = hex.DecodeString("603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4");
var iv, _ = hex.DecodeString("feffe9928665731c6d6a8f9467308308")

func addBase64Padding(value string) string {
    m := len(value) % 4
    if m != 0 {
        value += strings.Repeat("=", 4-m)
    }

    return value
}

func removeBase64Padding(value string) string {
    return strings.Replace(value, "=", "", -1)
}

func Pad(src []byte) []byte {
    padding := aes.BlockSize - len(src)%aes.BlockSize
    padtext := bytes.Repeat([]byte{byte(padding)}, padding)
    return append(src, padtext...)
}

func Unpad(src []byte) ([]byte, error) {
    length := len(src)
    unpadding := int(src[length-1])

    if unpadding > length {
        return nil, errors.New("unpad error. This could happen when incorrect encryption key is used")
    }

    return src[:(length - unpadding)], nil
}

func encrypt(this js.Value, i []js.Value) interface{} {
    block, err := aes.NewCipher(key)
    if err != nil {
       return ""
    }

    msg := Pad([]byte(i[0].String()))
    ciphertext := make([]byte, aes.BlockSize+len(msg))
    copy(ciphertext, iv)

    cfb := cipher.NewCBCEncrypter(block, iv)
    cfb.CryptBlocks(ciphertext[aes.BlockSize:], []byte(msg))
    finalMsg := removeBase64Padding(base64.URLEncoding.EncodeToString(ciphertext))
    //println(finalMsg)
    return finalMsg
}

func decrypt(this js.Value, i []js.Value) interface{} {
    block, err := aes.NewCipher(key)
    if err != nil {
        return ""
    }

    decodedMsg, err := base64.URLEncoding.DecodeString(addBase64Padding(i[0].String()))
    if err != nil {
        return ""
    }

    if (len(decodedMsg) % aes.BlockSize) != 0 {
        return ""
    }

    mIV := decodedMsg[:aes.BlockSize]
    msg := decodedMsg[aes.BlockSize:]

    cfb := cipher.NewCBCDecrypter(block, mIV)
    cfb.CryptBlocks(msg, msg)

    unpadMsg, err := Unpad(msg)
    if err != nil {
        return ""
    }

    println(string(unpadMsg))
    return string(unpadMsg)
}

func registerCallbacks() {
    js.Global().Set("encrypt", js.FuncOf(encrypt))
    js.Global().Set("decrypt", js.FuncOf(decrypt))
}

func main() {
	c := make(chan struct{}, 0)

	println("Go Assembly Running...")
	registerCallbacks()
    <-c
}
