"""
Script that collects data on characters off from the Raider.io API
Data is stored on the MySQL localhost DB
"""


# Import Libraries.
import pandas as pd
import time
import requests
from sqlalchemy import create_engine
from pandas.io.json import json_normalize


# DEPRECIATED DUE TO CHANGES IN load_char_info!
# Function for finding the last page in the API. Needed so wrappers can access this information.
def find_last_page():
    data = load_char_info(0)
    return data['rankings']['ui']['lastPage']


# Given a page number, stores the raider.io data into a dataframe.
def load_char_info(page):

    page_url = 'https://raider.io/api/mythic-plus/rankings/characters?region=us&season=season-7.3.2&' \
               'class=all&role=all&page={pg}'.format(pg=page)

    r = requests.get(page_url)
    parsed_r  = r.json()
    result = json_normalize(parsed_r['rankings']['rankedCharacters'], errors='ignore')

    # Cannot store lists into MySQL so we convert the runs column into a list
    result['runs']  = result['runs'].astype('str')
    return result


def upload_data_to_db(df, table):
    engine = create_engine('mysql+mysqlconnector://agent15:bot@localhost/raider_io')
    connection = engine.connect()

    # Use a temp table to handle duplicates
    df.to_sql(name='temp_table', con=engine, if_exists='replace', index=False)

    # Insert into primary table while ignoring duplicates
    connection = engine.connect()
    connection.execute("INSERT IGNORE INTO {tbl} SELECT * FROM temp_table".format(tbl=table))
    connection.close()
    return


def collect_data(current_page, last_page):
    for page in range(current_page, last_page + 1):

        # Load a page of data and initialize/reset the DF holding the data.
        # If an error occurs, break from the for loop and return the page.
        time.sleep(0.25)
        try:
            data = load_char_info(page)
            print("Loaded character page %s at %s." % (page, time.ctime()))
            upload_data_to_db(data, 'character_info')
        except:
            break
    return page
