Crypted = "9153787770964"

def caesar_decrypt(crypted_str):
    decrypted_str = ''
    for i in range(0, len(crypted_str)):
        decrypted_str += str((int(crypted_str[i]) + 4) % 10)
    return decrypted_str
decrypt=caesar_decrypt(Crypted)
print(f"{decrypt[0:2]}°{decrypt[2:4]}'{decrypt[4:7]}.{decrypt[7]}\"N, {decrypt[8]}°{decrypt[8:10]}'{decrypt[10:12]}.{decrypt[12]}\"W")
