from dependency_injector import containers, providers
from Packages.Preparing_Tables.Grouping_Summary import DataProcessor,DataBoundary,DataController

class DataPostProcess_Container(containers.DeclarativeContainer):
    
    entity = providers.Factory(DataProcessor)
    control = providers.Factory(DataController, data_processor=entity)
    boundary = providers.Factory(DataBoundary, controller=control)
