from dependency_injector import containers, providers
from Packages.RuBERT.RuBERT_ECB import RuBERT_Entity,RuBERT_Boundary, RuBERT_Control

class RuBERT_Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.model_path.from_value("sergeyzh/rubert-mini-sts")

    entity = providers.Factory(RuBERT_Entity, model_path=config.model_path)
    control = providers.Factory(RuBERT_Control, rubert_entity=entity)
    boundary = providers.Factory(RuBERT_Boundary, rubert_control=control)
