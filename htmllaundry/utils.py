import re
from lxml import etree
from lxml import html
from htmllaundry.cleaners import DocumentCleaner


TAG = re.compile(u"<.*?>")
ANCHORS = etree.XPath("descendant-or-self::a | descendant-or-self::x:a",
                      namespaces={'x':html.XHTML_NAMESPACE})


def StripMarkup(markup):
    """Strip all markup from a HTML fragment."""
    return TAG.sub(u"", markup)



def ForceLinkTarget(doc, target="_blank"):
    """Force a target on links in a HTML document. If `None` is
    given as target all target attributes are removed instead."""
    for el in ANCHORS(doc):
        if target is None:
            if "target" in el.attrib:
                del el.attrib["target"]
        else:
            el.set("target", target)


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
            if el.tag=="br" and not el.tail:
                preceding=el.getprevious()
                if preceding is not None and preceding.tag==el.tag:
                    victims.append(el)
                    continue

                next=el.getnext()
                if next is None or next.tag==el.tag:
                    victims.append(el)
                    continue

            if el.tag in legal_empty_tags:
                continue

            if len(el)==0 and (el.text is None or not el.text.strip()):
                victims.append(el)
                continue

        if victims and victims[0]==doc:
            doc.clear()
            return 0
        else:
            for victim in victims:
                victim.getparent().remove(victim)

        return len(victims)

    while clean(doc):
        pass

    return doc



def WrapText(doc):
    """Make sure there is no unwrapped text at the top level. Any bare text
    found is wrapped in a `<p>` element.
    """
    def par(text):
        el=etree.Element("p")
        el.text=text
        return el
        
    if doc.text:
        doc.insert(0, par(doc.text))

    insertions=[]
    for i in range(len(doc)):
        el=doc[i]
        if el.tail:
            insertions.append((i, par(el.tail)))
            el.tail=None

    for (index, el) in reversed(insertions):
        doc.insert(index+1, el)




def sanitize(input, cleaner=DocumentCleaner):
    """Cleanup markup using a given cleanup configuration."""
    if "body" not in cleaner.allow_tags:
        cleaner.allow_tags.append("body")

    input=u"<html><body>%s</body></html>" % input
    document=html.document_fromstring(input)
    bodies=[e for e in document if html._nons(e.tag)=="body"]
    body=bodies[0]

    cleaned=cleaner.clean_html(body)
    RemoveEmptyTags(cleaned)
    WrapText(cleaned)
    ForceLinkTarget(cleaned)

    output=u"".join([etree.tostring(fragment, encoding=unicode)
                     for fragment in cleaned.iterchildren()])

    return output



