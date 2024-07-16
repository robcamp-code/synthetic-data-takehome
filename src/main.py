import random
from hashlib import sha256
from cryptography.fernet import Fernet
import pandas as pd

KEY = Fernet.generate_key()
cipher_suite = Fernet(KEY)

def return_same(x):
    return x


def tokenize_ssn(ssn):
    ssn_int = random.randint(100000000, 999999999)
    ssn_str = str(ssn_int)

    tokenized_ssn = ssn_str[:3] + '-' + ssn_str[3:5] + '-' + ssn_str[5:]
    return tokenized_ssn


def encrypt_tokenize(ssn):
    """ 
    first tokenize the data by replacing ssn with random integers in the correct format
    then encrypt the tokenized SSN
    """
    tokenized = tokenize_ssn(ssn)
    encrypted = encrypt(tokenized)
    return encrypted


def encrypt(data: str) -> str:
    ssn_bytes = str(data).encode('utf-8')
    encrypted_ssn = cipher_suite.encrypt(ssn_bytes)
    return encrypted_ssn.decode('utf-8')



def hash(data: str) -> str:
    sha256_hash = sha256()
    sha256_hash.update(data.encode('utf-8'))
    hashed_string = sha256_hash.hexdigest()
    return hashed_string


def mask_email(data: str) -> str:
    """ replace the data with random codes """
    email_domain = data.split('@')
    email_domain[0] = hash(email_domain[0]) #TODO: use encryption instead
    anonymized_email = "@".join(email_domain)
    return anonymized_email


def replace_last_name_with_initial(last_name: str) -> str:
    """ replace last name with only the first letter """
    return last_name[0]


def pseudo_anonymize_address(address: str) -> str:
    """ 
    ADDRESS:
    pseudo_anonymization, the data is still considered (PII); however, it is 
    accomplished by substituting PII values like name, ID number, or date of birth
    with a random code. Pseudo anonymization is reversable where data masking is not 
      
    But there are numerous other methods of pseudonymization, including the use of: 
    - Cryptographic hash techniques, that arbitrarily input strings to fixed 
    length outputs and then apply them directly to the identifier  
    - Random number generators, that create a random number and then assign it to an identifier
    - Message authentication codes, which are keyed-hash functions that require a secret key to generate the 
    pseudonym for each data field 
    - Monotonic counters, that substitute an identifier with a unique, non-repeating value
    - Encryption, that safeguards identifiers as long as the encryption key remains uncompromised  
    """
    return encrypt(address)


def anonymize_id(student_id: int) -> str:
    """ anonymize the data generate string n in a similar format """
    n_digits = len(str(student_id))
    low_bound = int('1' + '0' * (n_digits - 1))
    upper_bound = int('9' * n_digits)
    new_id = random.randint(low_bound, upper_bound)
    
    return new_id

agg_map = {
    "name": return_same,
    "first_name": return_same, 
    "last_name": replace_last_name_with_initial, 
    "dob": hash, 
    "age": return_same, 
    "email": mask_email,
    "address": pseudo_anonymize_address,
    "ssn": encrypt_tokenize,
    "medical_record_number": encrypt,
    "student_id": anonymize_id,
    "city": return_same,
    "state": return_same,
    "zip": return_same

}


if __name__ == "__main__":
    df = pd.read_csv('./synthetic_data.csv')
    df.drop('Unnamed: 0', axis=1, inplace=True)
    for col in df.columns:
        print(col)
        df[col] = df[col].apply(agg_map[col])
    
    df.to_csv('./final_df.csv')