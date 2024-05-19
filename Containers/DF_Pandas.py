from dependency_injector import containers, providers
from Packages.Loading_DataSet.Pandas_ECB_df import DataFrameEntity,DataFrameBoundary,DataFrameControl
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Packages','Loading_DataSet')))

class Pandas_Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.filepath.from_value('data/New_coordinates_titles.csv')
    
    entity = providers.Factory(DataFrameEntity, filepath=config.filepath)
    control = providers.Factory(DataFrameControl, dataframe_entity=entity)
    boundary = providers.Factory(DataFrameBoundary, dataframe_control=control)
