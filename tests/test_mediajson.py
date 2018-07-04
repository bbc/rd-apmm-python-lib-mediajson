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

from __future__ import absolute_import
from __future__ import print_function

import unittest
import json
from six import StringIO
from uuid import UUID
from mediatimestamp import Timestamp
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
    "timestamp": Timestamp.from_sec_nsec("417798915:0")
}

MEDIAJSON_STRING = '{"foo": "bar", "baz": ["boop", "beep"], "boggle": {"cat": "\\u732b", "kitten": "\\u5b50\\u732b"}, '\
    '"numeric": 25, "boolean": true, "decimal": 0.44, "uuid": "b8b4a34f-3293-11e8-89c0-acde48001122", '\
    '"rational": {"numerator": 30000, "denominator": 1001}, "timestamp": "417798915:0"}'


class TestJSON(unittest.TestCase):
    def test_dump_pure_json(self):
        fp = StringIO()

        mediajson.dump(PURE_JSON_DATA, fp)

        decoded = json.loads(fp.getvalue())
        self.assertEqual(PURE_JSON_DATA, decoded)

    def test_dumps_pure_json(self):
        encoded = mediajson.dumps(PURE_JSON_DATA)
        decoded = json.loads(encoded)

        self.assertEqual(PURE_JSON_DATA, decoded)

    def test_load_pure_json(self):
        fp = StringIO(PURE_JSON_STRING)

        decoded = mediajson.load(fp)

        self.assertEqual(PURE_JSON_DATA, decoded)

    def test_loads_pure_json(self):
        decoded = mediajson.loads(PURE_JSON_STRING)

        self.assertEqual(PURE_JSON_DATA, decoded)

    def test_dump_mediajson(self):
        fp = StringIO()

        mediajson.dump(MEDIAJSON_DATA, fp)

        decoded = mediajson.loads(fp.getvalue())
        self.assertEqual(MEDIAJSON_DATA, decoded)

    def test_dumps_mediajson(self):
        encoded = mediajson.dumps(MEDIAJSON_DATA)
        decoded = mediajson.loads(encoded)

        self.assertEqual(MEDIAJSON_DATA, decoded)

    def test_load_mediajson(self):
        fp = StringIO(MEDIAJSON_STRING)

        decoded = mediajson.load(fp)

        self.assertEqual(MEDIAJSON_DATA, decoded)

    def test_loads_mediajson(self):
        decoded = mediajson.loads(MEDIAJSON_STRING)

        self.assertEqual(MEDIAJSON_DATA, decoded)
