from dependency_injector import containers, providers
from Packages.Loading_DataSet.Pandas_ECB_df import DataFrameEntity,DataFrameBoundary,DataFrameControl
import os

relative_path = '/app/Packages/Loading_DataSet/data/New_coordinates_titles.csv'
absolute_path = os.path.abspath(os.path.join(os.getcwd(), relative_path))
directory_path = '/app/Packages/Loading_DataSet/data/'
class Pandas_Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    print(os.getcwd())

    current_dir = os.path.dirname(__file__)
    relative_path = os.path.join(current_dir, 'Packages','Loading_Dataset' 'data', 'New_coordinates_titles.csv')
    config.filepath.from_value(relative_path)
    
    entity = providers.Factory(DataFrameEntity, filepath=config.filepath)
    control = providers.Factory(DataFrameControl, dataframe_entity=entity)
    boundary = providers.Factory(DataFrameBoundary, dataframe_control=control)
