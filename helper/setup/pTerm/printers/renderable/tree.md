---
description: The tree printer can be used to display a hierarchy
---

# Tree

{% embed url="https://raw.githubusercontent.com/pterm/pterm/master/_examples/tree/demo/animation.svg" %}
[https://github.com/pterm/pterm/tree/master/\_examples/tree](https://github.com/pterm/pterm/tree/master/\_examples/tree)
{% endembed %}

## Basic Usage

```go
pterm.DefaultTree.WithRoot(putils.NewTreeFromLeveledList(pterm.LeveledList{
    pterm.LeveledListItem{Level: 0, Text: "Hello, World!"}
    pterm.LeveledListItem{Level: 1, Text: "Hello, World2!"}
})).Render()
```

## Options

| Name                   | Type        | Description                           |
| ---------------------- | ----------- | ------------------------------------- |
| `Root`                 | `TreeNode`  | The structured tree                   |
| `TreeStyle`            | `*Style`    | Style of the tree                     |
| `TextStyle`            | `*Style`    | Style of the text                     |
| `TopRightCornerString` | `string`    | Top right corner string               |
| `TopRightDownString`   | `string`    | Top right down string                 |
| `HorizontalString`     | `string`    | Horizontal line string                |
| `VerticalString`       | `string`    | Vertical line string                  |
| `RightDownLeftString`  | `string`    | Right down left string                |
| `Indent`               | `int`       | How much the items should be indented |
| `Writer`               | `io.Writer` | Custom output writer                  |

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

{% embed url="https://pkg.go.dev/github.com/pterm/pterm#TreePrinter" %}
