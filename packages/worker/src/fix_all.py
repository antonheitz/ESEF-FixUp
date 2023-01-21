from typing import List
from packages.worker.src.file_dataclasses import PackageFile
from packages.worker.src.fixup.optimize_css import CssOptimizer
from packages.worker.src.fixup.base_fixup import BaseFixup, FixupOptions

registered_fixes: List[BaseFixup] = [
    CssOptimizer("CSS Optimizer")
]


def fix_files(files: List[PackageFile], options: FixupOptions) -> None:
    for fix in registered_fixes:
        fix.run(files, options)
