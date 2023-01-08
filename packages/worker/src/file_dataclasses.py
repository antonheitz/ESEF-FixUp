from dataclasses import dataclass
import xml.dom.minidom as MD

@dataclass
class PackageFile:
    name: str
    path: str
    type: str
    zip_root: str
    xml_document: MD.Document = None

    IXBRL: str = "IXBRL"
    XHTML: str = "XHTML"
    XML: str = "XML"
    XSD: str = "XSD"
    OTHER: str = "OTHER"