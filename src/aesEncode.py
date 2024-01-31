# 报错 SystemError: PY_SSIZE_T_CLEAN macro must be defined for '#' formats
# 这个问题可能是由于 pycryptodome 库与 Python 版本不兼容导致的。
# 此问题出现在Docker容器中，使用 Python 3.11.7 版本会出现，以上情况安装 pycryptodomex 库，改为 from Cryptodome.Cipher import AES
# from Cryptodome.Cipher import AES

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