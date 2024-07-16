""" 
generate.py 
utility functions for generating a synthetic dataset
"""

import random
from datetime import datetime, timedelta

import pandas as pd
import pydbgen
from pydbgen import pydbgen
from random_address import real_random_address


possible_ids = range(1_000_000, 9_999_999)
col_names = ["first_name", "last_name", "name", "dob", "age", "email", "ssn", "medical_record_number", "student_id"]

def get_first_name(name: str) -> str:
    names = name.split(" ")
    names.pop(-1)
    return " ".join(names)


def get_last_name(name: str) -> str:
    names = name.split(" ")
    return names.pop(-1)


def generate_dob(start_year=1950, end_year=2000):
    """
    Generates a random date between January 1, 1950, and December 31, 2000.
    :param start_year: The start year for the date range (inclusive)
    :param end_year: The end year for the date range (inclusive)
    :return: A random date as a string in the format YYYY-MM-DD
    """
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    
    random_date = start_date + timedelta(days=random_days)
    
    return random_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')


def generate_medical_number(x):
    n_digits = 7
    low_bound = int('1' + '0' * (n_digits - 1))
    upper_bound = int('9' * n_digits)
    return str(random.randint(low_bound, upper_bound))


def generate_student_id(x) -> int:
    sample = random.sample(possible_ids, 1)
    return sample[0]


def generate_age(x) -> int:
    return random.randint(18, 70)


def get_location(row):
    addr = real_random_address()
    state = addr["state"]
    address = addr['address1']
    city, zip = None, None

    try: city = addr["city"] 
    except Exception as e: print(e)
    
    try: zip = addr["postalCode"] 
    except Exception as e: print(e)
    
    return pd.Series([address, city, state, zip], index=["address", "city", "state", "zip"])


def generate_syntetic_data():
    src_db = pydbgen.pydb()
    pydb_df = src_db.gen_dataframe(1000, fields=col_names, phone_simple=True)
    pydb_df.head()
    pydb_df["dob"] = pydb_df["dob"].apply(lambda x: generate_dob())
    
    pydb_df["student_id"] = pydb_df["student_id"].apply(generate_student_id)
    loc_info = pydb_df.apply(get_location, result_type='expand', axis=1)
    pydb_df = pd.concat([pydb_df, loc_info], axis=1)

    pydb_df["first_name"] = pydb_df["name"].apply(get_first_name)
    pydb_df["last_name"] = pydb_df["name"].apply(get_last_name)
    pydb_df["medical_record_number"] = pydb_df["medical_record_number"].apply(generate_medical_number)
    
    pydb_df.to_csv('./synthetic_data.csv')


if __name__ == "__main__":
    generate_syntetic_data()