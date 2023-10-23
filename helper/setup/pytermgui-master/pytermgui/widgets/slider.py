"""This module contains the `Slider` class."""

from __future__ import annotations

from typing import Any, Callable

from ..ansi_interface import MouseAction, MouseEvent
from ..input import keys
from ..regex import real_length
from . import styles as w_styles
from .base import Widget

FILLED_SELECTED_STYLE = w_styles.MarkupFormatter("[72]{item}")
FILLED_UNSELECTED_STYLE = w_styles.MarkupFormatter("[247]{item}")
UNFILLED_STYLE = w_styles.MarkupFormatter("[240]{item}")


class Slider(Widget):  # pylint: disable=too-many-instance-attributes
    """A Widget to display & configure scalable data.

    By default, this Widget will act like a slider you might find in a
    settings page, allowing percentage-based selection of magnitude.
    Using `WindowManager` it can even be dragged around by the user using
    the mouse.
    """

    locked: bool
    """Disallow mouse input, hide cursor and lock current state"""

    chars = {"cursor": "", "rail": "━", "delimiter": ["[", "]"]}

    styles = w_styles.StyleManager(
        delimiter="surface",
        filled="surface+1",
        cursor="primary",
        filled_selected="primary",
        unfilled="surface-1",
        unfilled_selected="surface",
    )

    keys = {
        "increase": {keys.RIGHT, keys.CTRL_F, "l", "+"},
        "decrease": {keys.LEFT, keys.CTRL_B, "h", "-"},
    }

    def __init__(
        self,
        onchange: Callable[[float], Any] | None = None,
        locked: bool = False,
        **attrs: Any,
    ) -> None:
        """Initializes a Slider.

        Args:
            onchange: The callable called every time the value
                is updated.
            locked: Whether this Slider should accept value changes.
        """

        self._value = 0.0

        super().__init__(**attrs)
        self._selectables_length = 1

        self.is_locked = locked
        self.onchange = onchange

    @property
    def value(self) -> float:
        """Returns the value of this Slider.

        Returns:
            A floating point number between 0.0 and 1.0.
        """

        return self._value

    @value.setter
    def value(self, new: float) -> None:
        """Updates the value."""

        if self.is_locked:
            return

        self._value = max(0.0, min(new, 1.0))

        if self.onchange is not None:
            self.onchange(self._value)

    def handle_key(self, key: str) -> bool:
        """Moves the slider cursor."""

        if self.execute_binding(key):
            return True

        if key in self.keys["increase"]:
            self.value += 0.1
            return True

        if key in self.keys["decrease"]:
            self.value -= 0.1
            return True

        return False

    def handle_mouse(self, event: MouseEvent) -> bool:
        """Moves the slider cursor."""

        delimiter = self._get_char("delimiter")[0]

        if event.action in [MouseAction.LEFT_CLICK, MouseAction.LEFT_DRAG]:
            offset = event.position[0] - self.pos[0] + 1 - real_length(delimiter)
            self.value = max(0, min(offset / self.width, 1.0))
            return True

        return False

    def get_lines(self) -> list[str]:
        """Gets slider lines."""

        rail = self._get_char("rail")
        cursor = self._get_char("cursor") or rail
        delimiters = self._get_char("delimiter")

        assert isinstance(delimiters, list)
        assert isinstance(cursor, str)
        assert isinstance(rail, str)

        cursor = self._get_style("cursor")(cursor)
        unfilled = self.styles.unfilled(rail)

        if self.selected_index is None:
            filled = self.styles.filled(rail)
        else:
            filled = self.styles.filled_selected(rail)

            for i, char in enumerate(delimiters):
                delimiters[i] = self.styles.filled_selected(char)

        for i, delimiter in enumerate(delimiters):
            delimiters[i] = self.styles.delimiter(delimiter)

        width = self.width - real_length("".join(delimiters))
        count = width * self.value - 1

        chars = [delimiters[0]]

        for i in range(width):
            if i == count and not self.is_locked and self.selected_index is not None:
                chars.append(cursor)
                continue

            if i <= count:
                chars.append(filled)
                continue

            chars.append(unfilled)

        chars.append(delimiters[1])
        line = "".join(chars)
        self.width = real_length(line)

        return [line]
