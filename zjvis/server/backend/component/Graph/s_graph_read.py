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
import json
from backend.component.Graph.parse_json import Proxy_json
from backend.component.Graph.graph import Node
from backend.component.Graph.graph_read import get_data

# Base_RATE = 16
# nodes保留每个节点的单独信息，以节点全称为key进行索引

nodes = {}
# edges_info保留每条线的维度信息，以起始节点+‘_’+目标节点为key进行索引
edges_info = {}


class Graph:
    def __init__(self):
        self.nodes = []

    @property
    def node(self):
        return self.nodes

    def add_node(self, node):
        node["name"] = node["uid"].replace("-", "/")
        for i in range(len(node["inputs"])):
            node["inputs"][i] = node["inputs"][i].replace("-", "/")
        self.nodes.append(node)


# 同根同支，以短边的尽头为分叉点
# 同根不同支，
# 不同根
def diff_index_find(small_len, node_edge_list, target_edge_list, same_root,
                    same_branch):
    # 遍历寻找分叉点
    for i in range(small_len):

        # 判断是否同根
        if i == 0:
            if node_edge_list[i] == target_edge_list[i]:
                same_root = True
            else:
                same_root = False
                break

        # 判断是否同支
        if i == small_len - 1:
            if node_edge_list[i] == target_edge_list[i]:
                same_branch = True
            else:
                same_branch = False
                break

        if node_edge_list[i] != target_edge_list[i]:
            break

    if same_branch:
        return -1
    else:
        return i


def edge_build(edge_list, diff_index):
    nodes_list = []
    curr_edge = ""
    for edge in edge_list:
        if curr_edge == "":
            curr_edge = edge
        else:
            curr_edge = curr_edge + "/" + edge
        nodes_list.append(curr_edge)
    for i in range(diff_index):
        # print(str(i)+"-"+str(diff_index)+"-"+str(len(nodes_list)))
        del nodes_list[0]
    return nodes_list


def edge_deal(node):
    # 获取当前节点的全称
    node_path = node["uid"]
    # 获取当前节点的目标节点集
    targets = node["targets"]
    # 获取当前节点的输出维度集
    if "_output_shapes" in node["attrs"]:
        output_shapes = node["attrs"]["_output_shapes"]
    else:
        output_shapes = [""]

    # 判断输出维度集中是否只有一个输出
    sign = 1
    if len(output_shapes) == 1:
        sign = 0
    else:
        sign = 1
    # 存储当sign为1时，两个节点之间的边的信息
    cur2targets_edge_info = []
    if sign == 1:
        # 存储当前输出维度与目标节点输出维度均不一致的情况
        # candidate_list = []
        for i, target in enumerate(targets):
            cur2targets_edge_info.append("{?}")
            # 标记是否唯一匹配
            unique_sign = False
            duplication_sign = False
            if "_output_shapes" in nodes[target]["attrs"]:
                target_output_shapes = nodes[target]["attrs"][
                    "_output_shapes"]
            else:
                target_output_shapes = [""]
            # 若有匹配
            # 若有单个匹配，则在cur2targets_edge_info的相应位置存储维度信息
            # 若有多个匹配，则在cur2targets_edge_info的相应位置存储？，并将其存入候选列
            for output_shape in output_shapes:
                if duplication_sign:
                    break
                for target_output_shape in target_output_shapes:
                    if (output_shape == target_output_shape) & (
                            unique_sign is False):
                        unique_sign = True
                        cur2targets_edge_info[i] = output_shape
                        break
                    elif (output_shape == target_output_shape) & (
                            unique_sign is True):
                        duplication_sign = True
                        cur2targets_edge_info[i] = "{?}"
                        # candidate_list.append(target)
                        break
                    else:
                        continue
            # 若无匹配，则在cur2targets_edge_info的相应位置存储？，并将其存入候选列
            if (unique_sign is False) & (duplication_sign is False):
                cur2targets_edge_info[i] = "{?}"
                # candidate_list.append(target)

    # 判断两节点是否同根
    same_root = False
    # 判断两节点是否同支
    same_branch = False
    # 拆分指出边的路径
    node_edge_list = node_path.strip("/").split("/")
    node_edge_len = len(node_edge_list)

    for k, target in enumerate(targets):
        # 根据node_path和target的联合建立一个key,add中根据索引取出边的信息和j组成字典

        # 拆分每个指入边的的路径
        target_edge_list = target.strip("/").split("/")
        target_edge_len = len(target_edge_list)

        # 寻找分叉点
        if node_edge_len < target_edge_len:
            diff_index = diff_index_find(node_edge_len, node_edge_list,
                                         target_edge_list, same_root,
                                         same_branch)
        else:
            diff_index = diff_index_find(target_edge_len, node_edge_list,
                                         target_edge_list, same_root,
                                         same_branch)

        # 构边与插入
        # 同支情况下由于展开父节点消失，故不进行边的构建
        if diff_index == -1:
            continue
        else:
            from_nodes = edge_build(node_edge_list, diff_index)
            to_nodes = edge_build(target_edge_list, diff_index)
            for i in from_nodes:
                for j in to_nodes:
                    # 构造和存储每条边的信息
                    edge_id = i + "_" + j
                    if sign == 0:
                        edges_info[edge_id] = output_shapes[0]
                    else:
                        edges_info[edge_id] = cur2targets_edge_info[k]

                    nodes[i]["targets"].add(j)


