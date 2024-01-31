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
            self.encrypted_data += str(hex(double_encrypted_rod)) + 'X'

        self.encrypted_data += str(hex(total_key)) + 'X' + str(hex(self.random_key))
        return self.encrypted_data


class CustomDecryption:
    def __init__(self):
        self.data_list = []
        self.decrypted_data = ''

    def perform_decryption(self, encrypted_data, key):
        self.decrypted_data = ''
        self.data_list = encrypted_data.split('X')
        key_list = self.data_list[-2:]

        if len(key_list) < 2 or not all(key_list):
            return "Invalid encrypted data format. Cannot decrypt."

        try:
            total_key = int(key_list[0], 16)
            r_key = int(key_list[1], 16)
        except ValueError:
            return "Invalid encrypted data format. Cannot decrypt."

        for i in range(len(self.data_list) - 2):
            try:
                d_decrypt = int(self.data_list[i], 16) ^ r_key
                decrypted_int = d_decrypt ^ total_key
                self.decrypted_data += chr(decrypted_int)
            except ValueError:
                return "Invalid encrypted data format. Cannot decrypt."

        return self.decrypted_data


if __name__ == "__main__":
    text_to_encrypt = "HelloWorld"
    key_to_use = "minsatt"

    custom_encryptor = CustomEncryption()
    encrypted_text = custom_encryptor.perform_encryption(text_to_encrypt, key_to_use)
    print("Encrypted data:", encrypted_text)

    custom_decryptor = CustomDecryption()
    decrypted_text = custom_decryptor.perform_decryption(encrypted_text, key_to_use)
    print("Decrypted data:", decrypted_text)
