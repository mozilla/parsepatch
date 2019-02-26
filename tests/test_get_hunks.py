# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

# flake8: noqa W293
# Don't delete the trailing whitespace on this file. It's necessary for
# the tests. *The diffs contain trailing whitespace*.

import unittest

from parsepatch.patch import Patch


class GetHunksTest(unittest.TestCase):
    def setUp(self):
        self.knownCorrect = [
            {
                'filename': 'browser/components/urlbar/UrlbarInput.jsm',
                'src_start': 225,
                'src_end': 17,
                'dest_start': 225,
                'dest_end': 27,
                'diff': b"""\
 
   /**
    * Called by the view when a result is selected.
    *
    * @param {Event} event The event that selected the result.
    * @param {UrlbarMatch} result The result that was selected.
    */
   resultSelected(event, result) {
-    // TODO: Set the input value to the target url.
+    // Set the input value to the target url.
+    let val = result.url;
+    let uri;
+    try {
+      uri = Services.io.newURI(val);
+    } catch (ex) {}
+    if (uri) {
+      val = this.window.losslessDecodeURI(uri);
+    }
+    this.value = val;
+
     this.controller.resultSelected(event, result);
   }
 
   // Getters and Setters below.
 
   get focused() {
     return this.textbox.getAttribute("focused") == "true";
   }"""
            },
            {
                'filename': 'browser/components/urlbar/tests/browser/browser_UrlbarController_resultOpening.js',
                'src_start': 54,
                'src_end': 17,
                'dest_start': 54,
                'dest_end': 23,
                'diff': b"""\
   sandbox.stub(window, "switchToTabHavingURI").returns(true);
   sandbox.stub(window, "isTabEmpty").returns(false);
   sandbox.stub(window.gBrowser, "removeTab");
 
   const event = new MouseEvent("click", {button: 0});
   const url = "https://example.com/1";
   const result = new UrlbarMatch(UrlbarUtils.MATCH_TYPE.TAB_SWITCH, {url});
 
-  controller.resultSelected(event, result);
+  Assert.equal(gURLBar.value, "", "urlbar input is empty before selecting a result");
+  if (Services.prefs.getBoolPref("browser.urlbar.quantumbar", true)) {
+    gURLBar.resultSelected(event, result);
+    Assert.equal(gURLBar.value, url, "urlbar value updated for selected result");
+  } else {
+    controller.resultSelected(event, result);
+  }
 
   Assert.ok(window.switchToTabHavingURI.calledOnce,
     "Should have triggered switching to the tab");
 
   let args = window.switchToTabHavingURI.args[0];
 
   Assert.equal(args[0], url, "Should have passed the expected url");
   Assert.ok(!args[1], "Should not attempt to open a new tab");"""
            }
        ]

    def test_local(self):
        self.assertEqual(Patch.parse_file('tests/patches/8be2131ed183.patch', get_hunks=True), self.knownCorrect)

    def test_remote(self):
        self.assertEqual(Patch.parse_changeset('https://hg.mozilla.org/mozilla-central/raw-rev', '8be2131ed183', get_hunks=True), self.knownCorrect)
