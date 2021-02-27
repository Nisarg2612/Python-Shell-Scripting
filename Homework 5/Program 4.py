from cryptography.fernet import Fernet

# encryting the below string.
string = "hello everyone"

# the random key fernet generator
key = Fernet.generate_key()

# Instance the Fernet class with the key
f = Fernet(key)

# to encrypt the string string must
# be encoded to byte string before encryption
enc_string = f.encrypt(string.encode())

print("original string: ", string)
print("encrypted string: ", enc_string)

dec_string = f.decrypt(enc_string).decode()

print("decrypted string: ", dec_string)

def encryption(func):

    def str_encrypt(*args, **kwarg):
        enc_string = f.encrypt(string.encode())
        
    return str_encrypt

@ encryption
def dec_str():
    print("original string: ", string)
    print("encrypted string: ", enc_string)

def decryption(fun):

    def str_decrypt(*args, **kwarg):
        dec_string = f.decrypt(enc_string).decode()
    return str_decrypt

@decryption
def dec_destr():
    print("decrypted string: ", dec_string)
