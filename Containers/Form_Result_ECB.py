from dependency_injector import containers, providers
from Packages.Getting_Final_DFs.Form_Result_ECB import Forming_Entity,Forming_Boundary,Forming_Control

class Split_DF_Container(containers.DeclarativeContainer):
    
    entity = providers.Factory(Forming_Entity)
    controller = providers.Factory(Forming_Control, data_processor=entity)
    boundary = providers.Factory(Forming_Boundary, controller=controller)
