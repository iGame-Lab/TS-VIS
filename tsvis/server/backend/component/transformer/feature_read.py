class transformer_text_read:
    def __init__(self, data=None, tag=None):
        self.data = data
        self.tag = tag
    def get_data(self):
        _data = self.data

        if "transformertext-sentence" in _data[0]['tag']:
            value = _data[0]['value'].tolist()
        else:
            res = {}
            attention = {}
            for kid_data in _data[0]['value']:
                if type(_data[0]['value'][kid_data]) == dict:
                    for kid in _data[0]['value'][kid_data]:
                        _data[0]['value'][kid_data][kid] = _data[0]['value'][kid_data][kid].tolist()
                    attention[kid_data] = _data[0]['value'][kid_data]
            res['attention'] = attention
            res['bidirectional'] = _data[0]['value']['bidirectional']
            res['default_filter'] = _data[0]['value']['default_filter']
            res['displayMode'] = _data[0]['value']['displayMode']
            res['layer'] = _data[0]['value']['layer']
            res['head'] = _data[0]['value']['head']


            value = {
                'wall_time': _data[0]['wall_time'],
                'step': _data[0]['step'],
                'data': res
            }
        return value
