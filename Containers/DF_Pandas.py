from dependency_injector import containers, providers
from Packages.Loading_DataSet.Pandas_ECB_df import DataFrameEntity,DataFrameBoundary,DataFrameControl

class Pandas_Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.filepath.from_value('Packages/Loading_DataSet/data/New_coordinates_titles.csv')
    
    entity = providers.Factory(DataFrameEntity, filepath=config.filepath)
    control = providers.Factory(DataFrameControl, dataframe_entity=entity)
    boundary = providers.Factory(DataFrameBoundary, dataframe_control=control)
