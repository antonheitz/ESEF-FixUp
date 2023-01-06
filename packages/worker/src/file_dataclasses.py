from dataclasses import dataclass
import xml.dom.minidom as MD

@dataclass
class FileTypes:
    IXBRL: str = "IXBRL"
    XHTML: str = "XHTML"
    XML: str = "XML"
    XSD: str = "XSD"
    OTHER: str = "OTHER"

@dataclass
class PackageFile:
    name: str
    path: str
    type: str
    xml_document: MD.Document = None