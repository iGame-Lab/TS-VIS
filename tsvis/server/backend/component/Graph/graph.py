# -*- coding: UTF-8 -*-
"""
 Copyright 2021 Tianshu AI Platform. All Rights Reserved.

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
from __future__ import division, print_function, with_statement
from __future__ import unicode_literals  # at top of module

from collections import defaultdict


def get_source_name(s):
    if ":" in s:
        s = s.split(":")[0]
    if '^' in s:
        return s[1:]
    return s


def get_scope_level(s):
    if s == "root":
        return 0
    if '/' not in s:
        return 1
    return len(s.split('/'))


def get_name(s):
    if '/' not in s:
        return s
    return s.split('/')[-1]


class Node:
    def __init__(self, name, op):
        self._name = name
        self._op = op
        self._inputs = []
        self._outputs = []
        self._attrs = {}

    def __str__(self):
        input = "\n\t input:".join(self._inputs)
        output = "\n\t output:".join(self._outputs)
        return "node:{\n" + "\t name:" + self._name + "\n\t op:" + self._op + "\n\t input:" + input + "\n\t output:" \
               + output + "\n\t attrs" + str(self._attrs) + "}\n"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, s):
        self._name = s

    @property
    def op(self):
        return self._op

    @property
    def input(self):
        return self._inputs

    def add_input(self, i_name):
        self._inputs.append(i_name)

    @property
    def output(self):
        return self._outputs

    def add_output(self, o_name):
        self._outputs.append(o_name)

    @property
    def attr(self):
        return self._attrs

    def set_attr(self, attr):
        self._attrs = attr


class Graph:
    def __init__(self, name="root"):
        self._name = name
        self._node = {}

    def add_node(self, node):
        self._node[node.name] = node

    def get_node(self, name):
        if name not in self._node.keys():
            return KeyError
        return self._node[name]

    def get_all_nodes_name(self):
        return self._node.keys()

    def pop(self, name):
        self._node.pop(name)

    def get_name(self):
        return self._name


class TreeNode(object):
    """The basic node of tree structure"""

    def __init__(self, name, parent=None):
        super(TreeNode, self).__init__()
        self.name = name
        self.parent = parent
        self.child = {}
        self.node = None
        self.full_name = None

    def __repr__(self):
        return 'TreeNode(%s)' % self.name

    def __contains__(self, item):
        return item in self.child

    def __len__(self):
        """return number of children node"""
        return len(self.child)

    def get_child(self, name, defval=None):
        """get a child node of current node"""
        return self.child.get(name, defval)

    def add_child(self, name, obj=None):
        """add a child node to current node"""
        if obj and not isinstance(obj, TreeNode):
            raise ValueError(
                'TreeNode only add another TreeNode obj as child')
        if obj is None:
            obj = TreeNode(name)
        obj.parent = self
        self.child[name] = obj
        return obj

    def del_child(self, name):
        """remove a child node from current node"""
        if name in self.child:
            del self.child[name]

    def find_child(self, name, create=False):
        """find child node by path/name, return None if not found"""
        # convert path to a list if input is a string
        path = name if isinstance(name, list) else name.strip("/").split(
            "/")
        cur = self
        for sub in path:
            # search
            obj = cur.get_child(sub)
            if obj is None and create:
                # create new node if need
                obj = cur.add_child(sub)
            # check if search done
            if obj is None:
                break
            cur = obj
        cur.full_name = name
        return cur

    def items(self):
        return self.child.items()

    def dump(self, indent=0):
        """dump tree to string"""
        tab = '    ' * (indent - 1) + ' |- ' if indent > 0 else ''
        print('%s%s' % (tab, self.name))
        for name, obj in self.items():
            obj.dump(indent + 1)


class Proxy:
    def __init__(self, graph):
        self._nodes = graph.node
        self._links = self._get_links()
        # self._change_scope()
        self._graph = self._set_graph()
        self._add_fakeNode()
        self._tree = self._set_tree()

    # 提升某些特殊点的namescope
    def _change_scope(self):
        keys = self._graph.get_all_nodes_name()
        fixed_list = []
        for key in keys:
            node = self._graph.get_node(key)
            i_length = len(node.input)
            o_length = len(node.output)
            if i_length == 0 and o_length == 1:
                o_name = node.output[0]
                name = node.name
                o_name_level = get_scope_level(o_name)
                name_level = get_scope_level(name)
                diff = abs(o_name_level - name_level)
                # if name.startswith(o_name) and diff == 1:
                if o_name in name and diff == 1:
                    fixed_list.append((o_name, name))
        # print(len(fixed_list))
        for o_name, name in fixed_list:
            s = get_name(o_name)
            name_level = get_scope_level(name)
            if name_level == 2:
                c_name = name.split("/")[-1]
            else:
                c_name = name.replace("/" + s + "/", '/')
            # 删除图中节点
            tmp = self._graph.get_node(name)
            self._graph.pop(name)
            # 新增加节点，并修改名字以及输出
            new_node = Node(c_name, tmp.op)
            new_node.add_output(o_name)
            new_node.set_attr(tmp.attr)
            self._graph.add_node(new_node)
            # 修改连接关系
            self._links.pop(name)
            self._links.pop(o_name)
            self._links[o_name] = c_name
            self._links[c_name] = o_name

    # 增加虚节点
    def _add_fakeNode(self):
        keys = self._graph.get_all_nodes_name()
        add_node_name_list = set()

        for key in keys:
            node = self._graph.get_node(key)
            node_name = node.name
            for to_node_name in node.output:
                # 父节点指向子节点
                if get_source_name(to_node_name).startswith(node_name):
                    add_node_name_list.add(node_name)

                # 子节点指向父节点
                if node_name.startswith(get_source_name(to_node_name)):
                    add_node_name_list.add(to_node_name)
        add_node_name_list = list(add_node_name_list)

        # 为这些节点创建虚节点
        for node_name in add_node_name_list:

            node = self._graph.get_node(get_source_name(node_name))
            new_name = get_source_name(node_name) + "/(" + \
                       get_source_name(node_name).split('/')[-1] + ")"

            new_node = Node(new_name, node.op)
            links = self._links[get_source_name(node_name)]
            for i in node.input:
                new_node.add_input(i)
                i_name = get_source_name(i)
                # print(i_name)
                if i_name not in self._graph.get_all_nodes_name():
                    continue
                tmp = self._graph.get_node(i_name)
                if ("^" + i_name, "^" + node.name) in links:
                    tmp.add_output("^" + new_name)
                else:
                    tmp.add_output(new_name)
            for t in node.output:
                new_node.add_output(t)
                t_name = get_source_name(t)
                if t_name not in self._graph.get_all_nodes_name():
                    continue
                tmp = self._graph.get_node(t_name)
                if ("^" + node.name, "^" + t_name) in links:
                    tmp.add_input("^" + new_name)
                else:
                    tmp.add_input(new_name)
            new_node.set_attr(node.attr)
            self._graph.add_node(new_node)

    def _get_links(self):
        links = defaultdict(list)
        for node in self._nodes:
            to_name_without = get_source_name(node.name)
            from_names = node.input
            if from_names:
                for from_name in from_names:
                    name = node.name
                    from_name_without_ = get_source_name(from_name)
                    if "^" in from_name:
                        name = "^" + name
                    # links[from_name_without_].append((from_name, node.name))
                    links[from_name_without_].append((from_name, name))
                    # links[to_name_without].append((from_name, node.name))
                    links[to_name_without].append((from_name, name))
        return links

    def _set_graph(self):
        G = Graph()
        for node in self._nodes:
            tmp_node = Node(node.name, node.op)
            links = self._links[node.name]
            if links:
                for f, t in links:
                    f_without = get_source_name(f)
                    if f_without == tmp_node.name:
                        tmp_node.add_output(t)
                    else:
                        tmp_node.add_input(f)
            tmp_node.set_attr(node.attr)
            G.add_node(tmp_node)
        return G

    @property
    def graph(self):
        return self._graph

    def _set_tree(self):
        root = TreeNode("root")
        keys = self._graph.get_all_nodes_name()
        for key in keys:
            cur = root.find_child(key, True)
            cur.node = self._graph.get_node(key)
        return root

    @property
    def tree(self):
        return self._tree


graph_op = [
    {
        "op": "Convolution",
        "list": ["conv2d", "conv2d_transpose", "conv2dtranspose", "conv3d",
                 "depthwise_conv2d", "depthwiseconv2d",
                 "depthwise_conv2d_native", "depthwiseconv2dnative",
                 "separable_conv2d", "separableconv2d",
                 "atrous_conv2d", "atrousconv2d"]
    },
    {
        "op": "Normalization",
        "list": ["Local Response Normalization", "Batch Normalization",
                 "Weight Normalization", "Layer Normalization",
                 "Instance Normalization", "Consine Normalization",
                 "Group Normalization",
                 "Local Response Norm", "Batch Norm", "Weight Norm",
                 "Layer Norm", "Instance Norm", "Consine Norm",
                 "Group Norm"]
    },
    {
        "op": "Math&Activation&Pooling",
        "list": ["abs", "accumulate_n", "accumulaten",
                 "acos", "add",
                 "add_n", "addn",
                 "argmax", "argmin", "asin", "atan",
                 "batch_cholesky", "batchcholesky",
                 "batch_cholesky_solve", "batchcholeskysolve",
                 "batch_fft", "batchfft",
                 "batch_fft2d", "batch fft2d",
                 "batch_fft3d", "batch fft3d",
                 "batch_ifft", "batch ifft",
                 "batch_ifft2d", "batchifft2d",
                 "batch_ifft3d", "batchifft3d",
                 "batch_matmul", "batchmatmul",
                 "batch_matrix_band_part", "batchmatrixbandpart",
                 "batch_matrix_determinant", "batchmatrixdeterminant",
                 "batch_matrix_diag", "batchmatrixdiag",
                 "batch_matrix_diag_part", "batchmatrixdiagpart",
                 "batch_matrix_inverse", "batchmatrixinverse",
                 "batch_matrix_set_diag", "batchmatrixsetdiag",
                 "batch_matrix_solve", "batchmatrixsolve",
                 "batch_matrix_solve_ls", "batchmatrixsolvels",
                 "batch_matrix_transpose", "batchmatrixtranspose",
                 "batch_matrix_triangular_solve",
                 "batchmatrixtriangularsolve",
                 "batch_self_adjoint_eig", "batchselfadjointeig",
                 "ceil", "cholesky",
                 "cholesky_solve", "choleskysolve",
                 "complex", "complex_abs", "complexabs",
                 "conj", "cos", "cross", "cumprod", "cumsum", "diag",
                 "diag_part", "diagpart", "digamma", "div",
                 "div_no_nan", "divnonan",
                 "edit_distance", "editdistance",
                 "erf", "erfc", "exp", "fft", "fft2d", "fft3d", "floor",
                 "floordiv", "ifft", "ifft2d", "ifft3d",
                 "igamma", "igammac", "imag",
                 "inv", "invert_permutation", "invertpermutation", "lbeta",
                 "lgamma", "listdiff", "log", "matmul",
                 "matrix_determinant", "matrixdeterminant",
                 "matrix_inverse", "matrixinverse",
                 "matrix_solve", "matrixsolve",
                 "matrix_solve_ls", "matrixsolvels",
                 "matrix_triangular_solve", "matrixtriangularsolve",
                 "maximum", "minimum", "mod", "mul", "neg",
                 "polygamma", "pow", "real",
                 "reduce_all", "reduceall",
                 "reduce_any", "reduceany",
                 "reduce_max", "reducemax",
                 "reduce_mean", "reducemean",
                 "reduce_min", "reducemin",
                 "reduce_prod", "reduceprod",
                 "reduce_sum", "reducesum",
                 "round", "rsqrt",
                 "scalar_mul", "scalarmul",
                 "segment_max", "segmentmax",
                 "segment_mean", "segmentmean",
                 "segment_min", "segmentmin",
                 "segment_prod", "segmentprod",
                 "segment_sum", "segmentsum",
                 "self_adjoint_eig", "selfadjointeig", "sign", "sin",
                 "sparse_segment_mean", "sparsesegmentmean",
                 "sparse_segment_sqrt_n", "sparsesegmentsqrtn",
                 "sparse_segment_sqrt_n_grad", "sparsesegmentsqrtngrad",
                 "sparse_segment_sum", "sparsesegmentsum", "sqrt",
                 "square",
                 "squared_difference", "squareddifference", "sub", "sum",
                 "tan", "trace", "transpose", "truediv",
                 "unique",
                 "unsorted_segment_sum", "unsortedsegmentsum",
                 "where", "zeta",
                 "bias_add", "biasadd",
                 "elu", "tanh",
                 "log_softmax", "logsoftmax",
                 "relu", "relu6", "selu", "crelu",
                 "leaky_relu", "leaky relu",
                 "sigmoid", "softmax", "softplus", "softsign",
                 "avg_pool", "avgpool",
                 "avg_pool3d", "avgpool3d",
                 "max_pool", "maxpool",
                 "max_pool3d", "maxpool3d",
                 "max_pool_with_argmax", "maxpoolwithargmax",
                 "global_pool, globalpool",
                 "pyramid_pool, pyramidpool"]
    },
    {
        "op": "Sparse Tensors&Tensor Transformations",
        "list": ["shape", "sparse_add", "sparseadd", "sparse_concat",
                 "sparseconcat", "sparse_fill_empty_rows",
                 "sparsefillemptyrows", "sparse_maximum", "sparsemaximum",
                 "sparse_merge", "sparsemerge",
                 "sparse_minimum", "sparseminimum", "sparse_reduce_sum",
                 "sparsereducesum", "sparse_reorder",
                 "sparsereorder", "sparse_reset_shape", "sparseresetshape",
                 "sparse_reshape", "sparsereshape",
                 "sparse_retain", "sparseretain", "sparse_softmax",
                 "sparsesoftmax", "sparse_split", "sparsesplit",
                 "sparse_tensor_dense_matmul", "sparsetensordensematmul",
                 "sparse_tensor_to_dense",
                 "sparsetensortodense", "sparse_to_dense", "sparsetodense",
                 "sparse_to_indicator", "sparsetoindicator",
                 "SparseTensor", "SparseTensorValue",
                 "batch_to_space", "batchtospace", "bitcast",
                 "boolean_mask", "booleanmask", "cast", "concat",
                 "depth_to_space", "depthtospace", "dynamic_partition",
                 "dynamicpartition", "dynamic_stitch",
                 "dynamicstitch", "expand_dims", "expanddims",
                 "extract_image_patches", "extractimagepatches", "gather",
                 "gather_nd", "gathernd", "meshgrid", "one_hot", "onehot",
                 "pack", "pad", "rank", "reshape", "reverse",
                 "reverse_sequence", "reversesequence", "saturate_cast",
                 "saturatecast", "shape", "shape_n", "shapen",
                 "size", "slice", "space_to_batch", "spacetobatch",
                 "space_to_depth", "spacetodepth", "split",
                 "squeeze", "string_to_number", "stringtonumber", "tile",
                 "to_bfloat16", "tobfloat16", "to_double",
                 "todouble", "to_float", "tofloat", "to_int32", "toint32",
                 "to_int64", "toint64", "transpose",
                 "unique_with_counts", "uniquewithcounts", "unpack"]
    },
    {
        "op": "ControlFlow",
        "list": ["add_check_numerics_ops", "addchecknumericsops", "Assert",
                 "case", "check_numerics", "checknumerics",
                 "cond", "count_up_to", "countupto", "equal", "greater",
                 "greater_equal", "greaterequal", "group",
                 "identity", "is_finite", "isfinite", "is_inf", "isinf",
                 "is_nan", "isnan", "less", "less_equal",
                 "lessequal", "logical_and", "logicaland", "logical_not",
                 "logicalnot", "logical_or", "logicalor",
                 "logical_xor", "logicalxor", "no_op", "noop", "not_equal",
                 "notequal", "Print", "select", "tuple",
                 "verify_tensor_all_finite", "verifytensorallfinite",
                 "where", "while_loop", "whileloop"]
    },
    {
        "op": "Losses&Metrics",
        "list": ["absolute_difference", "absolutedifference", "add_loss",
                 "addloss", "cosine_distance",
                 "cosinedistance", "ctc_loss", "ctcloss", "get_losses",
                 "getlosses", "get_regularization_losses",
                 "getregularizationlosses", "get_total_loss",
                 "gettotalloss", "l2_loss", "l2loss", "log_loss",
                 "logloss", "nce_loss", "nceloss", "sigmoid_cross_entropy",
                 "sigmoidcrossentropy",
                 "softmax_cross_entropy", "softmaxcrossentropy",
                 "sum_of_pairwise_squares", "sumofpairwisesquares",
                 "sum_of_squares", "sumofsquares", "accuracy",
                 "aggregate_metric_map", "aggregatemetricmap",
                 "aggregate_metrics", "aggregatemetrics",
                 "auc_using_histogram", "aucusinghistogram",
                 "confusion_matrix", "confusionmatrix", "set_difference",
                 "setdifference", "set_intersection",
                 "setintersection", "set_size", "setsize", "set_union",
                 "setunion", "sampled_softmax_loss",
                 "sampledsoftmaxloss", "sigmoid_cross_entropy_with_logits",
                 "sigmoidcrossentropywithlogits",
                 "streaming_accuracy", "softmax_cross_entropy_with_logits",
                 "softmaxcrossentropywithlogits",
                 "sparse_softmax_cross_entropy_with_logits",
                 "sparsesoftmaxcrossentropywithlogits",
                 "streamingaccuracy",
                 "streaming_auc", "streamingauc", "streaming_mean",
                 "streamingmean", "streaming_mean_absolute_error",
                 "streamingmeanabsoluteerror",
                 "streaming_mean_cosine_distance",
                 "streamingmeancosinedistance",
                 "streaming_mean_iou", "streamingmeaniou",
                 "streaming_mean_relative_error",
                 "streamingmeanrelativeerror",
                 "streaming_mean_squared_error",
                 "streamingmeansquarederror",
                 "streaming_percentage_less", "streamingpercentageless",
                 "streaming_precision", "streamingprecision",
                 "streaming_recall", "streamingrecall",
                 "streaming_recall_at_k", "streamingrecallatk",
                 "streaming_root_mean_squared_error",
                 "streamingrootmeansquarederror",
                 "streaming_sparse_precision_at_k",
                 "streamingsparseprecisionatk",
                 "streaming_sparse_recall_at_k",
                 "streamingsparserecallatk",
                 "weighted_cross_entropy_with_logits",
                 "weightedcrossentropywithlogits"]
    },
    {
        "op": "InputsandReaders",
        "list": ["batch", "batch_join", "batchjoin", "decode_csv",
                 "decodecsv", "decode_json_example",
                 "decodejsonexample", "decode_raw", "decoderaw",
                 "FIFOQueue", "FixedLenFeature",
                 "FixedLengthRecordReader", "FixedLenSequenceFeature",
                 "IdentityReader", "input_producer",
                 "inputproducer", "limit_epochs", "limitepochs",
                 "match_filenames_once", "matchfilenamesonce",
                 "matching_files", "matchingfiles", "PaddingFIFOQueue",
                 "parse_example", "parseexample",
                 "parse_single_example", "parsesingleexample",
                 "placeholder", "placeholder_with_default",
                 "placeholderwithdefault", "QueueBase",
                 "RandomShuffleQueue", "range_input_producer",
                 "rangeinputproducer", "read_file", "readfile",
                 "ReaderBase", "shuffle_batch", "shufflebatch",
                 "shuffle_batch_join", "shufflebatchjoin", "size",
                 "slice_input_producer", "sliceinputproducer",
                 "sparse_placeholder", "sparseplaceholder",
                 "string_input_producer", "stringinputproducer",
                 "TextLineReader", "TFRecordReader", "VarLenFeature",
                 "WholeFileReader"]
    }
]
