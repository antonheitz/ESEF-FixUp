from dataclasses import dataclass


@dataclass
class IxbrlTags:
    NAMESPACE: str = "http://www.xbrl.org/2013/inlineXBRL"
    FRACTION: str = "fraction"
    NONFRACTION: str = "nonFraction"
    NONNUMERIC: str = "nonNumeric"
    FOOTNOTE: str = "footnote"