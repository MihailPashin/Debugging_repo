from dependency_injector import containers, providers
from Packages.Loading_DataSet.Pandas_ECB_df import DataFrameEntity,DataFrameBoundary,DataFrameControl
import os


class Pandas_Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    name_of_file='New_coordinates_titles.csv'
    current_dir = os.path.dirname(__file__)
    relative_path = os.path.join(current_dir, '..', 'Packages','Loading_Dataset', 'data', name_of_file)
    config.filepath.from_value(relative_path)
    
    entity = providers.Factory(DataFrameEntity, filepath=config.filepath)
    control = providers.Factory(DataFrameControl, dataframe_entity=entity)
    boundary = providers.Factory(DataFrameBoundary, dataframe_control=control)
