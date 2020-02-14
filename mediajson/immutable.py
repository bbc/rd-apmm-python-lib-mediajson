# Copyright 2017 British Broadcasting Corporation
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
For backwards compatibility all of the methods and classes in mediajson
are also available in mediajson.immutable.

This may eventually go away, but will remain for the duration of major version 2"""

from json import JSONEncoder, JSONDecoder

from .encode import dump, dumps, encode_value, NMOSJSONEncoder
from .decode import load, loads, decode_value, NMOSJSONDecoder


__all__ = ["dump", "dumps", "load", "loads",
           "encode_value", "decode_value",
           "JSONEncoder", "JSONDecoder",
           "NMOSJSONEncoder", "NMOSJSONDecoder"]
