"""
The basic building blocks making up the Widget system.
"""

# The classes defined here need more than 7 instance attributes,
# and there is no cyclic import during runtime.
# pylint: disable=too-many-instance-attributes, cyclic-import

from __future__ import annotations

from copy import deepcopy
from inspect import signature
from typing import Any, Callable, Generator, Iterator, Optional, Type, Union
from unicodedata import lookup as u_lookup

from ..ansi_interface import MouseAction, MouseEvent, reset
from ..enums import HorizontalAlignment, SizePolicy, WidgetChange
from ..fancy_repr import FancyYield
from ..helpers import break_line
from ..input import keys
from ..markup import get_markup
from ..regex import real_length
from ..term import Terminal, get_terminal
from . import styles as w_styles

__all__ = ["Widget", "Label"]

BoundCallback = Callable[..., Any]
WidgetType = Union["Widget", Type["Widget"]]


def _set_obj_or_cls_style(
    obj_or_cls: Type[Widget] | Widget, key: str, value: w_styles.StyleType
) -> Type[Widget] | Widget:
    """Sets a style for an object or class

    Args:
        obj_or_cls: The Widget instance or type to update.
        key: The style key.
        value: The new style.

    Returns:
        Type[Widget] | Widget: The updated class.

    Raises:
        See `pytermgui.widgets.styles.StyleManager`.
    """

    obj_or_cls.styles[key] = value

    return obj_or_cls


def _set_obj_or_cls_char(
    obj_or_cls: Type[Widget] | Widget, key: str, value: w_styles.CharType
) -> Type[Widget] | Widget:
    """Sets a char for an object or class

    Args:
        obj_or_cls: The Widget instance or type to update.
        key: The char key.
        value: The new char.

    Returns:
        Type[Widget] | Widget: The updated class.

    Raises:
        KeyError: The char key provided is invalid.
    """

    if not key in obj_or_cls.chars.keys():
        raise KeyError(f"Char {key} is not valid for {obj_or_cls}!")

    obj_or_cls.chars[key] = value

    return obj_or_cls


