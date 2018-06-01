"""
Script that re-runs data collection in case of errors.
"""

import character_collection as dc
import keystone_collection as kc
from multiprocessing import Process


# Collect data from the character API.
def collect_char_data():
    start_page = 0
    last_page = dc.find_last_page()
    while start_page < last_page:
        start_page = dc.collect_data(start_page, last_page)
        print("Error occurred on page %s. Restarting character data collection." % start_page)

    print("Character collection data completed.")
    return


# Collect data from the keystone run API.
def collect_keystone_data():
    start_page = 7266
    last_page = kc.find_last_page()
    while start_page < last_page:
        start_page = kc.collect_data(start_page, last_page)
        print("Error occurred on page %s. Restarting keystone run data collection." % start_page)

    print("Keystone run collection data completed.")
    return


def main():

    # Process(target=collect_keystone_data).start()
    # Process(target=collect_char_data).start()

    collect_keystone_data()
    print("Data collection complete.")
    return


if __name__ == '__main__':
    main()
