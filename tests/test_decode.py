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

import unittest
from io import StringIO
from uuid import UUID
from mediatimestamp import Timestamp, TimeRange
from fractions import Fraction

import mediajson


PURE_JSON_DATA = {
    "foo": "bar",
    "baz": ["boop", "beep"],
    "boggle": {"cat": u"\u732b",
               "kitten": u"\u5b50\u732b"},
    "numeric": 25,
    "boolean": True,
    "decimal": 0.44
}

PURE_JSON_STRING = '{"foo": "bar", "baz": ["boop", "beep"], "boggle": {"cat": "\\u732b", "kitten": "\\u5b50\\u732b"},' \
    ' "numeric": 25, "boolean": true, "decimal": 0.44}'

MEDIAJSON_DATA = {
    "foo": "bar",
    "baz": ["boop", "beep"],
    "boggle": {"cat": u"\u732b",
               "kitten": u"\u5b50\u732b"},
    "numeric": 25,
    "boolean": True,
    "decimal": 0.44,
    "uuid": UUID("b8b4a34f-3293-11e8-89c0-acde48001122"),
    "rational": Fraction(30000, 1001),
    "timestamp": Timestamp.from_sec_nsec("417798915:0"),
    "timeranges": [TimeRange(Timestamp(417798915, 0), Timestamp(417798916, 999), TimeRange.INCLUSIVE),
                   TimeRange(Timestamp(417798915, 0), Timestamp(417798916, 999), TimeRange.EXCLUSIVE),
                   TimeRange(Timestamp(417798915, 0), Timestamp(417798916, 999), TimeRange.INCLUDE_START),
                   TimeRange(Timestamp(417798915, 0), Timestamp(417798916, 999), TimeRange.INCLUDE_END),
                   TimeRange.never(),
                   TimeRange.eternity(),
                   TimeRange.from_start(Timestamp(417798915, 0), TimeRange.INCLUSIVE),
                   TimeRange.from_start(Timestamp(417798915, 0), TimeRange.EXCLUSIVE),
                   TimeRange.from_end(Timestamp(417798915, 0), TimeRange.INCLUSIVE),
                   TimeRange.from_end(Timestamp(417798915, 0), TimeRange.EXCLUSIVE)]
}

MEDIAJSON_STRING = '{"foo": "bar", "baz": ["boop", "beep"], "boggle": {"cat": "\\u732b", "kitten": "\\u5b50\\u732b"}, '\
    '"numeric": 25, "boolean": true, "decimal": 0.44, "uuid": "b8b4a34f-3293-11e8-89c0-acde48001122", '\
    '"rational": {"numerator": 30000, "denominator": 1001}, "timestamp": "417798915:0",'\
    '"timeranges": ["[417798915:0_417798916:999]", "(417798915:0_417798916:999)", "[417798915:0_417798916:999)", '\
    '"(417798915:0_417798916:999]", "()", "_", "[417798915:0_", "(417798915:0_", "_417798915:0]", "_417798915:0)"]}'


class TestJSONDecode(unittest.TestCase):
    def test_load_pure_json(self):
        fp = StringIO(PURE_JSON_STRING)

        decoded = mediajson.load(fp)

        self.assertEqual(PURE_JSON_DATA, decoded)

    def test_loads_pure_json(self):
        decoded = mediajson.loads(PURE_JSON_STRING)

        self.assertEqual(PURE_JSON_DATA, decoded)

    def test_load_mediajson(self):
        fp = StringIO(MEDIAJSON_STRING)

        decoded = mediajson.load(fp)

        self.assertEqual(MEDIAJSON_DATA, decoded)

    def test_loads_mediajson(self):
        decoded = mediajson.loads(MEDIAJSON_STRING)

        self.assertEqual(MEDIAJSON_DATA, decoded)
