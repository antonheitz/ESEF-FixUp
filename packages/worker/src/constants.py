from dataclasses import dataclass


@dataclass
class IxbrlTags:
    NAMESPACE: str = "http://www.xbrl.org/2013/inlineXBRL"
    FRACTION: str = "fraction"
    NONFRACTION: str = "nonFraction"
    NONNUMERIC: str = "nonNumeric"
    FOOTNOTE: str = "footnote"

@dataclass
class XhtmlTags:
    NAMESPACE: str = "http://www.w3.org/1999/xhtml"
    HEAD: str = "head"
    STYLE: str = "style"