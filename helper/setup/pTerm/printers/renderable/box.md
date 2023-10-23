---
description: The box printer can be used to put content inside a box to highlight it
---

# Box

{% embed url="https://raw.githubusercontent.com/pterm/pterm/master/_examples/box/demo/animation.svg" %}
[https://github.com/pterm/pterm/tree/master/\_examples/box](https://github.com/pterm/pterm/tree/master/\_examples/box)
{% endembed %}

## Basic Usage

```go
pterm.DefaultBox.Println("Hello, World!")
```

## Options

| Name                      | Type        | Description                                                |
| ------------------------- | ----------- | ---------------------------------------------------------- |
| `Title`                   | `string`    | Title of the box                                           |
| `TitleTopLeft`            | `bool`      | Sets if the title should be displayed on the top left      |
| `TitleTopRight`           | `bool`      | Sets if the title should be displayed on the top right     |
| `TitleTopCenter`          | `bool`      | Sets if the title should be displayed on the top center    |
| `TitleBottomLeft`         | `bool`      | Sets if the title should be displayed on the bottom left   |
| `TitleBottomRight`        | `bool`      | Sets if the title should be displayed on the bottom right  |
| `TitleBottomCenter`       | `bool`      | Sets if the title should be displayed on the bottom center |
| `TextStyle`               | `*Style`    | Style of the content text                                  |
| `VerticalString`          | `string`    | Char used for vertical lines                               |
| `BoxStyle`                | `*Style`    | Style of the box                                           |
| `HorizontalString`        | `string`    | Character har used for horizontal lines                    |
| `TopRightCornerString`    | `string`    | Character used for the top right corner                    |
| `TopLeftCornerString`     | `string`    | Character used for the top left corner                     |
| `BottomLeftCornerString`  | `string`    | Character used for the bottom left corner                  |
| `BottomRightCornerString` | `string`    | Character used for the bottom right corner                 |
| `TopPadding`              | `int`       | Top space between content and box border                   |
| `BottomPadding`           | `int`       | Bottom space between content and box border                |
| `RightPadding`            | `int`       | Right space between content and box border                 |
| `LeftPadding`             | `int`       | Left space between content and box border                  |
| `Writer`                  | `io.Writer` | Custom writer                                              |

### Using Options

{% content-ref url="../../tutorials/using-printer-options.md" %}
[using-printer-options.md](../../tutorials/using-printer-options.md)
{% endcontent-ref %}

## Methods

{% hint style="info" %}
This printer implements the `RenderablePrinter` interface.
{% endhint %}

{% content-ref url="./" %}
[.](./)
{% endcontent-ref %}

| Method      | Description                                           |
| ----------- | ----------------------------------------------------- |
| `Render()`  | Prints to the terminal or uses the specified `Writer` |
| `Srender()` | Returns the rendered string                           |

## Full Specification

{% hint style="info" %}
pkg.go.dev contains the full specification for this printer and more technical descriptions.
{% endhint %}

{% embed url="https://pkg.go.dev/github.com/pterm/pterm#BoxPrinter" %}
