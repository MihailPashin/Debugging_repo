import pandas as pd
from dependency_injector import containers, providers

class Forming_Entity:
    def split_data(self, df):
        home_objects = df[['title']].drop_duplicates().reset_index(drop=True)
        home_objects.index += 1
        home_objects = home_objects.reset_index(level=0).rename(columns={"index": "object_id"})

        point_coordinates = df[['coord_X', 'coord_Y']].drop_duplicates().reset_index(drop=True)
        point_coordinates.index += 1
        point_coordinates = point_coordinates.reset_index(level=0).rename(columns={"index": "id"})

        groups = df[['Group']].drop_duplicates().reset_index(drop=True)
        groups.index += 1
        groups = groups.reset_index(level=0).rename(columns={"index": "group_id"})
        print('len groups', len(groups))
        print('df.info', df.info())
        return home_objects, point_coordinates, groups

    def merge_data(self, home_objects, point_coordinates, df):
        home_objects = pd.merge(home_objects, point_coordinates, left_on='object_id', right_on='id', how='right')
        home_objects = home_objects[['object_id', 'title', 'id']].rename(columns={'id': 'coord_id'})

        raions_id = pd.merge(home_objects, df, on=['title'])
        print('len home_objects', len(home_objects))        
        print('len raions_id', len(raions_id))
        return home_objects, raions_id

    def final_merge(self, groups, raions_id, df):
        final_result = pd.merge(groups, raions_id, on=['Group'])
        final_result = final_result[['group_id', 'object_id', 'svess', 'Негативная', 'Нейтральная', 'Положительная']]
        final_result = final_result.rename(columns={
            'Негативная': 'count_negative_reviews',
            'Нейтральная': 'count_neutral_reviews',
            'Положительная': 'count_positive_reviews',
            'svess': 'x_scaled'
        })
        return final_result

class Forming_Boundary:
    def __init__(self, controller):
        self.controller = controller

    def process_data(self, df):
        self.validate_columns(df, ['title', 'coord_X', 'coord_Y', 'Group', 'svess', 'Негативная', 'Нейтральная', 'Положительная'])
        return self.controller.process_data(df)

    def validate_columns(self, df, required_columns):
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Пропущенные столбцы: {', '.join(missing_columns)}")

class Forming_Control:
    def __init__(self, data_processor):
        self.data_processor = data_processor

    def process_data(self, df):
        home_objects, point_coordinates, groups = self.data_processor.split_data(df)
        home_objects, raions_id = self.data_processor.merge_data(home_objects, point_coordinates, df)
        final_result = self.data_processor.final_merge(groups, raions_id, df)

        home_objects_dict = home_objects.to_dict(orient='records')
        raions_id_dict = raions_id.to_dict(orient='records')
        point_coordinates_dict = point_coordinates.to_dict(orient='records')
        groups_dict = groups.to_dict(orient='records')
        final_result_dict = final_result.to_dict(orient='records')
        print('final_result', len(final_result_dict), 'raions_id_dict', len(raions_id_dict), 'point_coordinates_dict',len(point_coordinates_dict),len(groups_dict), 'groups')
        return [{'final_result': final_result_dict},
            {'coordinates': point_coordinates_dict},
            {'groups': groups_dict},
            {'objects_nedvizhimost': home_objects_dict}]



