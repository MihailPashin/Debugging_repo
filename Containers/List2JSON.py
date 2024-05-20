from dependency_injector import containers, providers
from Packages.Nested_List_to_JSON.save_to_json import NestedListToJSON



class Save2JSON_Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    init_convert = providers.Factory(NestedListToJSON, nested_list=config.nested_list)
