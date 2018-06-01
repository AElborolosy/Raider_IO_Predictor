"""
Script that trains two sets of 13 Machine Learning Algorithms.
Set 1: Predicts performance score (score - base score for that keystone) based on run time.
Set 2: Predicts run time based on key level and total score of the five players.
"""

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
from multiprocessing import Pool
import numpy as np
import pandas as pd
import pickle


# Train a single machine learning algorithm.
def train_validate_adj_score_model(dungeon):
    df = pd.read_csv('data//{d}//{d}_adj_score.csv'.format(d=dungeon))
    x_train, x_test, y_train, y_test = train_test_split(df.drop('run_score', axis=1),
                                                        df['run_score'],
                                                        test_size=0.3,
                                                        random_state=42)

    # Initialize and train the model.
    model = LinearRegression()
    model.fit(x_train, y_train)

    # Quantitatively validate the model using the r2_score.
    predictions = model.predict(x_test)
    performance = r2_score(y_test, predictions)
    print("%s Model Trained! R2: %.3f" % (dungeon, performance))

    # Visually validate the model using a plot of y_test vs predictions.
    ideal_line = np.arange(min(y_test), max(y_test), step=1)
    plt.plot(ideal_line, ideal_line, '-')
    plt.plot(y_test, predictions, '.')
    plt.title('%s Adj Score Model\nR2: %.3f' % (dungeon, performance))
    plt.xlabel('Actual Score')
    plt.ylabel('Predicted Score')
    plt.savefig('data\\{d}\\{d}_adj_score_visual.png'.format(d=dungeon))

    # Store model in pickle file for later usage.
    pickle.dump(model, open('data\\{d}\\{d}_adj_score_model.pickle'.format(d=dungeon), 'wb'))
    return


def main():
    # Create a list of dungeons from the text file.
    file_path = 'data\\dungeon_list.txt'
    file = open(file_path, 'rU')
    dungeon_list = [x for x in str(file.read()).split()]
    file.close()

    # Create a queue for training the models in parallel.
    p = Pool(6)
    p.map(train_validate_adj_score_model, [x for x in dungeon_list])
    print("All models trained!")
    return


if __name__ == '__main__':
    main()
