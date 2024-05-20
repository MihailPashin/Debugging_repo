import pandas as pd

class DataProcessor:
    
    def merge_data(self, result, df):
        merged_df = pd.merge(result, df, left_on='Индекс', right_on=df.index).reset_index(drop=True, inplace=False)
        return merged_df

    def summarize_data(self, merged_df):
        summary = merged_df.groupby(['title', 'Group', 'coord_X', 'coord_Y'], as_index=False).agg(
            numbers_reviews=('Оценка', 'count'),
            averall_ves=('Вес прогноза', 'sum')
        )
        return summary

    def find_duplicates(self, summary):
        duplicates = summary.groupby(['title', 'Group'], as_index=False).agg(
            numbers_reviews=('Group', 'count')
        )
        return duplicates[duplicates['numbers_reviews'] > 1]

    def update_coordinates(self, summary):
        test = summary[summary['title'] == 'Новый город'].groupby(['title']).first(['coord_X', 'coord_Y']).reset_index()
        summary.loc[summary['title'] == 'Новый город', ['coord_X', 'coord_Y']] = test[['coord_X', 'coord_Y']].values
        return summary

    def pivot_data(self, merged_df):
        numbers_plus_minus = merged_df.groupby(['title', 'Group', 'Оценка'], as_index=False).agg(
            numbers_reviews=('Оценка', 'count'),
            averall_ves=('Вес прогноза', 'sum')
        )
        df_transposed = numbers_plus_minus.pivot(index=['title', 'Group'], columns='Оценка', values='numbers_reviews').fillna(0).reset_index()
        df_transposed[['Негативная', 'Нейтральная', 'Положительная']] = df_transposed[['Негативная', 'Нейтральная', 'Положительная']].astype(int)
        return df_transposed

    def update_weights(self, df_transposed, summary):
        update_df_ves = pd.merge(df_transposed, summary, on=['title', 'Group'])
        return update_df_ves

class DataBoundary:
    def __init__(self, controller):
        self.controller = controller

    def validate_and_process(self, result, df):
        print(df.info())
        if 'Индекс' not in result.columns:
            raise ValueError("Первый DataFrame должен содержать столбец 'Индекс'.")
        if not all(col in df.columns for col in ['coord_X', 'coord_Y', 'title']):
            raise ValueError("Второй DataFrame должен содержать столбцы 'coord_X', 'coord_Y', 'title' ")
        return self.controller.process_data(result, df)

class DataController:
    def __init__(self, data_processor):
        self.data_processor = data_processor
        
    def process_data(self, result, df):
        merged_df = self.data_processor.merge_data(result, df)
        summary = self.data_processor.summarize_data(merged_df)

        if not self.data_processor.find_duplicates(summary).empty:
            summary = self.data_processor.update_coordinates(summary)

        summary = summary.groupby(['title', 'Group', 'coord_X', 'coord_Y'], as_index=False).agg(
            numbers_reviews=('averall_ves', 'sum'),
            averall_ves=('numbers_reviews', 'sum')
        )

        df_transposed = self.data_processor.pivot_data(merged_df)
        update_df_ves = self.data_processor.update_weights(df_transposed, summary)

        return update_df_ves
