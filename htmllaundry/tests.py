import unittest
import six

class Mock:
    pass

class StripMarkupTests(unittest.TestCase):
    def StripMarkup(self, *a, **kw):
        from htmllaundry.utils import StripMarkup
        return StripMarkup(*a, **kw)

    def testEmpty(self):
        obj=Mock()
        obj.description=six.u("")
        self.assertEqual(self.StripMarkup(six.u("")), six.u(""))

    def testNoMarkup(self):
        self.assertEqual(self.StripMarkup(six.u("Test")), six.u("Test"))

    def testSingleTag(self):
        self.assertEqual(self.StripMarkup(six.u("Test <em>me</me>")), six.u("Test me"))

    def testMultipleTags(self):
        self.assertEqual(
                self.StripMarkup(six.u("Test <em>me</me> <strong>now</strong>")),
                six.u("Test me now"))

    def testStrayBracket(self):
        self.assertEqual(
                self.StripMarkup(six.u("Test <em>me</em> >")),
                six.u("Test me >"))



class RemoveEmptyTagsTests(unittest.TestCase):
    def _remove(self, str):
        from htmllaundry.utils import RemoveEmptyTags
        import lxml.etree
        fragment=lxml.etree.fromstring(str)
        fragment=RemoveEmptyTags(fragment)
        return lxml.etree.tostring(fragment, encoding=unicode)

    def testRemoveEmptyParagraphElement(self):
        self.assertEqual(self._remove(six.u("<div><p/></div>")), six.u("<div/>"))

    def testRemoveEmptyParagraph(self):
        self.assertEqual(self._remove(six.u("<div><p></p></div>")), six.u("<div/>"))

    def testRemoveParagraphWithWhitespace(self):
        self.assertEqual(self._remove(six.u("<div><p>  </p></div>")), six.u("<div/>"))
        
    def testRemoveParagraphWithUnicodeWhitespace(self):
        self.assertEqual(self._remove(six.u("<div><p> \xa0 </p></div>")), six.u("<div/>"))
        
    def testKeepEmptyImageElement(self):
        self.assertEqual(self._remove(six.u("<div><img src='image'/></div>")),
                six.u('<div><img src="image"/></div>'))

    def testCollapseBreaks(self):
        self.assertEqual(self._remove(six.u("<body><p>one<br/><br/>two</p></body>")), six.u("<body><p>one<br/>two</p></body>"))

    def testNestedData(self):
        self.assertEqual(self._remove(six.u("<div><h3><bad/></h3><p>Test</p></div>")), six.u("<div><p>Test</p></div>"))

    def testKeepElementsWithTail(self):
        self.assertEqual(self._remove(six.u("<body>One<br/> two<br/> three</body>")),
                                      six.u("<body>One<br/> two<br/> three</body>"))

    def testTrailingBreak(self):
        self.assertEqual(self._remove(six.u("<div>Test <br/></div>")), six.u("<div>Test </div>"))

    def testLeadingBreak(self):
        self.assertEqual(self._remove(six.u("<div><br/>Test</div>")), six.u("<div>Test</div>"))



class ForceLinkTargetTests(unittest.TestCase):
    def force_link_target(self, str, target="_blank"):
        import lxml.etree
        from htmllaundry.cleaners import LaundryCleaner
        fragment=lxml.etree.fromstring(str)
        cleaner=LaundryCleaner()
        cleaner.force_link_target(fragment, target)
        return lxml.etree.tostring(fragment, encoding=unicode)

    def testNoAnchor(self):
        self.assertEqual(self.force_link_target(six.u("<div><p/></div>")), six.u("<div><p/></div>"))

    def testAddTarget(self):
        self.assertEqual(self.force_link_target(six.u('<div><a href="http://example.com"/></div>'), "_blank"),
                six.u('<div><a href="http://example.com" target="_blank"/></div>'))

    def testRemoveTarget(self):
        self.assertEqual(
                self.force_link_target(six.u('<div><a target="_blank" href="http://example.com"/></div>'), None),
                six.u('<div><a href="http://example.com"/></div>'))



