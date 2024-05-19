from Containers.Topic_Checker import Topic_Container
from Containers.DF_Pandas import Pandas_Container
from Containers.Yake import Yake_Container
from Containers.RuBERT import RuBERT_Container
from Containers.XLM_RoBERTa import SentimentModel_Container
#from Containers.List2JSON import Save2JSON_Container
#from Containers.DataPostProcessing import DataPostProcess_Container
#from Containers.Normalize_Weigth import NormalizerWeight_Container
#from Containers.Form_Result_ECB import Split_DF_Container
import pandas as pd

if __name__ == "__main__" :
   
    topic_boundary = Topic_Container().boundary()
    topics=topic_boundary.check_groups_and_save() ## Отобразил и вернул все тематики
    print('Выполнено сохранение тематик')
    print('test branch  ')
    df_boundary = Pandas_Container().boundary()
    reviews = df_boundary.get_reviews('message')  # Получил все отзывы  
    entire_df = df_boundary.get_all_dataframe()   # Получил весь датафрейм
    print('Импотированный датасет сохранен и приведен к нужному формату - ', type(entire_df))
    
    yake_boundary = Yake_Container().boundary()
    keywords = yake_boundary.get_keywords(reviews) ## Проверка отзывов на словарь + Извлечение ключ. фраз.
    print('Ключевые фразы извлечены и приведены к формату ', type(keywords))
    

    rubert_boundary = RuBERT_Container().boundary()
    rubert_boundary.activate_embed(keywords) # Создание векторного пространства слов.
    list_by_groups = rubert_boundary.process_reviews(topics, reviews)
    print('Разметка отзывов по тематикам выполнена и сохранена ')
    
    sentiment_boundary = SentimentModel_Container().boundary()
    result = sentiment_boundary.analyze_sentiments(list_by_groups, topics)
    print('Sentiment Analysis произведён. Число строк в таблице',len(result))
    sliced_df = pd.concat([result.head(5), result.tail(5)])
    print ('Результирующий DataFrame',sliced_df)

    '''
    
    json_saver = Save2JSON_Container()
    json_saver.config.nested_list.from_value(keywords)
    json_saver.init_convert().save_to_json('Results_in_JSON','yake_keywords.json') ## Сохрание ключ. фраз в JSON 

    sentiment_boundary = SentimentModel_Container().boundary()
    result = sentiment_boundary.analyze_sentiments(list_by_groups, topics)
    print('Sentiment Analysis произведён. Число строк в таблице',len(result))
    sliced_df = pd.concat([result.head(5), result.tail(5)])
    print ('Результирующий DataFrame',sliced_df)

    postprocess = DataPostProcess_Container().boundary()
    new_dataframe = postprocess.validate_and_process(result, entire_df)
    sliced_df = pd.concat([new_dataframe.head(5), new_dataframe.tail(5)])
    print ('Постобработка DataFrame',sliced_df)

    weigths_norma = NormalizerWeight_Container().boundary()
    print('new_dataframe',new_dataframe.info()) 
    recalc_df = weigths_norma.process_grading(new_dataframe)
    print('recalc_df',recalc_df.info())    
    sliced_df = pd.concat([recalc_df.head(5), recalc_df.tail(5)])
    print ('Оценки пересчитаны',sliced_df)

    final_entries = Split_DF_Container().boundary()
    list_of_df = final_entries.process_data(recalc_df)    
    print ('DataFrame разделен по схеме нормализованной БД')
    print(len(list_of_df))
    for entry in list_of_df:
        filename, groups = next(iter(entry.items()))
        json_saver.config.nested_list.from_value(groups)
        json_saver.init_convert().save_to_json('Results_in_JSON',f'{filename}.json')
    print ('Таблицы DataFrame сохранены в JSON формате. Модуль завершает работу')
    '''
