from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
def encryptAesEcb(plaintext, key):
    aes = AES.new(key, AES.MODE_ECB)
    padded_data = pad(plaintext, AES.block_size)
    ciphertext = aes.encrypt(padded_data)
    encoded_ciphertext = base64.b64encode(ciphertext).decode('utf-8')
    return encoded_ciphertext

def decryptAesEcb(ciphertext, key):
    aes = AES.new(key, AES.MODE_ECB)
    encrypted_data = base64.b64decode(ciphertext)
    decrypted_data = aes.decrypt(encrypted_data)
    unpadded_data = unpad(decrypted_data, AES.block_size)
    return unpadded_data.decode("utf-8")