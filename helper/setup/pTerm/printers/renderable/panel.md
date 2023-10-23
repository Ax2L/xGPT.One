---
description: >-
  The panel printer can be used to create multiple spaces in the terminal, which
  can have different content
---

# Panel

{% embed url="https://raw.githubusercontent.com/pterm/pterm/master/_examples/panel/demo/animation.svg" %}
[https://github.com/pterm/pterm/tree/master/\_examples/panel](https://github.com/pterm/pterm/tree/master/\_examples/panel)
{% endembed %}

## Basic Usage

```go
// Declare panels in a two dimensional grid system.
panels := pterm.Panels{
  {{Data: "This is the first panel"}, {Data: pterm.DefaultHeader.Sprint("Hello, World!")}, {Data: "This\npanel\ncontains\nmultiple\nlines"}},
  {{Data: pterm.Red("This is another\npanel line")}, {Data: "This is the second panel\nwith a new line"}},
}

// Print panels.
pterm.DefaultPanel.WithPanels(panels).Render()
```

## Options

| Name              | Type         | Description                                                                          |
| ----------------- | ------------ | ------------------------------------------------------------------------------------ |
| `Panels`          | `Panels`     | The different panels which should be printed                                         |
| `Padding`         | `int`        | Padding to the side of the panels                                                    |
| `BottomPadding`   | `int`        | Padding to the bottom of the panels                                                  |
| `SameColumnWidth` | `bool`       | Sets if every panel should have the same column width                                |
| `BoxPrinter`      | `BoxPrinter` | Sets a box printer, which the panel printer should use to add a border to the panels |
| `Writer`          | `io.Writer`  | Custom output writer                                                                 |

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

{% embed url="https://pkg.go.dev/github.com/pterm/pterm#PanelPrinter" %}
