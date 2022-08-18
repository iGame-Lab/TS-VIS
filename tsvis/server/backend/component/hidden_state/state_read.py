import numpy as np
import copy

class state_read:
    def __init__(self, data, pos, ranges, word):
        self.data = data
        self.pos = pos
        self.ranges = ranges
        self.word = word

    def get_data(self):
        _data = self.data[0]['value']
        length = len(_data)
        ranges = int(self.ranges)
        pos = int(self.pos)
        word = self.word[0]['value'][0]
        if pos + ranges < length - 1:
            if pos + ranges > len(word):
                input_word = copy_space_word(pos, ranges, word)
            else:
                input_word = copy.deepcopy(word[pos:pos + ranges])
            result = {
                "data": _data[pos:pos + ranges].tolist(),
                "word": input_word,
                "right": length - pos - ranges,
                "max": np.max(_data).item(),
                "min": np.min(_data).item()
            }
        else:
            if pos + ranges > len(word):
                input_word = copy_space_word(pos, ranges, word)
            else:
                input_word = copy.deepcopy(word[pos:pos + ranges])
            result = {
                "data": _data[pos:].tolist(),
                "word": input_word,
                "right": 0,
                "max": np.max(_data).item(),
                "min": np.min(_data).item()
            }
        return result


class state_select_read:
    def __init__(self, data, pattern, threshold, word, length):
        self.data = data
        self.pattern = pattern
        self.threshold = threshold
        self.word = word
        self.length = int(length)

    def get_data(self):
        _data = self.data[0]['value']
        _data_len = len(_data)
        select_data = _data.copy()
        word = self.word[0]['value'][0]
        threshold = float(self.threshold)
        pattern = list(map(self.change_int, self.pattern))
        select_data[_data > threshold] = 1
        select_data[_data < threshold] = 0
        pattern_len = len(self.pattern)
        select_data = np.transpose(select_data, (1, 0))
        pos = []
        for kid_data in select_data:
            pos += self.find_kid_pos(kid_data, pattern)
        pos = set(pos)
        res = []
        uid = 0
        for i in pos:
            item = {
                'id': uid,
                'start_pos': i,
                'data': word[i:min(i + self.length, _data_len)]
            }
            res.append(item)
            uid += 1
        return res

    def change_int(self, x):
        return int(x)

    def find_kid_pos(self, s, p):
        s_len = len(s)
        p_len = len(p)
        i = 0
        res = []
        while i < s_len - p_len:
            tip = 0
            patten_list = s[i:i + p_len]
            for s_kid, p_kid in zip(patten_list, p):
                if s_kid != p_kid:
                    tip = 1
                    break
            if tip == 0:
                res.append(i)
            i += 1
        return res


def is_space(word):
    for _char in word:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False


def copy_space_word(pos, ranges, word):
    space_num = pos + ranges - len(word)
    input_word = copy.deepcopy(word[pos:])
    is_chinese = is_space(input_word)
    for i in range(space_num):
        if is_chinese:
            input_word += '￥'
        else:
            input_word += ' ￥'

    return input_word
