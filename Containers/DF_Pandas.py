from dependency_injector import containers, providers
from Packages.Loading_DataSet.Pandas_ECB_df import DataFrameEntity,DataFrameBoundary,DataFrameControl
import os

file_relative_path = os.path.join(os.path.dirname(__file__), '..', 'Packages', 'Loading_DataSet', 'data', 'New_coordinates_titles.csv')
absolute_file_path = os.path.abspath(file_relative_path)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class Pandas_Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.filepath.from_value(absolute_file_path)
    
    entity = providers.Factory(DataFrameEntity, filepath=config.filepath)
    control = providers.Factory(DataFrameControl, dataframe_entity=entity)
    boundary = providers.Factory(DataFrameBoundary, dataframe_control=control)
