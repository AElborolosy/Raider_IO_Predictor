"""
Split the data into 26 files, two for each of the 13 instances (two files for the two ML Algorithms in our pipeline).
"""

import pandas as pd
import os


# Split the df into two, one for each ML algorithm.
def split_data_sets(df):

    # Dictionary based on scores written in Raider.IO core.lua file.
    key_score = {2: 20, 3: 30, 4: 40, 5: 50, 6: 60, 7: 70, 8: 80, 9: 90, 10: 100, 11: 110, 12: 121, 13: 133, 14: 146,
                 15.0: 161, 16: 177, 17: 195, 18: 214, 19: 236, 20: 259, 21: 285, 22: 314, 23: 345, 24: 380, 25: 419,
                 26: 459, 27: 505, 28.0: 556, 29: 612, 30: 673}

    # Convert run_time from MS to Minutes.
    df['run_time'] = df['run_time']/60000
    run_time_df = df[['run_time', 'key_level', 'tank_score', 'dps1_score', 'dps2_score', 'dps3_score', 'healer_score']]

    # Alter the key_level column to the base score found in the key_score dict.
    df.key_level.replace(to_replace=key_score.keys(), value=key_score.values(), inplace=True)
    run_score_df = pd.DataFrame(df['run_time'])
    run_score_df['run_score'] = df['run_score'] - df['key_level']
    return run_score_df, run_time_df


def main():

    raw_data = pd.read_csv('data\\joined_data_with_level.csv')

    for dungeon in raw_data.dungeon_name.unique():
        # If necessary, create the directory for the data.
        try:
            os.mkdir('data\\{d}'.format(d=dungeon))
        except OSError:
            print("{d} Directory already exists.".format(d=dungeon))

        # Filter the data for the specific dungeon. Drop the dungeon_name column and save the result to a csv.
        temp_df = raw_data.mask(cond=raw_data['dungeon_name'] != '{d}'.format(d=dungeon))
        temp_df.dropna(inplace=True)
        temp_df.drop(['dungeon_name'], axis=1, inplace=True)

        # Split data set into two csv files before saving them.
        adj_score_df, key_time_df = split_data_sets(temp_df)
        adj_score_df.to_csv('data\\{d}\\{d}_adj_score.csv'.format(d=dungeon), index=False)
        key_time_df.to_csv('data\\{d}\\{d}_key_time.csv'.format(d=dungeon), index=False)

        print("Created csv files for %s." % dungeon)

    return


if __name__ == '__main__':
    main()
