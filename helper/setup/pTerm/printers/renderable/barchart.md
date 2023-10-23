---
description: The bar chart printer can be used to show data in relation to each other
---

# BarChart

{% embed url="https://raw.githubusercontent.com/pterm/pterm/master/_examples/barchart/demo/animation.svg" %}
[https://github.com/pterm/pterm/tree/master/\_examples/barchart](https://github.com/pterm/pterm/tree/master/\_examples/barchart)
{% endembed %}

## Basic Usage

```go
positiveBars := pterm.Bars{
	pterm.Bar{
		Label: "Bar 1",
		Value: 5,
	},
	pterm.Bar{
		Label: "Bar 2",
		Value: 3,
	},
	pterm.Bar{
		Label: "Longer Label",
		Value: 7,
	},
}

pterm.Info.Println("Chart example with positive only values (bars use 100% of chart area)")

pterm.DefaultBarChart.WithBars(positiveBars).Render()
pterm.DefaultBarChart.WithHorizontal().WithBars(positiveBars).Render()
```

## Options

| Name                   | Type        | Description             |
| ---------------------- | ----------- | ----------------------- |
| `Root`                 | `TreeNode`  | The structured tree     |
| `TreeStyle`            | `*Style`    | Style of the tree       |
| `TextStyle`            | `*Style`    | Style of the text       |
| `TopRightCornerString` | `string`    | Top right corner string |
| TopRightDownString     | `string`    | Top right down string   |
| HorizontalString       | `string`    | Horizontal string       |
| VerticalString         | `string`    | Vertical string         |
| RightDownLeftString    | `string`    | Right down left string  |
| Indent                 | `int`       | Space between levels    |
| `Writer`               | `io.Writer` | Sets a custom writer    |

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

{% embed url="https://pkg.go.dev/github.com/pterm/pterm#BarChartPrinter" %}