# 提取所需信息构造数据结构
# label  节点简称
# index  节点的唯一数字索引，每层赋予16个编号
# parent 节点的父节点全称
# uid    节点的全称
# op     操作
# layer  节点当前所在的层级
# targets 目标节点
# attrs  属性
def data_build(tree, graph, data, level, curr_path=None, Graph_=None):
    # parent用于存储父节点名称
    # curr_path用于存储当前路径，主要用于虚节点的构造上
    parent = curr_path

    if len(tree.child) > 0:
        for i, sub_tree in enumerate(tree.child):

            # tree.child 是一个由缩略名作为key，TreeNode结构体作为value的字典
            node_name = sub_tree
            # index += 1

            if level == 0:
                # 第一层节点不存在父节点
                node_parent = ""
                curr_path = node_name
            else:
                node_parent = parent
                curr_path = node_parent + '/' + node_name

            # 用于判断节点是否存在，即是否在log中存有信息
            exits = True
            if tree.child[node_name].node is None:
                exits = False

            node_targets = []
            if exits:
                node_info = tree.child[node_name].node  # 一个字典
                for target in node_info.output:
                    node_targets.append(target)
                    # edge_deal(target,node_targets)
            else:
                # 为虚节点构造一个空的Node结构体
                # {
                # 	 name:
                # 	 op:
                # 	 input:
                # 	 output:
                # 	 attrs{}
                # }
                # 构造函数中需要包含name和op信息
                node_info = Node(curr_path, "")

            # 从node_info中获取节点的全称
            node_name_full = node_info.name
            # 处理attr的shape和_output_shape属性，处理成{1,1,1}形式的字符串
            node_attr = {}
            for key in node_info.attr.keys():
                if (key != "_output_shapes") & (key != "shape"):
                    node_attr[key] = node_info.attr[key]
                elif key == "shape":
                    # shape处理成{1,1,1}形式的字符串
                    # 每个shape都是一个protobuf,通过.来获取子层结构
                    raw_dim = node_info.attr[key]
                    raw_dim_length = len(raw_dim)
                    new_dim = ""
                    for j, dim in enumerate(raw_dim):
                        if j == 0:
                            new_dim = new_dim + '{' + str(dim)
                        else:
                            new_dim += ',' + str(dim)
                        if j == raw_dim_length - 1:
                            new_dim += '}'
                    node_attr[key] = new_dim
                elif key == "_output_shapes":
                    # 在_output_shapes中用一个list存储当前节点到其他节点边的维度信息，每一个是一个shape
                    shape_list = node_info.attr[key].list.shape
                    output_shapes = []
                    for shape in shape_list:
                        raw_dim = shape.dim
                        raw_dim_length = len(raw_dim)
                        new_dim = ""
                        for j, dim in enumerate(raw_dim):
                            str_dim = ""
                            if dim.size == -1:
                                str_dim = "?"
                            else:
                                str_dim = str(dim.size)
                            if j == 0:
                                new_dim = '{' + str_dim
                            else:
                                new_dim += ',' + str_dim
                            if j == raw_dim_length - 1:
                                new_dim += '}'
                        output_shapes.append(new_dim)
                    node_attr[key] = output_shapes

            # 节点构造与添加
            node = {}
            node["label"] = node_name
            # node["index"] = index
            node["parent"] = node_parent
            node["uid"] = node_name_full
            node["op"] = node_info.op
            node["layer"] = level + 1
            node["attrs"] = node_attr
            node["inputs"] = node_info.input
            Graph_.add_node(node)
            # print(node_info)
            node2nodes = node.copy()
            # nodes中node的边不重复，且仅含当前节点的信息,构建时为空，在处理后添加
            node2nodes["targets"] = set()
            nodes[node_name_full] = node2nodes

            node["targets"] = node_targets
            node["sub_net"] = []
            if level == 0:
                data.append(node)
                data_build(tree.child[node_name], graph, data[i],
                           level + 1, curr_path)
            else:
                data["sub_net"].append(node)
                data_build(tree.child[node_name], graph,
                           data["sub_net"][i], level + 1, curr_path)


