---
description: The table printer can be used to display structured data
---

# Table

{% embed url="https://raw.githubusercontent.com/pterm/pterm/master/_examples/table/demo/animation.svg" %}
[https://github.com/pterm/pterm/tree/master/\_examples/table](https://github.com/pterm/pterm/tree/master/\_examples/table)
{% endembed %}

## Basic Usage

```go
pterm.DefaultTable.WithData(pterm.TableData{
    {"Paul", "Dean", "nisi.dictum.augue@velitAliquam.co.uk"},
    {"Callie", "Mckay", "egestas.nunc.sed@est.com"},
    {"Libby", "Camacho", "aliquet.lobortis@semper.com"},
}).Render()
```

## Options

| Name                      | Type        | Description                                           |
| ------------------------- | ----------- | ----------------------------------------------------- |
| `Style`                   | `*Style`    | Style of the table                                    |
| `HasHeader`               | `bool`      | Sets if the table has a headline                      |
| `HeaderStyle`             | `*Style`    | Style of the table headline                           |
| `HeaderRowSeparator`      | `string`    | Row separator in the table headline                   |
| `HeaderRowSeparatorStyle` | `*Style`    | Style of the headline row separator                   |
| `Separator`               | `string`    | Character which is used to separate columns           |
| `SeparatorStyle`          | `*Style`    | Style for the separator                               |
| `RowSeparator`            | `string`    | Character which is used to separate rows              |
| `RowSeparatorStyle`       | `*Style`    | Style for the row separator                           |
| `Data`                    | `TableData` | The table content                                     |
| `Boxed`                   | `bool`      | Sets if the table should be printed with a border box |
| `LeftAlignment`           | `bool`      | Sets if the text should be aligned to the left        |
| `RightAlignment`          | `bool`      | Sets if the text should be aligned to the right       |
| `Writer`                  | `io.Writer` | Custom output writer                                  |

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

{% embed url="https://pkg.go.dev/github.com/pterm/pterm#TablePrinter" %}
