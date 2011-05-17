import unittest

class Mock:
    pass

class StripMarkupTests(unittest.TestCase):
    def StripMarkup(self, *a, **kw):
        from htmllaundry.utils import StripMarkup
        return StripMarkup(*a, **kw)

    def testEmpty(self):
        obj=Mock()
        obj.description=u""
        self.assertEqual(self.StripMarkup(u""), u"")

    def testNoMarkup(self):
        self.assertEqual(self.StripMarkup(u"Test"), u"Test")

    def testSingleTag(self):
        self.assertEqual(self.StripMarkup(u"Test <em>me</me>"), u"Test me")

    def testMultipleTags(self):
        self.assertEqual(
                self.StripMarkup(u"Test <em>me</me> <strong>now</strong>"),
                u"Test me now")

    def testStrayBracket(self):
        self.assertEqual(
                self.StripMarkup(u"Test <em>me</em> >"),
                u"Test me >")



class RemoveEmptyTagsTests(unittest.TestCase):
    def _remove(self, str):
        from htmllaundry.utils import RemoveEmptyTags
        import lxml.etree
        fragment=lxml.etree.fromstring(str)
        fragment=RemoveEmptyTags(fragment)
        return lxml.etree.tostring(fragment, encoding=unicode)

    def testRemoveEmptyParagraphElement(self):
        self.assertEqual(self._remove(u"<div><p/></div>"), u"<div/>")

    def testRemoveEmptyParagraph(self):
        self.assertEqual(self._remove(u"<div><p></p></div>"), u"<div/>")

    def testRemoveParagraphWithWhitespace(self):
        self.assertEqual(self._remove(u"<div><p>  </p></div>"), u"<div/>")
        
    def testRemoveParagraphWithUnicodeWhitespace(self):
        self.assertEqual(self._remove(u"<div><p> \xa0 </p></div>"), u"<div/>")
        
    def testKeepEmptyImageElement(self):
        self.assertEqual(self._remove(u"<div><img src='image'/></div>"), u'<div><img src="image"/></div>')

    def testCollapseBreaks(self):
        self.assertEqual(self._remove(u"<body><p>one<br/><br/>two</p></body>"), u"<body><p>one<br/>two</p></body>")

    def testNestedData(self):
        self.assertEqual(self._remove(u"<div><h3><bad/></h3><p>Test</p></div>"), u"<div><p>Test</p></div>")

    def testKeepElementsWithTail(self):
        self.assertEqual(self._remove(u"<body>One<br/> two<br/> three</body>"),
                                      u"<body>One<br/> two<br/> three</body>")

    def testTrailingBreak(self):
        self.assertEqual(self._remove(u"<div>Test <br/></div>"), u"<div>Test </div>")

    def testLeadingBreak(self):
        self.assertEqual(self._remove(u"<div><br/>Test</div>"), u"<div>Test</div>")



class ForceLinkTargetTests(unittest.TestCase):
    def force_link_target(self, str, target="_blank"):
        import lxml.etree
        from htmllaundry.cleaners import LaundryCleaner
        fragment=lxml.etree.fromstring(str)
        cleaner=LaundryCleaner()
        cleaner.force_link_target(fragment, target)
        return lxml.etree.tostring(fragment, encoding=unicode)

    def testNoAnchor(self):
        self.assertEqual(self.force_link_target(u"<div><p/></div>"), u"<div><p/></div>")

    def testAddTarget(self):
        self.assertEqual(self.force_link_target(u'<div><a href="http://example.com"/></div>', "_blank"),
                u'<div><a href="http://example.com" target="_blank"/></div>')

    def testRemoveTarget(self):
        self.assertEqual(self.force_link_target(u'<div><a target="_blank" href="http://example.com"/></div>', None),
                u'<div><a href="http://example.com"/></div>')



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
        self.assertEqual(self.sanitize(u""), u"")

    def testParagraph(self):
        self.assertEqual(self.sanitize(u"<p>Test</p>"), u"<p>Test</p>")

    def testParagraphCustomWrapperNotUsedIfAlreadyWrapped(self):
        self.assertEqual(self.sanitize(u"<p>Test</p>", wrap="span"), u"<p>Test</p>")

    def testParagraphWithWhitespace(self):
        self.assertEqual(
                self.sanitize(u"<p>Test</p>\n<p>\xa0</p>\n"),
                u"<p>Test</p>\n\n")

    def testLeadingBreak(self):
        self.assertEqual(
                self.sanitize(u"<br/><p>Test</p>"),
                u"<p>Test</p>")

    def testHeaderAndText(self):
        self.assertEqual(
                self.sanitize(u"<h3>Title</h3><p>Test</p>"),
                u"<h3>Title</h3><p>Test</p>")

    def testUnwrappedText(self):
        self.assertEqual(
                self.sanitize(u"Hello, World"),
                u"<p>Hello, World</p>")

    def testUnwrappedTextWithCustomWrapper(self):
        self.assertEqual(
                self.sanitize(u"Hello, World", wrap="strong"),
                u"<strong>Hello, World</strong>")

    def testTrailingUnwrappedText(self):
        self.assertEqual(
                self.sanitize(u"<p>Hello,</p> World"),
                u"<p>Hello,</p><p> World</p>")

    def testTrailingUnwrappedTextWithCustomWrapper(self):
        self.assertEqual(
                self.sanitize(u"<p>Hello,</p> World", wrap="b"),
                u"<p>Hello,</p><b> World</b>")

    def testUnwrappedTextEverywhere(self):
        self.assertEqual(
                self.sanitize(u"Hello, <p>you</p> nice <em>person</em>."),
                u"<p>Hello, </p><p>you</p><p> nice </p><em>person</em><p>.</p>")

    def testUnwrappedTextEverywhereWithCustomWrapper(self):
        self.assertEqual(
                self.sanitize(u"Hello, <p>you</p> nice <em>person</em>.", wrap="div"),
                u"<div>Hello, </div><p>you</p><div> nice </div><em>person</em><div>.</div>")

    def testStripStyleAttributes(self):
        self.assertEqual(
                self.sanitize(u'<p style=\"text-weight: bold\">Hello</p>'),
                u'<p>Hello</p>')

    def testJavascriptLink(self):
        self.assertEqual(
                self.sanitize(u'<p><a href="javascript:alert(\'I am evil\')">click me</a></p>'),
                u'<p><a href="">click me</a></p>')

    def testSkipWrapping(self):
        self.assertEqual(
                self.sanitize(u"Hello, <em>you</em> nice <em>person</em>.", wrap=None),
                u"Hello, <em>you</em> nice <em>person</em>.")

    def testRejectBadWrapElement(self):
        self.assertRaises(ValueError, self.sanitize, u"<p>Hello,</p> World", wrap="xxx")
        self.assertRaises(ValueError, self.sanitize, u"Hello, <em>you</em> nice <em>person</em>.", wrap="")


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

