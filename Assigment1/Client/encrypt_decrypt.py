import random


class CustomEncryption():
    def __init__(self):
        self.encrypted_data = ''
        self.random_key = random.randint(1, 65536)

    def perform_encryption(self, text, key):
        self.encrypted_data = ''
        total_key = 0
        for i in key:
            total_key += ord(i)

        key = int(bin(total_key)[2:])

        for i in text:
            encrypted_ord = ord(i) ^ total_key
            double_encrypted_rod = encrypted_ord ^ self.random_key
            print(double_encrypted_rod)

            self.encrypted_data += str(hex(double_encrypted_rod)) + 'X'
        self.encrypted_data += str(hex(total_key)) + 'X' + str(hex(self.random_key))
        print(self.encrypted_data)

        return self.encrypted_data


class CustomDecryption():

    def __init__(self):
        self.data_list: list = []
        self.decrypted_data: str = ''

    def perform_decryption(self, encrypted_data: str, key):
        self.decrypted_data = ''
        self.data_list = encrypted_data.split('X')
        key_list = self.data_list[-2:]
        total_key = int(key_list[0], 16)
        r_key = int(key_list[1], 16)
        print("user key:", total_key, ": random key:", r_key)

        for i in range(len(self.data_list) - 2):
            d_decrypt = int(self.data_list[i], 16) ^ r_key

            decrypted_int = d_decrypt ^ total_key
            self.decrypted_data += chr(decrypted_int)

        return self.decrypted_data


if __name__ == "__main__":
    custom_encryption = CustomEncryption()
    custom_decryption = CustomDecryption()

    text_to_encrypt = "HelloWorld"
    key_to_encrypt = "minsatt"

    encrypted_data: str = custom_encryption.perform_encryption(text_to_encrypt, key_to_encrypt)
    decrypted_data: str = custom_decryption.perform_decryption(encrypted_data, key_to_encrypt)

    print("Decrypted data:", decrypted_data)
