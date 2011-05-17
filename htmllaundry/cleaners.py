from lxml.html.clean import Cleaner
from lxml.html.clean import _find_external_links


marker = []


class LaundryCleaner(Cleaner):
    link_target = marker

    def __call__(self, doc):
        super(LaundryCleaner, self).__call__(doc)
        if self.link_target is not marker:
            self.force_link_target(doc, self.link_target)

    def force_link_target(self, doc, target):
        for el in _find_external_links(doc):
            if target is None:
                if 'target' in el.attrib:
                    del el.attrib['target']
            else:
                el.set('target', target)


DocumentCleaner = LaundryCleaner(
            page_structure=False,
            remove_unknown_tags=False,
            allow_tags=['blockquote', 'a', 'img', 'em', 'p', 'strong',
                        'h3', 'h4', 'h5', 'ul', 'ol', 'li', 'sub', 'sup',
                        'abbr', 'acronym', 'dl', 'dt', 'dd', 'cite',
                        'dft', 'br', 'table', 'tr', 'td', 'th', 'thead',
                        'tbody', 'tfoot'],
            safe_attrs_only=True,
            add_nofollow=True,
            scripts=True,
            javascript=True,
            comments=False,
            style=True,
            links=False,
            meta=False,
            processing_instructions=False,
            frames=False,
            annoying_tags=False)


# Useful for line fields such as titles
LineCleaner = LaundryCleaner(
            page_structure=False,
            safe_attrs_only=True,
            remove_unknown_tags=False,  # Weird API..
            allow_tags=['em', 'strong'],
            add_nofollow=True,
            scripts=True,
            javascript=True,
            comments=False,
            style=True,
            processing_instructions=False,
            frames=False,
            annoying_tags=False)

CommentCleaner = LaundryCleaner(
            page_structure=False,
            safe_attrs_only=True,
            remove_unknown_tags=False,  # Weird API..
            allow_tags=['blockquote', 'a', 'em', 'p', 'strong'],
            add_nofollow=True,
            scripts=False,
            javascript=True,
            comments=False,
            style=True,
            processing_instructions=False,
            frames=False,
            annoying_tags=False,
            link_target="_blank")


__all__ = ['DocumentCleaner', 'LineCleaner', 'CommentCleaner']