def data_search(data, level=1, build=True):
    # 由于第一层和其他层数据的存储形式不同
    # 第一层直接存放，其他层存在各自的subnet中
    if level == 1:
        for sub_data in data:
            if build:
                edge_deal(sub_data)
            else:
                targets_list = list(nodes[sub_data["uid"]]["targets"])
                sub_data["targets"] = []
                for target in targets_list:
                    edge_dic = {}
                    edge_id = sub_data["uid"] + "_" + target
                    edge_dic["id"] = target
                    edge_dic["info"] = edges_info[edge_id]
                    sub_data["targets"].append(edge_dic)
                # sub_data["targets"] = list(nodes[sub_data["uid"]]["targets"])
            # print(sub_data["label"])
            data_search(sub_data, level + 1, build)
    else:
        data = data["sub_net"]
        if len(data) > 0:
            for sub_data in data:
                # print(sub_data["label"])
                if build:
                    # 将重组的目标节点信息存进nodes中
                    edge_deal(sub_data)
                else:
                    # 从nodes中提取回信息放入data中
                    targets_list = list(nodes[sub_data["uid"]]["targets"])
                    sub_data["targets"] = []
                    for target in targets_list:
                        edge_dic = {}
                        edge_id = sub_data["uid"] + "_" + target
                        edge_dic["id"] = edge_id
                        edge_dic["info"] = edges_info[edge_id]
                        sub_data["targets"].append(edge_dic)
                    # sub_data["targets"] = list(nodes[sub_data["uid"]]["targets"])
                data_search(sub_data, level + 1, build)


def preprocess(s_data):
    s_data = s_data.replace('\n', '')
    data = json.loads(s_data)
    res = []
    g = Graph()
    for d in data:
        proxy = Proxy_json(d)
        tree = proxy.tree
        # 建立data的层次型数据结构以及nodes的索引型结构
        _data = []
        level = 0
        graph = proxy.graph
        data_build(tree, graph, _data, level, Graph_=g)
        # 边的重新构造，存入nodes中
        data_search(_data, build=True)
        # 从nodes中取出边，赋值回data中
        data_search(_data, build=False)
        if _data:
            res.append(_data)
    return [res, g]


def get_s_graph_data(s_data):
    res, g = preprocess(s_data)
    return res


def get_c_graph_data(c_data):
    res, g = preprocess(c_data)
    res = get_data(g)
    return res