class StripOuterBreakTests(unittest.TestCase):
    def _strip(self, str):
        import lxml.etree
        from htmllaundry.utils import StripOuterBreaks
        fragment=lxml.etree.fromstring(str)
        StripOuterBreaks(fragment)
        return lxml.etree.tostring(fragment, encoding=unicode)

    def testNoBreak(self):
        self.assertEqual(self._strip("<body>Dummy text</body>"), "<body>Dummy text</body>")

    def testTrailingBreak(self):
        self.assertEqual(self._strip("<body>Dummy text<br/></body>"), "<body>Dummy text</body>")

    def testLeadingBreak(self):
        self.assertEqual(self._strip("<body><br/>Dummy text</body>"), "<body>Dummy text</body>")

    def testBreakAfterElement(self):
        self.assertEqual(self._strip("<body><p>Dummy</p><br/>text</body>"), "<body><p>Dummy</p>text</body>")



class SanizeTests(unittest.TestCase):
    def sanitize(self, *a, **kw):
        from htmllaundry.utils import sanitize
        return sanitize(*a, **kw)

    def testEmpty(self):
        self.assertEqual(self.sanitize(six.u("")), six.u(""))

    def testParagraph(self):
        self.assertEqual(self.sanitize(six.u("<p>Test</p>")), six.u("<p>Test</p>"))

    def testParagraphCustomWrapperNotUsedIfAlreadyWrapped(self):
        self.assertEqual(self.sanitize(six.u("<p>Test</p>"), wrap="span"), six.u("<p>Test</p>"))

    def testParagraphWithWhitespace(self):
        self.assertEqual(
                self.sanitize(six.u("<p>Test</p>\n<p>\xa0</p>\n")),
                six.u("<p>Test</p>\n\n"))

    def testLeadingBreak(self):
        self.assertEqual(
                self.sanitize(six.u("<br/><p>Test</p>")),
                six.u("<p>Test</p>"))

    def testHeaderAndText(self):
        self.assertEqual(
                self.sanitize(six.u("<h3>Title</h3><p>Test</p>")),
                six.u("<h3>Title</h3><p>Test</p>"))

    def testUnwrappedText(self):
        self.assertEqual(
                self.sanitize(six.u("Hello, World")),
                six.u("<p>Hello, World</p>"))

    def testUnwrappedTextWithCustomWrapper(self):
        self.assertEqual(
                self.sanitize(six.u("Hello, World"), wrap="strong"),
                six.u("<strong>Hello, World</strong>"))

    def testTrailingUnwrappedText(self):
        self.assertEqual(
                self.sanitize(six.u("<p>Hello,</p> World")),
                six.u("<p>Hello,</p><p> World</p>"))

    def testTrailingUnwrappedTextWithCustomWrapper(self):
        self.assertEqual(
                self.sanitize(six.u("<p>Hello,</p> World"), wrap="b"),
                six.u("<p>Hello,</p><b> World</b>"))

    def testUnwrappedTextEverywhere(self):
        self.assertEqual(
                self.sanitize(six.u("Hello, <p>you</p> nice <em>person</em>.")),
                six.u("<p>Hello, </p><p>you</p><p> nice </p><em>person</em><p>.</p>"))

    def testUnwrappedTextEverywhereWithCustomWrapper(self):
        self.assertEqual(
                self.sanitize(six.u("Hello, <p>you</p> nice <em>person</em>."), wrap="div"),
                six.u("<div>Hello, </div><p>you</p><div> nice </div><em>person</em><div>.</div>"))

    def testStripStyleAttributes(self):
        self.assertEqual(
                self.sanitize(six.u('<p style=\"text-weight: bold\">Hello</p>')),
                six.u('<p>Hello</p>'))

    def testJavascriptLink(self):
        self.assertEqual(
                self.sanitize(six.u('<p><a href="javascript:alert(\'I am evil\')">click me</a></p>')),
                six.u('<p><a href="">click me</a></p>'))

    def testSkipWrapping(self):
        self.assertEqual(
                self.sanitize(six.u("Hello, <em>you</em> nice <em>person</em>."), wrap=None),
                six.u("Hello, <em>you</em> nice <em>person</em>."))

    def testRejectBadWrapElement(self):
        self.assertRaises(ValueError, self.sanitize, six.u("<p>Hello,</p> World"), wrap="xxx")
        self.assertRaises(ValueError, self.sanitize, six.u("Hello, <em>you</em> nice <em>person</em>."), wrap="")


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

