"""
Convenience objects for Container corner & border styles.

They can be used as:
```python3
from pytermgui import Container, boxes

boxes.DOUBLE_TOP.set_chars_of(Container)
c = Container() # this will now use the style chosen
```

Boxes are also settable as a property of `pytermgui.widgets.Container`, and can
be referenced & defined in markup file definitions. For more info, check out
`pytermgui.file_loaders`.
"""

# This module is to be replaced with Frame, so the duplication won't be for long.
# pylint: disable=duplicate-code

from __future__ import annotations

from typing import Tuple

from ..regex import real_length
from .base import WidgetType


class Box:
    """Class for defining border & corner styles

    `lines` should be `list[str]` of length 3, such as:

    ```python3
    lines = [
        ".---.",
        "| x |",
        "`---`",
    ]
    ```

    The length of individual lines is arbitrary, only limitation is
    that the top & bottom border characters should occur most often in
    their respective lines.

    You can set corners to be of any length, their end is calculated by
    finding the index of the most often occuring character, which is assumed
    to be the border character.

    Top & bottom borders are currently limited in length to 1, but sides
    operate similarly to corners. They are separated by finding the index
    of the fill char from the start or end. The content char is "x" by
    default, however it can be set to anything else by giving the "content_char"
    construction parameter.

    As such, this:

    ```python3
    boxes.Box(
       [
           "corner1 ________________ corner2",
           "xleft   ################ rightxx",
           "corner3 ---------------- corner4",
       ],
       content_char="#",
    )
    ```

    Will result in:

    ```python3
    Box(
        borders=['xleft   ', '_', ' rightxx', '-'],
        corners=['corner1 ', ' corner2', ' corner4', 'corner3 ']
    )
    ```
    """

    CharType = Tuple[str, str, str, str]

    def __init__(self, lines: list[str], content_char: str = "x"):
        """Set instance attributes"""

        super().__init__()
        self.content_char = content_char

        top, _, bottom = lines
        top_left, top_right = self._get_corners(top)
        bottom_left, bottom_right = self._get_corners(bottom)

        self.borders = list(self._get_borders(lines))
        self.corners = [
            top_left,
            top_right,
            bottom_right,
            bottom_left,
        ]

    def __repr__(self) -> str:
        """Return string of self"""

        return self.debug()

    @staticmethod
    def _find_mode_char(line: str) -> str:
        """Find most often consecutively occuring character in string"""

        instances = 0
        current_char = ""

        results: list[tuple[str, int]] = []
        for char in line:
            if current_char == char:
                instances += 1
            else:
                if len(current_char) > 0:
                    results.append((current_char, instances))

                instances = 1
                current_char = char

        results.append((current_char, instances))

        results.sort(key=lambda item: item[1])
        if len(results) == 0:
            print(line, instances, current_char)

        return results[-1][0]

    def _get_corners(self, line: str) -> tuple[str, str]:
        """Get corners from a line"""

        mode_char = self._find_mode_char(line)
        left = line[: line.index(mode_char)]
        right = line[real_length(line) - (line[::-1].index(mode_char)) :]

        return left, right

    def _get_borders(self, lines: list[str]) -> tuple[str, str, str, str]:
        """Get borders from all lines"""

        top, middle, bottom = lines
        middle_reversed = middle[::-1]

        top_border = self._find_mode_char(top)
        left_border = middle[: middle.index(self.content_char)]

        right_border = middle[
            real_length(middle) - middle_reversed.index(self.content_char) :
        ]
        bottom_border = self._find_mode_char(bottom)

        # return top_border, left_border, right_border, bottom_border
        return left_border, top_border, right_border, bottom_border

    def set_chars_of(self, cls_or_obj: WidgetType) -> WidgetType:
        """Set border & corner chars of cls_or_obj to self values"""

        # We cannot import any widgets into here due to cyclic imports,
        # so we have to "hack" around it.
        if not hasattr(cls_or_obj, "set_char"):
            raise NotImplementedError(
                f"Object of type {cls_or_obj} does not support `set_char`"
            )

        cls_or_obj.set_char("border", self.borders)
        cls_or_obj.set_char("corner", self.corners)

        return cls_or_obj

    def debug(self) -> str:
        """Return identifiable information about object"""

        return f"Box(borders={self.borders}, corners={self.corners})"


BASIC = Box(
    [
        "-----",
        "| x |",
        "-----",
    ]
)

HEAVY = Box(
    [
        "┏━━━┓",
        "┃ x ┃",
        "┗━━━┛",
    ]
)
EMPTY = Box(
    [
        "",
        "x",
        "",
    ]
)
EMPTY_VERTICAL = Box(
    [
        "─────",
        "  x  ",
        "─────",
    ]
)
EMPTY_HORIZONTAL = Box(
    [
        "│   │",
        "│ x │",
        "│   │",
    ]
)
ROUNDED = Box(
    [
        "╭───╮",
        "│ x │",
        "╰───╯",
    ]
)

SINGLE = Box(
    [
        "┌───┐",
        "│ x │",
        "└───┘",
    ]
)

SINGLE_VERTICAL = Box(
    [
        "╔───╗",
        "║ x ║",
        "╚───╝",
    ]
)
SINGLE_HORIZONTAL = Box(
    [
        "╔═══╗",
        "│ x │",
        "╚═══╝",
    ]
)
DOUBLE_HORIZONTAL = Box(
    [
        "╭═══╮",
        "│ x │",
        "╰═══╯",
    ]
)
DOUBLE_VERTICAL = Box(
    [
        "╭───╮",
        "║ x ║",
        "╰───╯",
    ]
)
DOUBLE_SIDES = Box(
    [
        "╭═══╮",
        "║ x ║",
        "╰═══╯",
    ]
)
DOUBLE = Box(
    [
        "╔═══╗",
        "║ x ║",
        "╚═══╝",
    ]
)
DOUBLE_TOP = Box(
    [
        "╭═══╮",
        "│ x │",
        "╰───╯",
    ]
)
DOUBLE_BOTTOM = Box(
    [
        "╭───╮",
        "│ x │",
        "╰═══╯",
    ]
)
