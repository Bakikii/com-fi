from __future__ import annotations

import typing
from typing import Protocol, ClassVar, Tuple, Dict
from dataclasses import dataclass, field

T = typing.TypeVar('T', bound='CustomNode')


class CustomNode(Protocol):
    @classmethod
    def INPUT_TYPES(cls) -> dict: ...

    RETURN_TYPES: ClassVar[typing.Sequence[str]]
    RETURN_NAMES: typing.Optional[ClassVar[Tuple[str]]]
    OUTPUT_IS_LIST: typing.Optional[ClassVar[typing.Sequence[bool]]]
    INPUT_IS_LIST: typing.Optional[ClassVar[bool]]
    FUNCTION: ClassVar[str]
    CATEGORY: ClassVar[str]
    OUTPUT_NODE: typing.Optional[ClassVar[bool]]

    def __call__(self) -> T:
        ...


@dataclass
class ExportedNodes:
    NODE_CLASS_MAPPINGS: Dict[str, CustomNode] = field(default_factory=dict)
    NODE_DISPLAY_NAME_MAPPINGS: Dict[str, str] = field(default_factory=dict)
    EXTENSION_WEB_DIRS: Dict[str, str] = field(default_factory=dict)

    def update(self, exported_nodes: ExportedNodes) -> ExportedNodes:
        self.NODE_CLASS_MAPPINGS.update(exported_nodes.NODE_CLASS_MAPPINGS)
        self.NODE_DISPLAY_NAME_MAPPINGS.update(exported_nodes.NODE_DISPLAY_NAME_MAPPINGS)
        self.EXTENSION_WEB_DIRS.update(exported_nodes.EXTENSION_WEB_DIRS)
        return self

    def __len__(self):
        return len(self.NODE_CLASS_MAPPINGS)

    def __sub__(self, other: ExportedNodes):
        exported_nodes = ExportedNodes().update(self)
        for self_key in exported_nodes.NODE_CLASS_MAPPINGS:
            if self_key in other.NODE_CLASS_MAPPINGS:
                exported_nodes.NODE_CLASS_MAPPINGS.pop(self_key)
            if self_key in other.NODE_DISPLAY_NAME_MAPPINGS:
                exported_nodes.NODE_DISPLAY_NAME_MAPPINGS.pop(self_key)
        for self_key in exported_nodes.EXTENSION_WEB_DIRS:
            if self_key in other.EXTENSION_WEB_DIRS:
                exported_nodes.EXTENSION_WEB_DIRS.pop(self_key)
        return exported_nodes

    def __add__(self, other):
        exported_nodes = ExportedNodes().update(self)
        return exported_nodes.update(other)