class Widget:  # pylint: disable=too-many-public-methods
    """The base of the Widget system"""

    set_style = classmethod(_set_obj_or_cls_style)
    set_char = classmethod(_set_obj_or_cls_char)

    styles = w_styles.StyleManager()
    """Default styles for this class"""

    chars: dict[str, w_styles.CharType] = {}
    """Default characters for this class"""

    keys: dict[str, set[str]] = {}
    """Groups of keys that are used in `handle_key`"""

    serialized: list[str] = [
        "id",
        "pos",
        "depth",
        "width",
        "height",
        "selected_index",
        "selectables_length",
    ]
    """Fields of widget that shall be serialized by `pytermgui.serializer.Serializer`"""

    # This class is loaded after this module,
    # and thus mypy doesn't see its existence.
    _id_manager: Optional["_IDManager"] = None  # type: ignore

    size_policy = SizePolicy.get_default()
    """`pytermgui.enums.SizePolicy` to set widget's width according to"""

    parent_align = HorizontalAlignment.get_default()
    """`pytermgui.enums.HorizontalAlignment` to align widget by"""

    from_data: Callable[..., Widget | list[Widget] | None]

    # We cannot import boxes here due to cyclic imports.
    box: Any

    def __init__(self, **attrs: Any) -> None:
        """Initialize object"""

        self.set_style = lambda key, value: _set_obj_or_cls_style(self, key, value)
        self.set_char = lambda key, value: _set_obj_or_cls_char(self, key, value)

        self.width = 1
        self.height = 1
        self.pos = self.terminal.origin

        self.depth = 0

        self.styles = type(self).styles.branch(self)
        self.chars = type(self).chars.copy()

        self.parent: Widget | None = None
        self.selected_index: int | None = None

        self._selectables_length = 0
        self._id: Optional[str] = None
        self._serialized_fields = type(self).serialized
        self._bindings: dict[str | Type[MouseEvent], tuple[BoundCallback, str]] = {}
        self._relative_width: float | None = None
        self._previous_state: tuple[tuple[int, int], list[str]] | None = None

        self.positioned_line_buffer: list[tuple[tuple[int, int], str]] = []

        for attr, value in attrs.items():
            setattr(self, attr, value)

    def __repr__(self) -> str:
        """Return repr string of this widget.

        Returns:
            Whatever this widget's `debug` method gives.
        """

        return self.debug()

    def __fancy_repr__(self) -> Generator[FancyYield, None, None]:
        """Yields the repr of this object, then a preview of it."""

        yield self.debug()
        yield "\n\n"
        yield {
            "text": "\n".join((line + reset() for line in self.get_lines())),
            "highlight": False,
        }

    def __iter__(self) -> Iterator[Widget]:
        """Return self for iteration"""

        yield self

    @property
    def bindings(self) -> dict[str | Type[MouseEvent], tuple[BoundCallback, str]]:
        """Gets a copy of the bindings internal dictionary.

        Returns:
            A copy of the internal bindings dictionary, such as:

            ```
            {
                "*": (star_callback, "This is a callback activated when '*' is pressed.")
            }
            ```
        """

        return self._bindings.copy()

    @property
    def id(self) -> Optional[str]:  # pylint: disable=invalid-name
        """Gets this widget's id property

        Returns:
            The id string if one is present, None otherwise.
        """

        return self._id

    @id.setter
    def id(self, value: str) -> None:  # pylint: disable=invalid-name
        """Registers a widget to the Widget._id_manager.

        If this widget already had an id, the old value is deregistered
        before the new one is assigned.

        Args:
            value: The new id this widget will be registered as.
        """

        if self._id == value:
            return

        manager = Widget._id_manager
        assert manager is not None

        old = manager.get_id(self)
        if old is not None:
            manager.deregister(old)

        self._id = value
        manager.register(self)

    @property
    def selectables_length(self) -> int:
        """Gets how many selectables this widget contains.

        Returns:
            An integer describing the amount of selectables in this widget.
        """

        return self._selectables_length

    @property
    def selectables(self) -> list[tuple[Widget, int]]:
        """Gets a list of all selectables within this widget

        Returns:
            A list of tuples. In the default implementation this will be
            a list of one tuple, containing a reference to `self`, as well
            as the lowest index, 0.
        """

        return [(self, 0)]

    @property
    def is_selectable(self) -> bool:
        """Determines whether this widget has any selectables.

        Returns:
            A boolean, representing `self.selectables_length != 0`.
        """

        return self.selectables_length != 0

    @property
    def static_width(self) -> int:
        """Allows for a shorter way of setting a width, and SizePolicy.STATIC.

        Args:
            value: The new width integer.

        Returns:
            None, as this is setter only.
        """

        return None  # type: ignore

    @static_width.setter
    def static_width(self, value: int) -> None:
        """See the static_width getter."""

        self.width = value
        self.size_policy = SizePolicy.STATIC

    @property
    def relative_width(self) -> float | None:
        """Sets this widget's relative width, and changes size_policy to RELATIVE.

        The value is clamped to 1.0.

        If a Container holds a width of 30, and it has a subwidget with a relative
        width of 0.5, it will be resized to 15.

        Args:
            value: The multiplier to apply to the parent's width.

        Returns:
            The current relative_width.
        """

        return self._relative_width

    @relative_width.setter
    def relative_width(self, value: float) -> None:
        """See the relative_width getter."""

        self.size_policy = SizePolicy.RELATIVE
        self._relative_width = min(1.0, value)

    @property
    def terminal(self) -> Terminal:
        """Returns the current global terminal instance."""

        return get_terminal()

    def _align(self, lines: list[str]) -> list[str]:
        """Aligns the given lines based on this widget's `parent_align` attribute."""

        width = self.width

        def _align_left(line: str) -> str:
            return line + (width - real_length(line)) * " "

        def _align_center(line: str) -> str:
            right, extra = divmod(width - real_length(line), 2)
            left = right + extra

            return left * " " + line + right * " "

        def _align_right(line: str) -> str:
            return (width - real_length(line)) * " " + line

        if self.parent_align is None:
            raise TypeError("Horizontal alignment cannot be None.")

        assert isinstance(self.parent_align, HorizontalAlignment)

        aligner = {
            HorizontalAlignment.LEFT: _align_left,
            HorizontalAlignment.CENTER: _align_center,
            HorizontalAlignment.RIGHT: _align_right,
        }[self.parent_align]

        aligned = []

        for line in lines:
            aligned.append(aligner(line))

        return aligned

    def get_change(self) -> WidgetChange | None:
        """Determines whether widget lines changed since the last call to this function."""

        lines = self.get_lines()

        if self._previous_state is None:
            self._previous_state = (self.width, self.height), lines
            return WidgetChange.LINES

        lines = self.get_lines()
        (old_width, old_height), old_lines = self._previous_state

        self._previous_state = (self.width, self.height), lines

        if old_width != self.width and old_height != self.height:
            return WidgetChange.SIZE

        if old_width != self.width:
            return WidgetChange.WIDTH

        if old_height != self.height:
            return WidgetChange.HEIGHT

        if old_lines != lines:
            return WidgetChange.LINES

        return None

    def contains(self, pos: tuple[int, int]) -> bool:
        """Determines whether widget contains `pos`.

        Args:
            pos: Position to compare.

        Returns:
            Boolean describing whether the position is inside
                this widget.
        """

        rect = self.pos, (
            self.pos[0] + self.width,
            self.pos[1] + self.height,
        )

        (left, top), (right, bottom) = rect

        return left <= pos[0] < right and top <= pos[1] < bottom

    def handle_mouse(self, event: MouseEvent) -> bool:
        """Tries to call the most specific mouse handler function available.

        This function looks for a set of mouse action handlers. Each handler follows
        the format

            on_{event_name}

        For example, the handler triggered on MouseAction.LEFT_CLICK would be
        `on_left_click`. If no handler is found nothing is done.

        You can also define more general handlers, for example to group left & right
        clicks you can use `on_click`, and to catch both up and down scroll you can use
        `on_scroll`. General handlers are only used if they are the most specific ones,
        i.e. there is no "specific" handler.

        Args:
            event: The event to handle.

        Returns:
            Whether the parent of this widget should treat it as one to "stick" events
            to, e.g. to keep sending mouse events to it. One can "unstick" a widget by
            returning False in the handler.
        """

        def _get_names(action: MouseAction) -> tuple[str, ...]:
            if action.value in ["hover", "release"]:
                return (action.value,)

            parts = action.value.split("_")

            # left click & right click
            if parts[0] in ["left", "right"]:
                return (action.value, parts[1])

            if parts[0] == "shift":
                return (action.value, f"shift_{parts[1]}", parts[1])

            # scroll up & down
            return (action.value, parts[0])

        possible_names = _get_names(event.action)
        for name in possible_names:
            if hasattr(self, f"on_{name}"):
                handle = getattr(self, f"on_{name}")

                return handle(event)

        return False

    def handle_key(self, key: str) -> bool:
        """Handles a mouse event, returning its success.

        Args:
            key: String representation of input string.
                The `pytermgui.input.keys` object can be
                used to retrieve special keys.

        Returns:
            A boolean describing whether the key was handled.
        """

        return False and hasattr(self, key)

    def serialize(self) -> dict[str, Any]:
        """Serializes a widget.

        The fields looked at are defined `Widget.serialized`. Note that
        this method is not very commonly used at the moment, so it might
        not have full functionality in non-nuclear widgets.

        Returns:
            Dictionary of widget attributes. The dictionary will always
            have a `type` field. Any styles are converted into markup
            strings during serialization, so they can be loaded again in
            their original form.

            Example return:
            ```
                {
                    "type": "Label",
                    "value": "[210 bold]I am a title",
                    "parent_align": 0,
                    ...
                }
            ```
        """

        fields = self._serialized_fields

        out: dict[str, Any] = {"type": type(self).__name__}
        for key in fields:
            # Detect styled values
            if key.startswith("*"):
                style = True
                key = key[1:]
            else:
                style = False

            value = getattr(self, key)

            # Convert styled value into markup
            if style:
                style_call = self._get_style(key)
                if isinstance(value, list):
                    out[key] = [get_markup(style_call(char)) for char in value]
                else:
                    out[key] = get_markup(style_call(value))

                continue

            out[key] = value

        # The chars need to be handled separately
        out["chars"] = {}
        for key, value in self.chars.items():
            style_call = self._get_style(key)

            if isinstance(value, list):
                out["chars"][key] = [get_markup(style_call(char)) for char in value]
            else:
                out["chars"][key] = get_markup(style_call(value))

        return out

    def copy(self) -> Widget:
        """Creates a deep copy of this widget"""

        return deepcopy(self)

    def _get_style(self, key: str) -> w_styles.DepthlessStyleType:
        """Gets style call from its key.

        This is analogous to using `self.styles.{key}`

        Args:
            key: A key into the widget's style manager.

        Returns:
            A `pytermgui.styles.StyleCall` object containing the referenced
            style. StyleCall objects should only be used internally inside a
            widget.

        Raises:
            KeyError: Style key is invalid.
        """

        return self.styles[key]

    def _get_char(self, key: str) -> w_styles.CharType:
        """Gets character from its key.

        Args:
            key: A key into the widget's chars dictionary.

        Returns:
            Either a `list[str]` or a simple `str`, depending on the character.

        Raises:
            KeyError: Style key is invalid.
        """

        chars = self.chars[key]

        if isinstance(chars, str):
            if chars.startswith("u:"):
                identifier = " ".join(chars[2:].split("_"))
                chars = u_lookup(identifier)

            return chars

        return chars.copy()

    def get_lines(self) -> list[str]:
        """Gets lines representing this widget.

        These lines have to be equal to the widget in length. All
        widgets must provide this method. Make sure to keep it performant,
        as it will be called very often, often multiple times per WindowManager frame.

        Any longer actions should be done outside of this method, and only their
        result should be looked up here.

        Returns:
            Nothing by default.

        Raises:
            NotImplementedError: As this method is required for **all** widgets, not
                having it defined will raise NotImplementedError.
        """

        raise NotImplementedError(f"get_lines() is not defined for type {type(self)}.")

    def move(self, diff_x: int, diff_y: int) -> None:
        """Moves the widget by the given x and y changes."""

        self.pos = (self.pos[0] + diff_x, self.pos[1] + diff_y)

        adjusted = []
        for pos, line in self.positioned_line_buffer:
            adjusted.append(((pos[0] + diff_x, pos[1] + diff_y), line))

        self.positioned_line_buffer = adjusted

    def bind(
        self, key: str, action: BoundCallback, description: Optional[str] = None
    ) -> None:
        """Binds an action to a keypress.

        This function is only called by implementations above this layer. To use this
        functionality use `pytermgui.window_manager.WindowManager`, or write your own
        custom layer.

        Special keys:
        - keys.ANY_KEY: Any and all keypresses execute this binding.
        - keys.MouseAction: Any and all mouse inputs execute this binding.

        Args:
            key: The key that the action will be bound to.
            action: The action executed when the key is pressed.
            description: An optional description for this binding. It is not really
                used anywhere, but you can provide a helper menu and display them.
        """

        if description is None:
            description = f"Binding of {key} to {action}"

        self._bindings[key] = (action, description)

    def unbind(self, key: str) -> None:
        """Unbinds the given key."""

        del self._bindings[key]

    def execute_binding(self, key: Any, ignore_any: bool = False) -> bool:
        """Executes a binding belonging to key, when present.

        Use this method inside custom widget `handle_keys` methods, or to run a callback
        without its corresponding key having been pressed.

        Args:
            key: Usually a string, indexing into the `_bindings` dictionary. These are the
                same strings as defined in `Widget.bind`.
            ignore_any: If set, `keys.ANY_KEY` bindings will not be executed.

        Returns:
            True if the binding was found, False otherwise. Bindings will always be
                executed if they are found.
        """

        # Execute special binding
        if not ignore_any and keys.ANY_KEY in self._bindings:
            method, _ = self._bindings[keys.ANY_KEY]
            method(self, key)

        if key in self._bindings:
            method, _ = self._bindings[key]
            method(self, key)

            return True

        return False

    def select(self, index: int | None = None) -> None:
        """Selects a part of this Widget.

        Args:
            index: The index to select.

        Raises:
            TypeError: This widget has no selectables, i.e. widget.is_selectable == False.
        """

        if not self.is_selectable:
            raise TypeError(f"Object of type {type(self)} has no selectables.")

        if index is not None:
            index = min(max(0, index), self.selectables_length - 1)
        self.selected_index = index

    def print(self) -> None:
        """Prints this widget"""

        for line in self.get_lines():
            print(line)

    def debug(self) -> str:
        """Returns identifiable information about this widget.

        This method is used to easily differentiate between widgets. By default, all widget's
        __repr__ method is an alias to this. The signature of each widget is used to generate
        the return value.

        Returns:
            A string almost exactly matching the line of code that could have defined the widget.

            Example return:

            ```
            Container(Label(value="This is a label", padding=0),
            Button(label="This is a button", padding=0), **attrs)
            ```

        """

        constructor = "("
        for name in signature(getattr(self, "__init__")).parameters:
            current = ""
            if name == "attrs":
                current += "**attrs"
                continue

            if len(constructor) > 1:
                current += ", "

            current += name

            attr = getattr(self, name, None)
            if attr is None:
                continue

            current += "="

            if isinstance(attr, str):
                current += f'"{attr}"'
            else:
                current += str(attr)

            constructor += current

        constructor += ")"

        return type(self).__name__ + constructor


