from dependency_injector import containers, providers
from Packages.Topics.ECB_control_themes import Group,GroupInterface,GroupControl
from Packages.Topics.topics_themes import dict_for_razmetka

class Topic_Container(containers.DeclarativeContainer):
    
    topics_data = providers.Object(dict_for_razmetka)
    control = providers.Factory(GroupControl, data=topics_data)
    boundary = providers.Factory(GroupInterface, group_control=control)
