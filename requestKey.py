from dotenv import load_dotenv
import requests, os
    
# Load environment variables from .env file
load_dotenv()

# Define variables for the endpoint from .env
KME_hostname = os.getenv("KME_HOSTNAME")
Slave_SAE_id = os.getenv("SLAVE_SAE_ID")
Master_SAE_id = os.getenv("MASTER_SAE_ID")
    

class CipherObject:

    
    # Constructor that calls the necessary functions
    def __init__(self):

        self.status = self.get_status()
        self.quantum_key = self.get_enc_key() 

    # 1. Get status
    def get_status(self):

        # The 'f' define that we can pass a f_string inside the path
        url = f"{KME_hostname}/api/v1/keys/{Slave_SAE_id}/status"
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            print("Status:", response.json())
            return response.json()
        else:
            print("Failed to get status, status code:", response.status_code)
            return None

    # 2. Get key
    def get_enc_key(self):

        url = f"{KME_hostname}/api/v1/keys/{Slave_SAE_id}/enc_keys"
        response = requests.post(url)

        if response.status_code == 200:

            #Extract the key frome response
            key_data = response.json()

            # Convert the hex key to bytes
            enc_key = bytes.fromhex(key_data['enc_key'])

            print("Encryption Key received:", enc_key.hex())
            return enc_key
        
        else:
            print("Failed to retrieve encryption key, status code:", response.status_code)
            return None

    # 3. Get key with key IDs
    def get_dec_keys(key_ids):
        url = f"{KME_hostname}/api/v1/keys/{Master_SAE_id}/dec_keys"
        response = requests.post(url, json={"key_ids": key_ids})
        if response.status_code == 200:
            dec_keys = response.json()["dec_keys"]
            print("Decryption Keys received:", dec_keys)
            return dec_keys
        else:
            print("Failed to retrieve decryption keys, status code:", response.status_code)
            return None

