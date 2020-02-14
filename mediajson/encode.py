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
This module contains methods and classes to extend json encoding to cover
timestamps, uuids, and fractions.

To make use of it either use the dumps, and dump functions in place of the
versions from the standard json module, or use the class NMOSJSONEncoder as
your encoder class.
"""

import uuid
import json
from json import JSONEncoder
from fractions import Fraction

from typing import Optional, Union, cast
from .typing import MediaJSONSerialisable, JSONSerialisable

from mediatimestamp.immutable import Timestamp, TimeOffset, TimeRange


__all__ = ["dump", "dumps",
           "encode_value",
           "JSONEncoder",
           "NMOSJSONEncoder"]


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


def encode_value(o: MediaJSONSerialisable,
                 return_no_encode=True) -> Union[MediaJSONSerialisable, Optional[JSONSerialisable]]:
    if isinstance(o, dict):
        if not return_no_encode:
            return None
        res = {}
        for key in o:
            res[key] = encode_value(o[key])
        return cast(MediaJSONSerialisable, res)
    elif isinstance(o, list):
        if not return_no_encode:
            return None
        return cast(MediaJSONSerialisable, [encode_value(v) for v in o])
    elif isinstance(o, uuid.UUID):
        return str(o)
    elif isinstance(o, Timestamp):
        return o.to_tai_sec_nsec()
    elif isinstance(o, TimeOffset):
        return o.to_sec_nsec()
    elif isinstance(o, TimeRange):
        return o.to_sec_nsec_range()
    elif isinstance(o, Fraction):
        return {"numerator": o.numerator,
                "denominator": o.denominator}
    else:
        return o if return_no_encode else None


def encode_value_or_fail(o: MediaJSONSerialisable) -> Optional[JSONSerialisable]:
    return cast(Optional[JSONSerialisable], encode_value(o, return_no_encode=False))


class NMOSJSONEncoder(JSONEncoder):
    def default(self, o: MediaJSONSerialisable) -> JSONSerialisable:
        result = cast(Optional[JSONSerialisable], encode_value_or_fail(o))
        if result is not None:
            return result
        else:
            return super(NMOSJSONEncoder, self).default(o)