class Label(Widget):
    """A Widget to display a string

    By default, this widget uses `pytermgui.widgets.styles.MARKUP`. This
    allows it to house markup text that is parsed before display, such as:

    ```termage-svg
    print("hello world")
    ```

    ```python3
    import pytermgui as ptg

    with ptg.alt_buffer():
        root = ptg.Container(
            ptg.Label("[italic 141 bold]This is some [green]fancy [white inverse]text!")
        )
        root.print()
        ptg.getch()
    ```

    <p style="text-align: center">
     <img
      src="https://github.com/bczsalba/pytermgui/blob/master/assets/docs/widgets/label.png?raw=true"
      width=100%>
    </p>
    """

    serialized = Widget.serialized + ["*value", "align", "padding"]
    styles = w_styles.StyleManager(value="")

    def __init__(
        self,
        value: str = "",
        style: str | w_styles.StyleValue = "",
        padding: int = 0,
        non_first_padding: int = 0,
        **attrs: Any,
    ) -> None:
        """Initializes a Label.

        Args:
            value: The value of this string. Using the default value style
                (`pytermgui.widgets.styles.MARKUP`),
            style: A pre-set value for self.styles.value.
            padding: The number of space (" ") characters to prepend to every line after
                line breaking.
            non_first_padding: The number of space characters to prepend to every
                non-first line of `get_lines`. This is applied on top of `padding`.
        """

        super().__init__(**attrs)

        self.value = value
        self.padding = padding
        self.non_first_padding = non_first_padding
        self.width = real_length(value) + self.padding

        if style != "":
            self.styles.value = style

    def get_lines(self) -> list[str]:
        """Get lines representing this Label, breaking lines as necessary"""

        lines = []
        limit = self.width - self.padding
        broken = break_line(
            self.styles.value(self.value),
            limit=limit,
            non_first_limit=limit - self.non_first_padding,
        )

        for i, line in enumerate(broken):
            if i == 0:
                lines.append(self.padding * " " + line)
                continue

            lines.append(self.padding * " " + self.non_first_padding * " " + line)

        return lines or [""]


