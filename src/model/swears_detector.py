import json
from fuzzywuzzy.StringMatcher import StringMatcher
from enum import Enum



class ActionList(Enum):
    Delete = 0
    Stars = 1
    Replace = 2
    Mask = 3


class SwearsDetector:
    def __init__(self, source_file_path):
        file = json.load(open(source_file_path, "r", encoding="utf-8"))
        self.swears = file['swears']
        self.not_swears = file["not-swears"]

    def detect(self, string, action=None, max_distance_ratio=0.75):
        if action is None:
            action = ActionList.Stars
        excluded = []
        for excluded_key in self.swears.keys():
            searched_string = string
            founded = [1]
            cut_from = 0
            while len(founded) > 0:
                n = len(excluded_key)
                matcher = StringMatcher(None, excluded_key, searched_string)
                matched = matcher.get_matching_blocks()
                # print(matched, excluded_key)
                founded = []
                N = len(searched_string)
                for match in matched:
                    if match[1] >= N:
                        continue
                    x, y = self.__get_matching_words(searched_string, match[1], match[2] + match[1])
                    # print(x, y)
                    if (x, y) in founded:
                        continue
                    founded.append((x, y))
                    match_str = searched_string[x+1:y]
                    for swear in self.swears[excluded_key].keys():
                        if match_str in self.not_swears:
                            continue
                        m = StringMatcher(None, swear, match_str)
                        ratio = m.ratio()
                        # print(ratio)
                        if ratio >= max_distance_ratio:
                            excluded.append((
                                x + cut_from,
                                y + cut_from,
                                self.swears[excluded_key][swear] if action == ActionList.Replace else ''
                            ))
                            break
                if len(founded) > 0:
                    searched_string = searched_string[founded[-1][1]:]
                    cut_from += founded[-1][1]-1

        for to_change in excluded:
            replacement = ''
            if action == ActionList.Stars:
                replacement = string[to_change[0]+1] + '*' * (to_change[1]-to_change[0]-2)
            elif action == ActionList.Mask:
                replacement = '<mask>'
            else:
                replacement = to_change[2]
            string = string[:to_change[0]+1] + replacement + string[to_change[1]:]
        return string


    @staticmethod
    def __get_matching_words(str1, pos1, pos2):
        n = len(str1)
        while str1[pos1].isalpha() and pos1 > 0:
            pos1 -= 1
        while str1[pos2].isalpha() and pos2 < n - 1:
            pos2 += 1
        return pos1, pos2



if __name__ == '__main__':
    detector = SwearsDetector("C:\\Materiały\\bitehack\\src\\data\\excluded_words.json")
    print(detector.detect("u fucking idiot as bitch and dumbass dumbass what u have done", action=ActionList.Mask))