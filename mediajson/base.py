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

from __future__ import absolute_import
from __future__ import print_function

import uuid
import json
from json import JSONEncoder
from fractions import Fraction
from six import string_types
import re

import mediatimestamp.mutable as mutable
import mediatimestamp.immutable as immutable


UUID_REGEX = re.compile(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')


def dump(*args, **kwargs):
    if 'cls' not in kwargs and len(args) < 7:
        kwargs['cls'] = NMOSJSONEncoder
    elif len(args) >= 7 and args[6] is None:
        args = args[0:6] + [NMOSJSONEncoder] + args[7:]
    return json.dump(*args, **kwargs)


def dumps(*args, **kwargs):
    if 'cls' not in kwargs and len(args) < 6:
        kwargs['cls'] = NMOSJSONEncoder
    elif len(args) >= 6 and args[5] is None:
        args = args[0:5] + [NMOSJSONEncoder] + args[6:]
    return json.dumps(*args, **kwargs)


def _base_load(decoder_cls, *args, **kwargs):
    if 'cls' not in kwargs and len(args) < 3:
        kwargs['cls'] = decoder_cls
    elif len(args) >= 3 and args[2] is None:
        args = args[0:2] + [decoder_cls] + args[3:]
    return json.load(*args, **kwargs)


def _base_loads(decoder_cls, *args, **kwargs):
    if 'cls' not in kwargs and len(args) < 3:
        kwargs['cls'] = decoder_cls
    elif len(args) >= 3 and args[2] is None:
        args = args[0:2] + [decoder_cls] + args[3:]
    return json.loads(*args, **kwargs)


def encode_value(o, return_no_encode=True):
    if isinstance(o, dict):
        if not return_no_encode:
            return None
        res = {}
        for key in o:
            res[key] = encode_value(o[key])
        return res
    elif isinstance(o, list):
        if not return_no_encode:
            return None
        return [encode_value(v) for v in o]
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


def _base_decode_value(o, timestamp_cls, timeoffset_cls, timerange_cls):
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
    elif isinstance(o, string_types):
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
    def default(self, o):
        result = encode_value(o, return_no_encode=False)
        if result is not None:
            return result
        else:
            return super(NMOSJSONEncoder, self).default(o)
