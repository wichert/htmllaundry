import re
from lxml import etree
from lxml import html
from htmllaundry.cleaners import DocumentCleaner


TAG = re.compile(u"<.*?>")
ANCHORS = etree.XPath("descendant-or-self::a | descendant-or-self::x:a",
                      namespaces={'x':html.XHTML_NAMESPACE})
ALL_WHITESPACE = re.compile(r"^\s*$", re.UNICODE)


def isWhitespace(txt):
    """Utility method to test if txt is all whitespace or None."""
    return txt is None or bool(ALL_WHITESPACE.match(txt))



def StripMarkup(markup):
    """Strip all markup from a HTML fragment."""
    return TAG.sub(u"", markup)



def removeElement(el):
    parent=el.getparent()
    if el.tail:
        previous=el.getprevious()
        if previous is not None:
            if previous.tail:
                previous.tail+=el.tail
            else:
                previous.tail=el.tail
        else:
            if parent.text:
                parent.text+=el.tail
            else:
                parent.text=el.tail

    parent.remove(el)


def RemoveEmptyTags(doc):
    """Removes all empty tags from a HTML document. Javascript editors
    and browsers have a nasty habit of leaving stray tags around after
    their contents have been removed. This function removes all such
    empty tags, leaving only valid empty tags.

    In addition consecutive <br/> tags are folded into a single tag.
    This forces whitespace styling to be done using CSS instead of via an
    editor, which almost always produces better and more consistent results.
    """

    legal_empty_tags = frozenset(["br", "hr", "img", "input"])

    if hasattr(doc, "getroot"):
        doc=doc.getroot()

    def clean(doc):
        victims=[]
        for el in doc.iter():
            if el.tag=="br":
                preceding=el.getprevious()
                parent=el.getparent()

                if (preceding is None and not parent.text) or \
                        (preceding is not None and preceding.tag==el.tag and not preceding.tail) or \
                        (not el.tail and el.getnext() is None):
                    victims.append(el)
                    continue

            if el.tag in legal_empty_tags:
                continue

            if len(el)==0 and isWhitespace(el.text):
                victims.append(el)
                continue

        if victims and victims[0]==doc:
            doc.clear()
            return 0
        else:
            for victim in victims:
                removeElement(victim)

        return len(victims)

    while clean(doc):
        pass

    return doc



def StripOuterBreaks(doc):
    """Remove any toplevel break elements."""
    victims=[]

    for i in range(len(doc)):
        el=doc[i]
        if el.tag=="br":
            victims.append(el)

    for victim in victims:
        removeElement(victim)



def WrapText(doc, element='p'):
    """Make sure there is no unwrapped text at the top level. Any bare text
    found is wrapped in a `<p>` element.
    """
    def par(text):
        el=etree.Element(element)
        el.text=text
        return el
        
    if doc.text:
        doc.insert(0, par(doc.text))

    insertions=[]
    for i in range(len(doc)):
        el=doc[i]
        if not isWhitespace(el.tail):
            insertions.append((i, par(el.tail)))
            el.tail=None

    for (index, el) in reversed(insertions):
        doc.insert(index+1, el)




def sanitize(input, cleaner=DocumentCleaner, wrap='p'):
    """Cleanup markup using a given cleanup configuration.
       Unwrapped text will be wrapped with wrap parameter. 
    """
    if "body" not in cleaner.allow_tags:
        cleaner.allow_tags.append("body")

    input=u"<html><body>%s</body></html>" % input
    document=html.document_fromstring(input)
    bodies=[e for e in document if html._nons(e.tag)=="body"]
    body=bodies[0]

    cleaned=cleaner.clean_html(body)
    RemoveEmptyTags(cleaned)
    StripOuterBreaks(cleaned)

    if wrap is not None:
        if wrap in html.defs.tags:
            WrapText(cleaned, wrap)
        else:
            raise ValueError(
                "Invalid html tag provided for wrapping the sanitized text")

    output=u"".join([etree.tostring(fragment, encoding=unicode)
                     for fragment in cleaned.iterchildren()])
    if wrap is None and cleaned.text:
        output=cleaned.text+output

    return output



