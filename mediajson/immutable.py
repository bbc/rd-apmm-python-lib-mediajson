# Copyright 2019 British Broadcasting Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This module contains methods and classes to extend json encoding and decoding
to cover _immutable_ timestamps, uuids, and fractions.

To make use of it either use the dumps, loads, dump, and load functions in
place of the versions from the standard json module, or use the classes
NMOSJSONEncoder and NMOSJSONDecoder as your encoder and decoder classes.
"""

import mediatimestamp.immutable as immutable
from json import JSONEncoder, JSONDecoder
from typing import Tuple

from .base import dump, dumps, encode_value
from .base import _base_load, _base_loads, _base_decode_value
from .base import NMOSJSONEncoder
from .typing import JSONSerialisable, MediaJSONSerialisable

__all__ = ["dump", "dumps", "load", "loads",
           "encode_value", "decode_value",
           "JSONEncoder", "JSONDecoder",
           "NMOSJSONEncoder", "NMOSJSONDecoder"]


def load(*args, **kwargs) -> None:
    return _base_load(NMOSJSONDecoder, *args, **kwargs)


def loads(*args, **kwargs) -> str:
    return _base_loads(NMOSJSONDecoder, *args, **kwargs)


def decode_value(o: JSONSerialisable) -> MediaJSONSerialisable:
    return _base_decode_value(o, immutable.Timestamp, immutable.TimeOffset, immutable.TimeRange)


class NMOSJSONDecoder(JSONDecoder):
    def raw_decode(self, s: str, *args, **kwargs) -> Tuple[MediaJSONSerialisable, int]:
        value: JSONSerialisable
        (value, offset) = super(NMOSJSONDecoder, self).raw_decode(s,
                                                                  *args,
                                                                  **kwargs)
        return (decode_value(value), offset)
