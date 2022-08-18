from tsvis.server.backend.api.utils import get_api_params
from tsvis.parser.utils.logfile_utils import path_parser
from tsvis.parser.utils.cache_io import CacheIO
from .feature_read import featuremap_read, featuremap_diff_read
import base64
import io
import numpy as np
from PIL import Image
def featuremap_provider(file_path, range, tag, file_sorce_path, file_label_path):
    res = CacheIO(file_path).get_cache()
    sorce_data = CacheIO(file_sorce_path).get_cache()
    label_data = CacheIO(file_label_path).get_cache()
    if res:
        map_data = featuremap_read(data=res, range=range, tag=tag, sorce_data=sorce_data, label_data=label_data).get_data()
        return map_data
    else:
        return []
def featuremap_diff_provider(file_path1, file_path2):
    res1 = CacheIO(file_path1).get_cache()
    res2 = CacheIO(file_path2).get_cache()
    diff_data = featuremap_diff_read(data1=res1, data2=res2).get_data()
    return diff_data

def encode_base64(data):
    _io = io.BytesIO()
    _img = Image.fromarray(data.astype(np.uint8))
    _img.save(_io, "png")
    _content = _io.getvalue()
    _data = base64.b64encode(_content)
    res = "data:image/png;base64,%s" % _data.decode()
    return res

def get_featuremap_data(request):
    params = ['run', 'tag', 'range', 'task']
    run, tag, ranges, task = get_api_params(request, params)
    from tsvis.parser.utils.vis_logging import get_logger
    file_path = path_parser(get_logger().cachedir, run, 'featuremap', tag)
    file_sorce_path = path_parser(get_logger().cachedir, run, 'featuremap', task + '-sorce')
    file_label_path = path_parser(get_logger().cachedir, run, 'featuremap', task + '-label')
    data = featuremap_provider(file_path, int(ranges), tag, file_sorce_path, file_label_path)
    for item in range(len(data)):
        data[item]['value'] = [encode_base64(img) for img in data[item]['value']]
    return {tag: data}
