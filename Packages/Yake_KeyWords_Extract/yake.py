import yake

class YakeExtractor:
    def __init__(self, language="ru", n=5, dedup_lim=0.65, dedup_func='seqm', window_size=1, top=15):
        self.yake_extractor = yake.KeywordExtractor(lan=language, n=n, dedupLim=dedup_lim, dedupFunc=dedup_func, windowsSize=window_size, top=top)

    def extract_single_row(self, text):
        try:
            keywords = self.yake_extractor.extract_keywords(text)
            return [keyword[0] for keyword in keywords]
        except Exception as e:
            raise Exception(f"Сбой в алгоритме извлечения ключевых фраз: {e}")


class YakeControl:
    def __init__(self, extractor: YakeExtractor):
        self.yake_extractor = extractor

    def extract_keywords(self, reviews_dict):
        print('Активация алгоритма Yake')
        keywords_dict = {}
        for index, review in reviews_dict.items():
            keywords = self.yake_extractor.extract_single_row(review)
            keywords_dict[index] = keywords
        
        return keywords_dict

class YakeBoundary:
    def __init__(self, control: YakeControl):
        self.yake_control = control

    def validate_reviews(self, reviews):
        if not isinstance(reviews, dict):
            raise ValueError("Отзывы должны быть в виде словаря. Его структура: Ключ-Значение")
        else:
            print("Отзывы в виде словаря. Обработка ключевых фраз начинается")
    
    def get_keywords(self, reviews_dict):
        self.validate_reviews(reviews_dict)
        keywords_dict = self.yake_control.extract_keywords(reviews_dict)

        for index, review in reviews_dict.items():
            if index not in keywords_dict or not keywords_dict[index]:
                keywords_dict[index] = [str(review)]
        for index, review in list(keywords_dict.items())[:2]:
            print(f"Ключ отзыва: {index}, Ключевые фразы: {review}")
        return keywords_dict

