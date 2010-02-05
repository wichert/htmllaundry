from lxml.html.clean import Cleaner

DocumentCleaner = Cleaner(
            page_structure = False,
            remove_unknown_tags = False,
            allow_tags = [ "blockquote", "a", "img", "em", "p", "strong",
                           "h3", "h4", "h5", "ul", "ol", "li", "sub", "sup",
                           "abbr", "acronym", "dl", "dt", "dd", "cite",
                           "dft", "br", "table", "tr", "td", "th", "thead",
                           "tbody", "tfoot" ],
            safe_attrs_only = True,
            add_nofollow = True,
            scripts = False,
            javascript = False,
            comments = False,
            style = False,
            links = False, 
            meta = False,
            processing_instructions = False,
            frames = False,
            annoying_tags = False)


# Useful for line fields such as titles
LineCleaner = Cleaner(
            page_structure = False,
            safe_attrs_only = True,
            remove_unknown_tags = False, # Weird API..
            allow_tags = [ "em", "strong" ],
            add_nofollow = True,
            scripts = False,
            javascript = False,
            comments = False,
            style = False,
            processing_instructions = False,
            frames = False,
            annoying_tags = False)

CommentCleaner = Cleaner(
            page_structure = False,
            safe_attrs_only = True,
            remove_unknown_tags = False, # Weird API..
            allow_tags = [ "blockquote", "a", "em", "p", "strong" ],
            add_nofollow = True,
            scripts = False,
            javascript = False,
            comments = False,
            style = False,
            processing_instructions = False,
            frames = False,
            annoying_tags = False)


__all__ = [ "DocumentCleaner", "LineCleaner", "CommentCleaner"  ]

