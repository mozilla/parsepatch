# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import unittest
from parsepatch.patch import Patch
import whatthepatch as wtp


class PatchTest(unittest.TestCase):

    def readfile(self, filename):
        with open(filename, 'r') as In:
            patch = In.read()
            return patch

    def get_touched(self, patch):
        res = {}
        for diff in wtp.parse_patch(patch):
            h = diff.header
            new_p = h.new_path[2:] if h.new_path.startswith('b/') else h.new_p
            res[new_p] = added = []
            if diff.changes:
                for old_line, new_line, _ in diff.changes:
                    if not old_line and new_line:
                        added.append(new_line)

        return res

    def compare(self, rev, r1, r2):
        for p, i in r1.items():
            if 'added' in i:
                added = list(sorted(set(i['added']) | set(i['touched'])))
                self.assertEqual(added, r2[p])
            elif 'new' in i:
                # we've a new file
                self.assertTrue(p in r2)

    def test(self):
        revs = ['c4c0ad8b3eaa', 'f045ac9f76cf',
                'c58e9e70f971', 'd7a700707ddb',
                '81d3e4a2f3f3', '7e60ad275b73',
                'f9b391e62608', '7dabae5e261a',
                'c6f9187b0b2e', 'd4f80c4ba719']
        for rev in revs:
            path = 'tests/patches/{}.patch'.format(rev)
            patch = self.readfile(path)
            r1 = Patch.parse_patch(patch, skip_comments=False)
            r2 = self.get_touched(patch)
            self.compare(rev, r1, r2)
