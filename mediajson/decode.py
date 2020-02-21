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
This module contains methods and classes to extend json decoding to cover
timestamps, uuids, and fractions.

To make use of it either use the loads and load functions in place of the
versions from the standard json module, or use the class NMOSJSONDecoder as
your decoder class.
"""

import uuid
import json
from json import JSONDecoder
from fractions import Fraction
import re

from typing import Tuple
from .typing import MediaJSONSerialisable, JSONSerialisable

from mediatimestamp.immutable import Timestamp, TimeOffset, TimeRange


__all__ = ["load", "loads",
           "decode_value",
           "JSONDecoder",
           "NMOSJSONDecoder"]


UUID_REGEX = re.compile(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')


def load(*args, **kwargs) -> MediaJSONSerialisable:
    _args = list(args)
    if 'cls' not in kwargs and len(args) < 3:
        kwargs['cls'] = NMOSJSONDecoder
    elif len(args) >= 3 and args[2] is None:
        _args = _args[0:2] + [NMOSJSONDecoder] + _args[3:]
    return json.load(*_args, **kwargs)


def loads(*args, **kwargs) -> MediaJSONSerialisable:
    _args = list(args)
    if 'cls' not in kwargs and len(args) < 3:
        kwargs['cls'] = NMOSJSONDecoder
    elif len(args) >= 3 and args[2] is None:
        _args = _args[0:2] + [NMOSJSONDecoder] + _args[3:]
    return json.loads(*_args, **kwargs)


def decode_value(o: JSONSerialisable) -> MediaJSONSerialisable:
    if isinstance(o, dict):
        if len(o.keys()) == 2 and "numerator" in o and "denominator" in o:
            return Fraction(o['numerator'], o['denominator'])
        else:
            res = {}
            for key in o:
                res[key] = decode_value(o[key])
            return res
    elif isinstance(o, list):
        return [decode_value(v) for v in o]
    elif isinstance(o, str):
        if re.match(UUID_REGEX,
                    o):
            return uuid.UUID(o)
        elif re.match(r'^\d+:\d+$', o):
            return Timestamp.from_tai_sec_nsec(o)
        elif re.match(r'^(\+|-)\d+:\d+$', o):
            return TimeOffset.from_sec_nsec(o)
        elif re.match(r'^(\(|\[)?(\d+:\d+)?_(\d+:\d+)?(\)|\])?$', o):
            return TimeRange.from_str(o)
        elif o == "()":
            return TimeRange.never()
    return o


class NMOSJSONDecoder(JSONDecoder):
    def raw_decode(self, s: str, *args, **kwargs) -> Tuple[MediaJSONSerialisable, int]:
        value: JSONSerialisable
        (value, offset) = super(NMOSJSONDecoder, self).raw_decode(s,
                                                                  *args,
                                                                  **kwargs)
        return (decode_value(value), offset)
