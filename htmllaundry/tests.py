import unittest
import lxml.etree
from htmllaundry.utils import RemoveEmptyTags
from htmllaundry.utils import ForceLinkTarget
from htmllaundry.utils import StripMarkup
from htmllaundry.utils import sanitize

class Mock:
    pass


class StripMarkupTests(unittest.TestCase):
    def testEmpty(self):
        obj=Mock()
        obj.description=u""
        self.assertEqual(StripMarkup(u""), u"")

    def testNoMarkup(self):
        self.assertEqual(StripMarkup(u"Test"), u"Test")

    def testSingleTag(self):
        self.assertEqual(StripMarkup(u"Test <em>me</me>"), u"Test me")

    def testMultipleTags(self):
        self.assertEqual(StripMarkup(u"Test <em>me</me> <strong>now</strong>"),
                         u"Test me now")

    def testStrayBracket(self):
        self.assertEqual(StripMarkup(u"Test <em>me</em> >") , u"Test me >")



class RemoveEmptyTagsTests(unittest.TestCase):
    def _remove(self, str):
        fragment=lxml.etree.fromstring(str)
        fragment=RemoveEmptyTags(fragment)
        return lxml.etree.tostring(fragment, encoding=unicode)

    def testRemoveEmptyParagraphElement(self):
        self.assertEqual(self._remove(u"<div><p/></div>"), u"<div/>")

    def testRemoveEmptyParagraph(self):
        self.assertEqual(self._remove(u"<div><p></p></div>"), u"<div/>")

    def testRemoveParagraphWithWhitespace(self):
        self.assertEqual(self._remove(u"<div><p>  </p></div>"), u"<div/>")

    def testKeepEmptyBreakElement(self):
        self.assertEqual(self._remove(u"<div><br/></div>"), u"<div><br/></div>")
        
    def testKeepEmptyImageElement(self):
        self.assertEqual(self._remove(u"<div><img src='image'/></div>"), u'<div><img src="image"/></div>')

    def testCollapseBreaks(self):
        self.assertEqual(self._remove(u"<div><br/><br/></div>"), u"<div><br/></div>")

    def testNestedData(self):
        self.assertEqual(self._remove(u"<div><h3><bad/></h3> <p>Test</p></div>"), u"<div><p>Test</p></div>")

    def testKeepElementsWithTail(self):
        self.assertEqual(self._remove(u"<body>One<br/> two<br/> three</body>"),
                                      u"<body>One<br/> two<br/> three</body>")




class ForceLinkTargetTests(unittest.TestCase):
    def _force(self, str, target="_blank"):
        fragment=lxml.etree.fromstring(str)
        ForceLinkTarget(fragment, target=target)
        return lxml.etree.tostring(fragment, encoding=unicode)

    def testNoAnchor(self):
        self.assertEqual(self._force(u"<div><p/></div>"), u"<div><p/></div>")

    def testAddTarget(self):
        self.assertEqual(self._force(u"<div><a/></div>"),
                         u'<div><a target="_blank"/></div>')

    def testRemoveTarget(self):
        self.assertEqual(self._force(u"<div><a target='_blank'/></div>", None),
                         u"<div><a/></div>")



class SanizeTests(unittest.TestCase):
    def testEmpty(self):
        self.assertEqual(sanitize(u""), u"")

    def testParagraph(self):
        self.assertEqual(sanitize(u"<p>Test</p>"), u"<p>Test</p>")

    def testParagraphWithWhitespace(self):
        self.assertEqual(sanitize(u"<p>  </p>"), u"")

    def testHeaderAndText(self):
        self.assertEqual(sanitize(u"<h3>Title</h3><p>Test</p>"),
                         u"<h3>Title</h3><p>Test</p>")

    def testUnwrappedText(self):
        self.assertEqual(sanitize(u"Hello, World"), u"<p>Hello, World</p>")

    def testTrailingUnwrappedText(self):
        self.assertEqual(sanitize(u"<p>Hello,</p> World"), u"<p>Hello,</p><p> World</p>")

    def testUnwrappedTextEverywhere(self):
        self.assertEqual(sanitize(u"Hello, <p>you</p> nice <em>person</em>."),
                u"<p>Hello, </p><p>you</p><p> nice </p><em>person</em><p>.</p>")



def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

