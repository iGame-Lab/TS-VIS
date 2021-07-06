# -*- coding: UTF-8 -*-
"""
 Copyright 2020 Tianshu AI Platform. All Rights Reserved.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
 =============================================================
"""
from .graph import Node, Graph, TreeNode
from collections import defaultdict

filterList = [
    'summary_write_image',
    'summary_write_pb',
    'summary_write_histogram',
    'summary_write_scalar',
    'create_summary_writer',
    'flush_summary_writer'
]


def isTrue(layers, name):
    for layer in layers:
        if layer['name'] == name and layer['class_name'] in filterList:
            return True
    return False


class Proxy_json:
    def __init__(self, data):
        self.data = data
        self._graph = self._set_graph()
        self._tree = self._set_tree()

    @property
    def graph(self):
        return self._graph

    def _set_graph(self):
        class_name = self.data['class_name']
        if class_name == "Sequential":
            return self._extract_from_seq()
        else:
            return self._extract_from_model()

    def _extract_from_model(self):
        config = self.data['config']
        name = config['name']
        layers = config['layers']
        # input_layers = config['input_layers']
        # output_layers = config['output_layers']
        links = defaultdict(list)
        backend = self.data['backend']
        if backend == 'oneflow':
            for layer in layers:
                tmp_name = layer['name']
                tmp_op = layer['class_name']
                if tmp_op in filterList:
                    continue
                tmp_inbound_nodes = layer['inbound_nodes']
                if not tmp_inbound_nodes:
                    continue
                for tmp_inbound_node in tmp_inbound_nodes:
                    tmp_inbound_node_name = tmp_inbound_node
                    if isTrue(layers, tmp_inbound_node_name):
                        continue
                    links[tmp_name].append(
                        (tmp_inbound_node_name, tmp_name))
                    links[tmp_inbound_node_name].append(
                        (tmp_inbound_node_name, tmp_name))
        else:
            for layer in layers:
                tmp_name = layer['name']
                tmp_inbound_nodes = layer['inbound_nodes']
                if not tmp_inbound_nodes:
                    continue
                for tmp_inbound_node in tmp_inbound_nodes[0]:
                    tmp_inbound_node_name = tmp_inbound_node[0]
                    links[tmp_name].append(
                        (tmp_inbound_node_name, tmp_name))
                    links[tmp_inbound_node_name].append(
                        (tmp_inbound_node_name, tmp_name))
        g = Graph(name)
        for layer in layers:
            tmp_name = layer['name']
            if backend == 'oneflow' and isTrue(layers, tmp_name):
                continue
            tmp_op = layer['class_name']
            tmp_node = Node(tmp_name, tmp_op)
            tmp_links = links[tmp_name]
            if tmp_links:
                for f, t in tmp_links:
                    if f == tmp_name:
                        tmp_node.add_output(t)
                    else:
                        tmp_node.add_input(f)
            tmp_node.set_attr(layer['config'])
            g.add_node(tmp_node)
        totalKey = g.get_all_nodes_name()
        delList = []
        for key in totalKey:
            node = g.get_node(key)
            if not node.input and not node.output:
                delList.append(node.name)
        for l in delList:
            g.pop(l)
        return g

    def _extract_from_seq(self):
        config = self.data['config']
        name = config['name']
        layers = config['layers']
        build_input_shape = config['build_input_shape']
        shape = {'shape': build_input_shape}
        input_node = Node("input", "ReadVariable")
        input_node.add_output(layers[0]['config']['name'])
        input_node.set_attr(shape)
        g = Graph(name)
        g.add_node(input_node)
        for layer in layers:
            tmp_name = layer['config']['name']
            tmp_op = layer['class_name']
            tmp_node = Node(tmp_name, tmp_op)
            if layers.index(layer) == 0:
                tmp_node.add_input("input")
            else:
                tmp_input_name = layers[layers.index(layer) - 1]['config'][
                    'name']
                tmp_node.add_input(tmp_input_name)
            if layers.index(layer) != len(layers) - 1:
                tmp_output_name = \
                layers[layers.index(layer) + 1]['config']['name']
                tmp_node.add_output(tmp_output_name)
            tmp_node.set_attr(layer['config'])
            g.add_node(tmp_node)
        return g

    def _set_tree(self):
        root = TreeNode(self.graph.get_name())
        keys = self._graph.get_all_nodes_name()
        for key in keys:
            cur = root.find_child(key, True)
            cur.node = self._graph.get_node(key)
        return root

    @property
    def tree(self):
        return self._tree
