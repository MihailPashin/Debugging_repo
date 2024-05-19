class Group:
    def __init__(self, name_group, candidates, sm_score):
        self.name_group = name_group
        self.candidates = candidates
        self.sm_score = sm_score

    def is_sm_score_valid(self):
        return 0.66 < self.sm_score < 0.99

class GroupControl:
    def __init__(self, data):
        self.groups = {}
        self.load_data(data)

    def load_data(self, data):
        for idx, info in data.items():
            if self.validate_entry(info):
                self.groups[idx] = Group(info['name_group'], info['candidates'], info['sm_score'])
            else:
                print(f"Некорректный ввод {idx}")

    def validate_entry(self, info):
        required_keys = {'name_group', 'candidates', 'sm_score'}
        if not required_keys.issubset(info.keys()):
            raise ValueError("Структура словаря нарушена - проверьте наличие столбцов. 'name_group', 'candidates', 'sm_score'")
        if not isinstance(info['candidates'], list) or not all(isinstance(candidate, str) for candidate in info['candidates']):
            raise ValueError("Поисковые запросы должны быть списком строк. List of Strings")
        if not isinstance(info['sm_score'], float):
            raise ValueError("Тип данных степени схожести не float")
        return True

    def check_groups(self):
        return self.groups 
 
    def save_groups(self):
        result = {}
        for idx, group in self.groups.items():
            result[idx] = {
                'name_group': group.name_group,
                'candidates': group.candidates,
                'sm_score': group.sm_score
            }
        return result

class GroupInterface:
    def __init__(self, group_control: GroupControl):
        self.control = group_control

    def check_groups_and_save(self):
        for idx, group in self.control.check_groups().items():
            if not(group.is_sm_score_valid()):
                raise ValueError(f"Тематика отзывов {idx}: {group.name_group} с невалидным sm_score: {group.sm_score}. Диапазон допустимых значений 0.66 < x < 0.99")      
            else:
                print(f"Тематика отзывов {idx + 1}: {group.name_group}")
        return self.control.save_groups()

