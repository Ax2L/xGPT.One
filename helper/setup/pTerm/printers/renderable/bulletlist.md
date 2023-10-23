---
description: The bullet list printer can be used to display a bullet list
---

# BulletList

{% embed url="https://raw.githubusercontent.com/pterm/pterm/master/_examples/bulletlist/demo/animation.svg" %}
[https://github.com/pterm/pterm/tree/master/\_examples/bulletlist](https://github.com/pterm/pterm/tree/master/\_examples/bulletlist)
{% endembed %}

## Basic Usage

```go
pterm.DefaultBulletList.WithItems([]pterm.BulletListItem{
    {Level: 0, Text: "Level 0"},
    {Level: 1, Text: "Level 1"},
    {Level: 2, Text: "Level 2"},
}).Render()
```

## Options

| Name          | Type               | Description                                               |
| ------------- | ------------------ | --------------------------------------------------------- |
| `Items`       | `[]BulletListItem` | Items of the bullet list                                  |
| `TextStyle`   | `*Style`           | Style of the text                                         |
| `Bullet`      | `string`           | Character that is used in front of the items              |
| `BulletStyle` | `*Style`           | Style of the character that is used in front of the items |
| `Writer`      | `io.Writer`        | Custom output writer                                      |

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

{% embed url="https://pkg.go.dev/github.com/pterm/pterm#BulletListPrinter" %}
