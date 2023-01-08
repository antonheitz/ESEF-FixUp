
from dataclasses import dataclass
from typing import Dict, List, Tuple
from packages.worker.src.file_dataclasses import PackageFile
from packages.worker.src.fixup.base_fixup import BaseFixup
from packages.worker.src.constants import XhtmlTags
import cssutils
import xml.dom.minidom as MD

import logging
cssutils.log.setLevel(logging.CRITICAL)


@dataclass
class StyleCombination:
    class_name: str
    optimzed_group: List[int]

@dataclass
class Combination:
    values: List[int]

    def remove_combination(self, combination: 'Combination') -> None:
        if self.contains(combination):
            self.values = [num for num in self.values if num not in combination.values]
        
    def contains(self, combination: 'Combination') -> bool: 
        return all([num in self.values for num in combination.values])

    def common_combination(self, combination: 'Combination') -> 'Combination':
        common_numbers: List[int] = [num for num in combination.values if num in self.values]
        if common_numbers:
            return Combination(common_numbers)
        return None
        

@dataclass
class CombinationPool:
    combinations: List[Combination]

    def remove_combination(self, combination: Combination) -> None:
        for combination in self.combinations:
            combination.remove_combination(combination)
    
    def add_combination(self, combination: Combination) -> None:
        for own_combination in self.combinations:
            own_combination.remove_combination(combination)
        self.combinations = [own_combination for own_combination in self.combinations if len(own_combination.values) > 0]
        self.combinations.append(combination)

    def find_common_combination(self, combination: Combination) -> Combination:
        for own_combination in self.combinations:
            common_combination: Combination = own_combination.common_combination(combination)
            if common_combination:
                return common_combination
        return combination

class CssOptimizer(BaseFixup):
    def __init__(self, name: str):
        super().__init__(name)

    def run_file(self, file: PackageFile, options: dict = None) -> None:
        # run this fixup for ixbrl files only
        if file.type == file.IXBRL:
            self.optimize_file_css(file)

    def optimize_file_css(self, file: PackageFile) -> None:
        # iterate the document and get all style attributes for the respective nodes:
        nodelist_css: List[Tuple[MD.Element, List[str]]] = []
        child: MD.Element
        for child in file.xml_document.childNodes:
            if child.nodeType == child.ELEMENT_NODE:
                nodelist_css += _find_styles(child)
        # apply the ids in a optimized way to the nodelist
        style_string: str = _apply_optimized_classes(nodelist_css)
        # add style into a style attribute
        head_element: MD.Element
        for head_element in file.xml_document.getElementsByTagNameNS(XhtmlTags.NAMESPACE, XhtmlTags.HEAD):
            style_node: MD.Element = file.xml_document.createElement(XhtmlTags.STYLE)
            style_node.appendChild(file.xml_document.createTextNode(style_string))
            head_element.appendChild(style_node)
        
def _find_styles(node: MD.Element) -> List[Tuple[MD.Element, List[str]]]:
    nodelist: List[Tuple[MD.Element, str]] = []
    style: str = node.getAttribute("style")
    if style:
        parsed_style: cssutils.css.CSSStyleDeclaration = cssutils.parseStyle(style)
        nodelist.append((node, [rule.cssText for rule in parsed_style]))
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

def _apply_optimized_classes(nodelist_css: List[Tuple[MD.Element, List[str]]]) -> str:
    # get ids for all styles, grouping the same property/value combination to get the same id
    style_ids: Dict[str, int] = {}
    next_id: int = 0
    for node, style_values in nodelist_css:
        for style_value in style_values:
            if style_value not in style_ids:
                style_ids[style_value] = next_id
                next_id += 1
    nodelist_ids: List[Tuple[MD.Element, List[int]]] = [(node, [style_ids[style] for style in styles]) for node, styles in nodelist_css] 
    # optimize style combinations
    optimized_style_combinations: List[List[int]] = _optimize_styles([ids for node, ids in nodelist_ids])
    # build classes
    style_combinations, style_sheet = _create_style_sheet(optimized_style_combinations, style_ids)
    # apply the classes to the nodes
    for node, ids in nodelist_ids:
        added_ids: List[int] = []
        classes: List[str] = []
        for id in ids:
            if id not in added_ids:
                classes.append(style_combinations[id].class_name)
                added_ids += style_combinations[id].optimzed_group
        node.removeAttribute("style")
        node.setAttribute("class", node.getAttribute("class") + " " + " ".join(classes))
    # return style sheet
    return style_sheet

def _create_style_sheet(id_combinations: List[List[int]], style_ids: Dict[str, int]) -> Tuple[Dict[int, StyleCombination], str]:
    # revert style ids for lookup
    id_to_style: Dict[int, str] = {style_ids[style]:style for style in style_ids}
    style_combinations: Dict[int, StyleCombination] = {}
    style_sheet: str = ""
    for index, id_combination in enumerate(id_combinations):
        class_name: str = f"esef-fixup-style-{index}"
        class_content: str = ""
        style_combination: StyleCombination = StyleCombination(class_name, id_combination)
        for id in id_combination:
            class_content += id_to_style[id] + "; "
            style_combinations[id] = style_combination
        style_sheet += f".{class_name} {{ {class_content}}} \n"
    return style_combinations, style_sheet

def _optimize_styles(num_combinations: List[List[int]]) -> List[List[int]]:
    all_nums: List[int] = list(set([num for num_combination in num_combinations for num in num_combination]))
    pool: CombinationPool = CombinationPool([Combination(all_nums)])

    for num_combination in num_combinations:
        combination: Combination = Combination(num_combination)
        while combination.values:
            common_combination: Combination = pool.find_common_combination(combination)
            pool.add_combination(common_combination)
            combination.remove_combination(common_combination)

    return [optimized_combination.values for optimized_combination in pool.combinations]