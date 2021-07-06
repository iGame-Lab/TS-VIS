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
from oneflow.customized.utils import projector_pb2
from collections.abc import Iterable
from typing import BinaryIO
from typing import Optional
import numpy as np
from collections import namedtuple

ProjectorSummaryItem = namedtuple(
    "ProjectorSummaryItem", ["metadata", "sample", "projectors"]
)
Metadata = namedtuple("Metadata", ["type", "content"])
# SampleItem = namedtuple("SampleItem", ["name", "type", "X"])
ProjectorItem = namedtuple(
    'ProjectorItem', ['tag', 'step', 'wall_time', 'value', 'label']
)


def _decode_tensor(tensor):
    _tensor_shape = tuple([i.size for i in tensor.shape.dim])
    _decoded = np.frombuffer(tensor.content, dtype=tensor.dtype)
    _decoded = _decoded.reshape(_tensor_shape)
    return _decoded


class Projector_Reader:

    def __init__(
            self,
            fileblock: BinaryIO,
            tag_filter: Optional[Iterable] = None,
            stop_on_error: bool = False
    ):
        """
        Initalize new projector reader
        :param fileblock: A File IO for projector data
        :param tag_filter: A list of tags to leave (`None` for all)
        :param stop_on_error: Whether stop on a broken file(TODO)
        """
        self._fileblock = fileblock
        self._tag_filter = set(tag_filter) if tag_filter is not None else None
        self._stop_on_error = stop_on_error
        self._TYPES = {
            0: "embedding",
            1: "exception"
        }
        self._DATASETTYPES = {
            0: "image",
            1: "audio",
            2: "text"
        }

    def _decode_sample(self, dataset):
        _name = dataset.name
        _type = self._DATASETTYPES[dataset.type]
        _X = _decode_tensor(dataset.X)
        return dict(name=_name, type=_type, X=_X)

    def _decode_metadata(self, metadata):
        return Metadata(
            type=self._TYPES[metadata.type],
            content=metadata.content
        )

    def _decode_projector(self, projector: Iterable) -> Optional[ProjectorItem]:
        for pro in projector:
            _value = _decode_tensor(pro.value)
            _label = _decode_tensor(pro.label) if pro.HasField('label') else None
            yield ProjectorItem(
                tag=pro.tag,
                step=pro.step,
                wall_time=pro.WALL_TIME,
                value=_value,
                label=_label
            )

    def _check_tag(self, tag: str) -> bool:
        """
        Check if a tag matches the current tag filter
        :param tag: A string with tag
        :return: A boolean value.
        """
        return self._tag_filter is None or tag in self._tag_filter

    def read(self) -> ProjectorSummaryItem:
        summary = projector_pb2.SummaryProjector()
        summary.ParseFromString(self._fileblock.read())
        psi = ProjectorSummaryItem(
            metadata=self._decode_metadata(summary.metadata),
            sample=self._decode_sample(summary.sample)
            if summary.HasField("sample") else None,
            projectors=[item for item in self._decode_projector(summary.projector)
                        if item is not None and all([self._check_tag(item.tag)])]
        )
        return psi
