from typing import List, Tuple
import zipfile
import os
from packages.worker.src.file_dataclasses import PackageFile
import xml.dom.minidom as MD
from packages.worker.src.constants import IxbrlTags
from packages.worker.src.fixup.base_fixup import FixupOptions

EXTRACT_FOLDER: str = "TMP_EXTRACT"


def load_files(file_path: str, working_dir: str, options: FixupOptions) -> Tuple[List[PackageFile], str]:
    result_folder: str = _extract_zip(file_path, working_dir)
    file_paths: List[str] = _discover_files(result_folder)
    return _classify_files(file_paths, result_folder, undercover=options.undercover), result_folder


def save_files(files: List[PackageFile]) -> None:
    for file in files:
        if file.xml_document:
            with open(file.path, "w") as f:
                f.write(file.xml_document.toxml())


def _extract_zip(file_path: str, working_dir: str) -> str:
    # extract zip file
    result_folder: str = os.path.join(working_dir, EXTRACT_FOLDER)
    with zipfile.ZipFile(file_path, 'r') as f:
        f.extractall(result_folder)
    return result_folder


def _discover_files(folder: str) -> List[str]:
    # load list of created files in folder
    files: List[str] = []
    for item in os.listdir(folder):
        new_path: str = os.path.join(folder, item)
        if os.path.isdir(new_path):
            files += _discover_files(new_path)
        else:
            files.append(new_path)
    return files


def _classify_files(file_paths: List[str], base_folder: str, undercover: bool = False) -> List[PackageFile]:
    # classify and load files
    files: List[PackageFile] = []
    for file_path in file_paths:
        file_name: str = file_path[len(base_folder) + 1:]
        file: PackageFile = PackageFile(
            name=file_name,
            path=file_path,
            type=PackageFile.OTHER,
            zip_root=file_name.split(os.path.sep)[0],
            xml_document=None
        )
        # check base file type by extension
        file_extension: str = file_path.split(".")[-1].lower()
        if file_extension in ["xhtml", "html"]:
            file.type = PackageFile.XHTML
        elif file_extension in ["xml"]:
            file.type = PackageFile.XML
        elif file_extension in ["xsd"]:
            file.type = PackageFile.XSD
        # load files
        if file.type in [PackageFile.XHTML, PackageFile.XML, PackageFile.XSD]:
            file.xml_document: MD.Document = MD.parse(file.path)
            if file.type == PackageFile.XHTML:
                element_count: int = 0
                element_count += len(file.xml_document.getElementsByTagNameNS(
                    IxbrlTags.NAMESPACE, IxbrlTags.FRACTION))
                element_count += len(file.xml_document.getElementsByTagNameNS(
                    IxbrlTags.NAMESPACE, IxbrlTags.NONFRACTION))
                element_count += len(file.xml_document.getElementsByTagNameNS(
                    IxbrlTags.NAMESPACE, IxbrlTags.NONNUMERIC))
                element_count += len(file.xml_document.getElementsByTagNameNS(
                    IxbrlTags.NAMESPACE, IxbrlTags.FOOTNOTE))
                if element_count:
                    file.type = PackageFile.IXBRL
            # add edit comment for xml files if not undercover
            if not undercover:
                child: MD.Element
                # add comment to the file
                for child in file.xml_document.childNodes:
                    if child.nodeType == child.ELEMENT_NODE:
                        comment_node: MD.Comment = file.xml_document.createComment(
                            "POSTPROCCESSED WITH https://github.com/antonheitz/esef-post-processor (Version 0.0)")
                        if child.hasChildNodes():
                            child.insertBefore(comment_node, child.childNodes[0])
                        else:
                            child.appendChild(comment_node)
        files.append(file)
    return files
