"""
Script that re-runs data collection in case of errors.
"""

import character_collection as dc
from multiprocessing import Process


# Collect data from the character API.
def collect_char_data():
    start_page = 0
    last_page = 76502 # dc.find_last_page()
    while start_page < last_page:
        start_page = dc.collect_data(start_page, last_page)
        print("Error occurred on page %s. Restarting character data collection." % start_page)
    print("Character collection data completed.")
    return


def main():
    collect_char_data()
    print("Data collection complete.")
    return


if __name__ == '__main__':
    main()
