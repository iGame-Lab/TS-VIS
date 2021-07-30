from pathlib import Path
from zjvis.proto.graph_pb2 import GraphDef
from zjvis.proto.node_def_pb2 import NodeDef
from zjvis.proto.versions_pb2 import VersionDef
from zjvis.proto.attr_value_pb2 import AttrValue
from zjvis.proto.tensor_pb2 import TensorShapeProto
import re

def load_onnx_graph(fname):
    assert Path(fname).suffix == '.onnx', f'{fname} is not a *.onnx file.'
    assert Path(fname).exists(), f'{fname} is not exist.'

    import onnx
    m = onnx.load(fname)
    g = m.graph
    return parse(g)

def parser_input_output(node, name, op, input):
    shape = [str(d.dim_value) for d in node.type.tensor_type.shape.dim]
    shape = '[' + ', '.join(shape) + ']'
    attr = {'dtype': AttrValue(type=node.type.tensor_type.elem_type),
            'shape': AttrValue(s=shape.encode(encoding='utf_8'))}

    assert isinstance(input, list)
    return NodeDef(name=name.encode(encoding='utf_8'),
                   op=op,
                   input=input,
                   attr=attr)

def parse_weight_bias(node):
    shape = str(node.dims).encode(encoding='utf_8')
    return NodeDef(name=node.name.encode(encoding='utf_8'),
                   op=node.name.encode(encoding='utf_8'),
                   attr={'shape':AttrValue(s=shape)})

def str2dict(s):
    attr = {}
    for kv in re.split('#|\n',s):
        kv = kv.split('=')
        if len(kv)<2 or len(kv[0])<1:
            continue
        attr[kv[0]] = AttrValue(s=kv[1].encode(encoding='utf_8'))
    return attr

def parse(graph):
    nodes = []
    node_ident = {} # use output replace the current node's name.

    # parser input node
    for node in graph.input:
        nodes.append(parser_input_output(node=node, name=node.name,
                                         op='Variable', input=[]))
        node_ident[node.name] = node.name

    # parser train weights, bias
    for node in graph.initializer:
        nodes.append(parse_weight_bias(node))
        node_ident[node.name] = node.name

    for node in graph.node:
        node_ident[node.output[0]] = node.name

    # parser graph node (layer, conv, relu, pooling, ...)
    for node in graph.node:
        attr = []
        for s in node.attribute:
            attr.append('='.join([str(f[1]) for f in s.ListFields()]))

        inputs = [node_ident[name] if name in node_ident else name for name in node.input ]
        attr = str2dict('#'.join(attr))
        nodes.append(NodeDef(name = node.name.encode(encoding='utf_8'),
                             op = node.op_type,
                             input = inputs,
                             attr = attr)) #{'parameters': AttrValue(s=attr.encode(encoding='utf_8'))}

    # parser output
    for i, node in enumerate(graph.output, 1):
        nodes.append(parser_input_output(node=node, name=f'output.{i}',
                                         op='output',input=[node_ident[node.name]]))

    return GraphDef(node=nodes, versions=VersionDef(producer=22))
