"""
Creating 13 Deep Learning models that predict the run time of a Mythic+ Team given the scores/roles of the five players,
the dungeon, and the level of the key. There is one model for each dungeon.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from multiprocessing import Pool


# Normalize the input variables
def normalize_inputs(x_input):
    x_input = x_input.values.reshape(-1, 1)
    scaler = StandardScaler()
    x_input = scaler.fit_transform(x_input)
    return x_input


# Train a single machine learning algorithm
def train_validate_run_time_model(dungeon):
    # Read the input variables from the csv and then normalize them.
    data_df = pd.read_csv('data//{d}//{d}_key_time.csv'.format(d=dungeon))
    for col in data_df.drop('run_time', axis=1).columns:
        data_df[col] = normalize_inputs(data_df[col])
    x_train, x_test, y_train, y_test = train_test_split(data_df.drop('run_time', axis=1),
                                                        data_df['run_time'],
                                                        test_size=0.3)

    # Initialize and train the model.
    model = MLPRegressor(hidden_layer_sizes=(3, 2),
                         activation='tanh',
                         solver='adam',
                         max_iter=1000,
                         early_stopping=True,
                         batch_size=200)
    model.fit(x_train, y_train)
    model_performance = model.score(x_test, y_test)

    print("%s Model Trained. R2: %.3f" % (dungeon, model_performance))
    return


def main():
    np.random.seed(42)

    # Create a list of dungeons from the text file.
    file_path = 'data\\dungeon_list.txt'
    file = open(file_path, 'rU')
    dungeon_list = [x for x in str(file.read()).split()]
    file.close()

    # Create a queue for training the models in parallel.
    p = Pool(6)
    p.map(train_validate_run_time_model, [x for x in dungeon_list])
    print("All models trained!")

    return


if __name__ == '__main__':
    main()