class ScrollableWidget(Widget):
    """A widget with some scrolling helper methods.

    This is not an implementation of the scrolling behaviour itself, just the
    user-facing API for it.

    It provides a `_scroll_offset` attribute, which is an integer describing the current
    scroll state offset from the top, as well as some methods to modify the state."""

    def __init__(self, **attrs: Any) -> None:
        """Initializes the scrollable widget."""

        super().__init__(**attrs)

        self._max_scroll = 0
        self._scroll_offset = 0

    def scroll(self, offset: int) -> bool:
        """Scrolls to given offset, returns the new scroll_offset.

        Args:
            offset: The amount to scroll by. Positive offsets scroll down,
                negative up.

        Returns:
            True if the scroll offset changed, False otherwise.
        """

        base = self._scroll_offset

        self._scroll_offset = min(
            max(0, self._scroll_offset + offset), self._max_scroll
        )

        return base != self._scroll_offset

    def scroll_end(self, end: int) -> int:
        """Scrolls to either top or bottom end of this object.

        Args:
            end: The offset to scroll to. 0 goes to the very top, -1 to the
                very bottom.

        Returns:
            True if the scroll offset changed, False otherwise.
        """

        base = self._scroll_offset

        if end == 0:
            self._scroll_offset = 0

        elif end == -1:
            self._scroll_offset = self._max_scroll

        return base != self._scroll_offset

    def get_lines(self) -> list[str]:
        ...
