from dependency_injector import containers, providers
from Packages.XLM_RoBERTa.Sentiment_Analysis_ECB import SentimentModel_Entity,SentimentModel_Boundary,SentimentModel_Control

class SentimentModel_Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.model_name.from_value("sismetanin/xlm_roberta_base-ru-sentiment-rureviews")
    
    entity = providers.Factory(SentimentModel_Entity, model_name=config.model_name)
    control = providers.Factory(SentimentModel_Control, sentiment_model=entity)
    boundary = providers.Factory(SentimentModel_Boundary, sentiment_control=control)
