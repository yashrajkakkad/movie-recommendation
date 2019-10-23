import os
import pandas as pd
import numpy as np
import datetime
from collections import Counter
from sklearn.metrics.pairwise import cosine_similarity

DATASET_DIR = 'ml-latest-small'

genome_scores_data = pd.read_csv(os.path.join(DATASET_DIR, 'genome-scores.csv'))
movies_data = pd.read_csv(os.path.join(DATASET_DIR, 'movies.csv'))
ratings_data = pd.read_csv(os.path.join(DATASET_DIR, 'ratings.csv'))

genome_scores_data.head()
