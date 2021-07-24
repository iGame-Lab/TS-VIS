# -*- coding: UTF-8 -*-
# MIT License
#
# Copyright (c) 2019 Vadim Velicodnii
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from collections.abc import Iterable
from visparser.events_reader import EventsFileReader
from .event_parser import get_parser, get_graph


class SummaryReader(Iterable):
    """
    Iterates over events in all the files in the current logdir.
    """

    def __init__(self, fileblock, stop_on_error=False):
        """
        Initalize new summary reader
        :param fileblock: Event file block of Tensorboard
        :param tag_filter: A list of tags to leave (`None` for all)
        :param types: A list of types to get.
        :param stop_on_error: Whether stop on a broken file
        """
        self._fileblock = fileblock
        self._stop_on_error = stop_on_error

    def _decode_events(self, events: Iterable):
        """
        Convert events to `SummaryItem` instances
        :param events: An iterable with events objects
        :return: A generator with decoded events
            or `None`s if an event can't be decoded
        """
        for event in events:
            if event.HasField('graph_def'):
                yield get_graph(event)

            elif event.HasField('summary'):
                for value in event.summary.value:
                    yield get_parser(value, event.step, event.wall_time)

    def __iter__(self):
        """
        Iterate over events in all the files in the current logdir
        :return: A generator with `SummaryItem` objects
        """
        reader = EventsFileReader(self._fileblock)
        try:
            yield from (item for item in self._decode_events(reader) if item is not None)

        except Exception as e:
            if self._stop_on_error:
                raise
            else:  # file is read finish and exit
                pass
