from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from dotenv import load_dotenv
from requestKey import CipherObject
import os

# Fuction to delete files if there exist
def delete_files(files):

    for file in files:
        if os.path.exists(file):
            os.remove(file)
            print(f"Deleted existing file: {file}")

# Function to encrypt the file.txt and exported as encrypted file using AES-256-CBC algorithm
def encrypt_file(file_to_encrypt, encrypted_file, key, iv):

    print("\nHello! Let's encrypt a file with AES algorithm : \nencrypting...")
    
    try:

        # Create an AES cipher object with the key and IV
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # Read the file.txt
        with open(file_to_encrypt, 'rb') as f_in:
            plaintext = f_in.read()

        # Pad the plaintext to be a multiple of the block size (16 bytes)
        padded_plaintext = pad(plaintext, AES.block_size)

        # Encrypt the plaintext
        ciphertext = cipher.encrypt(padded_plaintext)

        # Write the IV and ciphertext to the encrypted file
        with open(encrypted_file, 'wb') as f_out:
            f_out.write(iv + ciphertext)
        
        # Read the content of encrypted file
        with open(encrypted_file, 'rb') as f_out:
            x = f_out.read()

        print("well done! you encrypted the file '" + file_to_encrypt + "'. Let's see what suppose to read there...\n")
        print(x)
        print("\nCheck inside folder 'QKD-encryption' and locate the file '" + encrypted_file +"'\n")
    
    except Exception as e:

        print(f"Ooops, an error occurred inside 'encrypt_file' function: {e}")


def decrypt_file(encrypted_file, decrypted_file, key):

    try:
        # Read the IV and ciphertext from the encrypted file
        with open(encrypted_file, 'rb') as f_in:
            iv = f_in.read(16)  # The first 16 bytes are the IV
            ciphertext = f_in.read()  # The rest is the ciphertext

        # Create an AES cipher object with the same key and IV
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # Decrypt the ciphertext
        padded_plaintext = cipher.decrypt(ciphertext)

        # Unpad the plaintext
        plaintext = unpad(padded_plaintext, AES.block_size)

        # Write the plaintext to the decrypted file
        with open(decrypted_file, 'wb') as f_out:
            f_out.write(plaintext)

        print(f"Decryption successful! The file '{decrypted_file}' has been created.\n")
    
    except Exception as e:
        print(f"Oops, an error occurred during decryption: {e}")


def main():

    # call class CipherObject from requestKey.py
    cipherobject = CipherObject()

    # Load environment variables from the .env file
    load_dotenv()

    # 'key' is the 256-bit quantum key received from the QKD device
    # Request the quantum key
    key = cipherobject.quantum_key

    # Generate a random initialization vector (IV)
    iv = os.urandom(16)
        
    input_file = 'file.txt'
    output_file = 'file_encrypted.bin'
    decrypted_file = 'file_decrypted.txt'

    try:

        # Check and delete existing files (only the encrypted and decrypted files)
        delete_files([output_file, decrypted_file])

        # Call function "encrypt_file"
        encrypt_file(input_file, output_file, key, iv)

        # Call function "decrypt_file"
        decrypt_file(output_file, decrypted_file, key)

    except Exception as e:

        print(f"Ooops, an error occurred when you try to call 'encrypt_file' function: {e}")


if __name__ == "__main__":
    main()


