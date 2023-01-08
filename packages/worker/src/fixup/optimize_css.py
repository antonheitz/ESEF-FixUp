
from typing import List, Tuple
from packages.worker.src.file_dataclasses import PackageFile
from packages.worker.src.fixup.base_fixup import BaseFixup
from packages.worker.src.constants import XhtmlTags
import xml.dom.minidom as MD

class CssOptimizer(BaseFixup):
    def __init__(self, name: str):
        super().__init__(name)

    def run_file(self, file: PackageFile, options: dict = None) -> None:
        # run this fixup for ixbrl files only
        if file.type == file.IXBRL:
            self.optimize_file_css(file)

    def optimize_file_css(self, file: PackageFile) -> None:
        # iterate the document and get all style attributes for the respective nodes:
        nodelist: List[Tuple[MD.Element, str]] = []
        child: MD.Element
        for child in file.xml_document.childNodes:
            if child.nodeType == child.ELEMENT_NODE:
                nodelist += _find_styles(child)
        # process node and styles, extend later to optimize the style space usage
        style_string: str = ""
        for index, (node, style) in enumerate(nodelist):
            style_string += _node_to_class(index, node, style)
        # add style into a style attribute
        head_element: MD.Element
        for head_element in file.xml_document.getElementsByTagNameNS(XhtmlTags.NAMESPACE, XhtmlTags.HEAD):
            style_node: MD.Element = file.xml_document.createElement(XhtmlTags.STYLE)
            style_node.appendChild(file.xml_document.createTextNode(style_string))
            head_element.appendChild(style_node)
        
def _find_styles(node: MD.Element) -> List[Tuple[MD.Element, str]]:
    nodelist: List[Tuple[MD.Element, str]] = []
    style: str = node.getAttribute("style")
    if style:
        nodelist.append((node, style))
    if node.hasChildNodes():
        child: MD.Element
        for child in node.childNodes:
            if child.nodeType == child.ELEMENT_NODE:
                nodelist += _find_styles(child)
    return nodelist

def _node_to_class(index: int, node: MD.Element, style: str) -> str:
    class_name: str = f"esef-fixup-style-{index}"
    node.removeAttribute("style")
    node.setAttribute("class", node.getAttribute("class") + f" {class_name}")
    return f".{class_name} {{{style}}} \n"