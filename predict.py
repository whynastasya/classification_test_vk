# -*- coding: utf-8 -*-
"""Untitled7.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1wNW9Xh1ZCLUFUl_J2sjoIWtVFK0nt4a5
"""

import pandas as pd
import json
import numpy as np
from xgboost import XGBClassifier
import joblib

def generate_features(df):
    df['values'] = df['values'].apply(lambda x: np.array(json.loads(x)) if isinstance(x, str) else x)
    df['mean'] = df['values'].apply(np.mean)
    df['std'] = df['values'].apply(np.std)
    df['median'] = df['values'].apply(np.median)
    df['min'] = df['values'].apply(np.min)
    df['max'] = df['values'].apply(np.max)
    return df[['mean', 'std', 'median', 'min', 'max', 'id']]

def make_predictions(test_data_path, model_path, submission_path):
    test_data = pd.read_parquet(test_data_path)
    test_features = generate_features(test_data)

    model = joblib.load(model_path)
    test_predictions = model.predict_proba(test_features[['mean', 'std', 'median', 'min', 'max']])[:, 1]

    submission = pd.DataFrame({'id': test_features['id'], 'score': test_predictions})
    submission.to_csv(submission_path, index=False)

if __name__ == "__main__":
    make_predictions('data/test.parquet', 'data/best_model.pkl', 'submission.csv')
