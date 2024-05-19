from dependency_injector import containers, providers
from Packages.Loading_DataSet.Pandas_ECB_df import DataFrameEntity,DataFrameBoundary,DataFrameControl
import os


class Pandas_Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    current_dir = os.path.dirname(__file__)
    relative_path = os.path.join(current_dir, '..', 'Packages', 'Loading_DataSet', 'data', 'New_coordinates_titles.csv')
    print('path new ',relative_path)
    config.filepath.from_value(relative_path)
    
    entity = providers.Factory(DataFrameEntity, filepath=config.filepath)
    control = providers.Factory(DataFrameControl, dataframe_entity=entity)
    boundary = providers.Factory(DataFrameBoundary, dataframe_control=control)
