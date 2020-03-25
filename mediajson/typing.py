#
# Copyright 2018 British Broadcasting Corporation
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
#

"""\
Types used for type checking other parts of the library
"""

from typing import Any, Union, Sequence, Mapping
from typing_extensions import TypedDict

from decimal import Decimal
from numbers import Rational
from fractions import Fraction
from uuid import UUID
from mediatimestamp.immutable import TimeOffset, TimeRange


__all__ = ["RationalTypes",
           "MediaJSONSerialisable",
           "JSONSerialisable",
           "FractionDict"]

# These are the types that can be freely converted into a Fraction
RationalTypes = Union[str, float, Decimal, Rational]

# TODO: Move this into mediajson, and make it actually describe what is serialisable.
# At current due to weaknesses in mypy this is rather limited and only provides type safety for a limited depth of json
# strucure
#
#  Hopefully at some point in the future proper recursive type definitions will be supported
#  Until that time we simply assume none of our json structures are all that deep
_MediaJSONSerialisable_value = Union[str, int, float, UUID, TimeOffset, TimeRange, Fraction]
# This means that type checking stops at the fourth level
_MediaJSONSerialisable0 = Union[_MediaJSONSerialisable_value, Sequence[Any], Mapping[str, Any]]
_MediaJSONSerialisable1 = Union[_MediaJSONSerialisable_value, Sequence[_MediaJSONSerialisable0],
                                Mapping[str, _MediaJSONSerialisable0]]
_MediaJSONSerialisable2 = Union[_MediaJSONSerialisable_value, Sequence[_MediaJSONSerialisable1],
                                Mapping[str, _MediaJSONSerialisable1]]
_MediaJSONSerialisable3 = Union[_MediaJSONSerialisable_value, Sequence[_MediaJSONSerialisable2],
                                Mapping[str, _MediaJSONSerialisable2]]
_MediaJSONSerialisable4 = Union[_MediaJSONSerialisable_value, Sequence[_MediaJSONSerialisable3],
                                Mapping[str, _MediaJSONSerialisable3]]
MediaJSONSerialisable = _MediaJSONSerialisable4


# This mechanism does the same for the standard JSON serialisability
_JSONSerialisable_value = Union[str, int, float]
# This means that type checking stops at the fourth level
_JSONSerialisable0 = Union[_JSONSerialisable_value, Sequence[Any], Mapping[str, Any]]
_JSONSerialisable1 = Union[_JSONSerialisable_value, Sequence[_JSONSerialisable0],
                           Mapping[str, _JSONSerialisable0]]
_JSONSerialisable2 = Union[_JSONSerialisable_value, Sequence[_JSONSerialisable1],
                           Mapping[str, _JSONSerialisable1]]
_JSONSerialisable3 = Union[_JSONSerialisable_value, Sequence[_JSONSerialisable2],
                           Mapping[str, _JSONSerialisable2]]
_JSONSerialisable4 = Union[_JSONSerialisable_value, Sequence[_JSONSerialisable3],
                           Mapping[str, _JSONSerialisable3]]
JSONSerialisable = _JSONSerialisable4


# This type defines a dictionary that can be converted into a Fraction by mediaJSON
class FractionDict (TypedDict):
    numerator: int
    denominator: int
