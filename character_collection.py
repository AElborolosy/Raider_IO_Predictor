"""
Script that collects data on characters off the Raider.IO API and stores them int a csv.
"""


# Import Libraries.
import pandas as pd
import urllib.request as url
import time


# Function for finding the last page in the API. Needed so wrappers can access this information.
def find_last_page():
    data = load_char_info(0)
    return data['rankings']['ui']['lastPage']


# Given a page number, stores the raider.io data into a dataframe.
def load_char_info(page):

    page_url = 'https://raider.io/api/mythic-plus/rankings/characters?region=us&season=season-7.3.2&' \
               'class=all&role=all&page={pg}'.format(pg=page)

    req = url.Request(page_url, headers={'User-Agent': "Magic Browser"})
    info = url.urlopen(req)
    data = pd.read_json(info, orient='columns')
    return data


def collect_data(current_page, last_page):
    page = 0  # If no current page is given, start at 0.
    for page in range(current_page, last_page + 1):

        # Load a page of data and initialize/reset the DF holding the data.
        # If an error occurs, break from the for loop and return the page.
        time.sleep(0.25)
        try:
            data = load_char_info(page)
        except url.HTTPError:
            break
        print("Loaded character page %s." % page)

        # Append to DF one page of data.
        char_info = pd.DataFrame(columns=["ID", "Score"])
        num_characters = len(data['rankings']['rankedCharacters'])
        for character in range(num_characters):
            char_id = data['rankings']['rankedCharacters'][character]['character']['id']
            score = data['rankings']['rankedCharacters'][character]['score']
            char_info.loc[character] = [char_id, score]

        # Write a page of character data to the csv.
        char_info.to_csv('data\\char_info.csv', header=None, index=False, mode="a")

    return page
