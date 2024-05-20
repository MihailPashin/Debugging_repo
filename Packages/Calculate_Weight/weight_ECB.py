import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

class DataNormalizer:
    def __init__(self, scaler):
        self.scaler = scaler

    def normalize(self, data):
        x = data['averall_ves'].values.reshape(-1, 1)
        df_sr = self.scaler.fit_transform(x)
        df_sr = np.around(df_sr).astype(int)
        return df_sr

    def adjust_scores(self, data, normalized_values):
        difference_positiv_vs_neg = data['Положительная'].values.reshape(-1, 1) - data['Негативная'].values.reshape(-1, 1)
        difference_positiv_vs_neutr = data['Положительная'].values.reshape(-1, 1) - data['Нейтральная'].values.reshape(-1, 1)

        unique_indices = list(np.unique(np.where(difference_positiv_vs_neg >= 2)[0]))
        unique_indices_than_neutral = list(np.unique(np.where(difference_positiv_vs_neutr > 1)[0]))

        data['svess'] = normalized_values
        data.loc[data.index.isin(unique_indices), 'svess'] += 3
        data.loc[data.index.isin(unique_indices_than_neutral), 'svess'] += 1
        data['svess'] = data['svess'].clip(upper=10).astype(int)
        
        return data

class DataController:
    def __init__(self, data_normalizer):
        self.data_normalizer = data_normalizer

    def process_data(self, df):
        update_df_ves = df.copy()
        for segment, data in update_df_ves.groupby('Group'):
            print('segment', segment)
            normalized_values = self.data_normalizer.normalize(data)
            adjusted_data = self.data_normalizer.adjust_scores(data, normalized_values)
            df.loc[data.index, 'svess'] = adjusted_data['svess']
        return df

class DataBoundary:
    def __init__(self, controller):
        self.controller = controller

    def process_grading(self, df):
        required_columns = ['averall_ves', 'Положительная', 'Негативная', 'Нейтральная', 'Group']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Datframe должен содержать столбцы: {required_columns}")
        return self.controller.process_data(df)

