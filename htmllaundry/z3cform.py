from zope.interface import implements
from zope.component import adapts
from zope.schema.interfaces import IText
from zope.schema import Text
from z3c.form.converter import FieldDataConverter
from z3c.form.interfaces import IWidget
from htmllaundry.utils import sanitize


class IHtmlText(IText):
    pass


class HtmlText(Text):
    """A HTML field. This is similar to a standard Text field, but will
    sanitize all markup passed into it.
    """
    implements(IHtmlText)


class HtmlDataConverter(FieldDataConverter):
    """z3c.form data convertor for HTML forms. This convertor
    sanitizes all input, guaranteeing simple and valid markup
    as a result.
    """
    adapts(IHtmlText, IWidget)

    def toFieldValue(self, value):
        data = super(HtmlDataConverter, self).toFieldValue(value)
        if data:
            data = sanitize(data)
        return data
