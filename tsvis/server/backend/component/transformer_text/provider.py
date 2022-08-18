from tsvis.server.backend.api.utils import get_api_params
from tsvis.parser.utils.logfile_utils import path_parser
from tsvis.parser.utils.cache_io import CacheIO
from .feature_read import transformer_text_read
def transformer_text_data_provider(file_path, tag):
    res = CacheIO(file_path).get_cache()
    if res:
        transformer_data = transformer_text_read(data=res, tag=tag).get_data()
        return transformer_data
    else:
        raise ValueError('No such data')

def get_transformer_text_data(request):
    params = ['run', 'tag']
    run, tag = get_api_params(request, params)
    from tsvis.parser.utils.vis_logging import get_logger
    file_path = path_parser(get_logger().cachedir, run, 'transformer', tag)
    data = transformer_text_data_provider(file_path, tag)
    return {tag: data}