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

import uuid
import json
from json import JSONEncoder, JSONDecoder
from fractions import Fraction
import re

from typing import Type, Optional, Union, cast
from .typing import MediaJSONSerialisable, JSONSerialisable

import mediatimestamp.mutable as mutable
import mediatimestamp.immutable as immutable


UUID_REGEX = re.compile(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')


def dump(obj: MediaJSONSerialisable, fp, *args, **kwargs) -> None:
    _args = list(args)
    if 'cls' not in kwargs and len(args) < 7:
        kwargs['cls'] = NMOSJSONEncoder
    elif len(_args) >= 5 and _args[4] is None:
        _args = _args[0:4] + [NMOSJSONEncoder] + _args[5:]
    return json.dump(obj, fp, *_args, **kwargs)


def dumps(obj: MediaJSONSerialisable, *args, **kwargs) -> str:
    _args = list(args)
    if 'cls' not in kwargs and len(args) < 5:
        kwargs['cls'] = NMOSJSONEncoder
    elif len(args) >= 5 and args[4] is None:
        _args = _args[0:4] + [NMOSJSONEncoder] + _args[5:]
    return json.dumps(obj, *_args, **kwargs)


def _base_load(decoder_cls: Type[JSONDecoder], *args, **kwargs) -> None:
    _args = list(args)
    if 'cls' not in kwargs and len(args) < 3:
        kwargs['cls'] = decoder_cls
    elif len(args) >= 3 and args[2] is None:
        _args = _args[0:2] + [decoder_cls] + _args[3:]
    return json.load(*_args, **kwargs)


def _base_loads(decoder_cls: Type[JSONDecoder], *args, **kwargs) -> str:
    _args = list(args)
    if 'cls' not in kwargs and len(args) < 3:
        kwargs['cls'] = decoder_cls
    elif len(args) >= 3 and args[2] is None:
        _args = _args[0:2] + [decoder_cls] + _args[3:]
    return json.loads(*_args, **kwargs)


def encode_value(o: MediaJSONSerialisable,
                 return_no_encode=True) -> Union[MediaJSONSerialisable, Optional[JSONSerialisable]]:
    if isinstance(o, dict):
        if not return_no_encode:
            return None
        res = {}
        for key in o:
            res[key] = encode_value_or_fail(o[key])
        return cast(JSONSerialisable, res)
    elif isinstance(o, list):
        if not return_no_encode:
            return None
        return cast(JSONSerialisable, [encode_value_or_fail(v) for v in o])
    elif isinstance(o, uuid.UUID):
        return str(o)
    elif isinstance(o, mutable.Timestamp) or isinstance(o, immutable.Timestamp):
        return o.to_tai_sec_nsec()
    elif isinstance(o, mutable.TimeOffset) or isinstance(o, immutable.TimeOffset):
        return o.to_sec_nsec()
    elif isinstance(o, mutable.TimeRange) or isinstance(o, immutable.TimeRange):
        return o.to_sec_nsec_range()
    elif isinstance(o, Fraction):
        return {"numerator": o.numerator,
                "denominator": o.denominator}
    else:
        return o if return_no_encode else None


def encode_value_or_fail(o: MediaJSONSerialisable) -> Optional[JSONSerialisable]:
    return cast(Optional[JSONSerialisable], encode_value(o, return_no_encode=False))


def _base_decode_value(o: JSONSerialisable,
                       timestamp_cls: Type[immutable.Timestamp],
                       timeoffset_cls: Type[immutable.TimeOffset],
                       timerange_cls: Type[immutable.TimeRange]) -> MediaJSONSerialisable:
    if isinstance(o, dict):
        if len(o.keys()) == 2 and "numerator" in o and "denominator" in o:
            return Fraction(o['numerator'], o['denominator'])
        else:
            res = {}
            for key in o:
                res[key] = _base_decode_value(o[key], timestamp_cls, timeoffset_cls, timerange_cls)
            return res
    elif isinstance(o, list):
        return [_base_decode_value(v, timestamp_cls, timeoffset_cls, timerange_cls) for v in o]
    elif isinstance(o, str):
        if re.match(UUID_REGEX,
                    o):
            return uuid.UUID(o)
        elif re.match(r'^\d+:\d+$', o):
            return timestamp_cls.from_tai_sec_nsec(o)
        elif re.match(r'^(\+|-)\d+:\d+$', o):
            return timeoffset_cls.from_sec_nsec(o)
        elif re.match(r'^(\(|\[)?(\d+:\d+)?_(\d+:\d+)?(\)|\])?$', o):
            return timerange_cls.from_str(o)
        elif o == "()":
            return timerange_cls.never()
    return o


class NMOSJSONEncoder(JSONEncoder):
    def default(self, o: MediaJSONSerialisable) -> JSONSerialisable:
        result = cast(Optional[JSONSerialisable], encode_value_or_fail(o))
        if result is not None:
            return result
        else:
            return super(NMOSJSONEncoder, self).default(o)
