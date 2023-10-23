# Select

{% embed url="https://raw.githubusercontent.com/pterm/pterm/master/_examples/interactive_select/demo/animation.svg" %}
[https://github.com/pterm/pterm/tree/master/\_examples/interactive\_select](https://github.com/pterm/pterm/tree/master/\_examples/interactive\_select)
{% endembed %}

## Basic Usage

```go
result, _ := pterm.DefaultInteractiveSelect.
	WithOptions([]string{"a", "b", "c", "d"}).
	Show()
pterm.Info.Printfln("You answered: %s", result)
```

## Options

| Name            | Type       | Description                                                                          |
| --------------- | ---------- | ------------------------------------------------------------------------------------ |
| `DefaultText`   | `string`   | Default prompt text                                                                  |
| `TextStyle`     | `*Style`   | Style of the prompt text                                                             |
| `Options`       | `[]string` | List of menu options                                                                 |
| `OptionStyle`   | `*Style`   | Style of menu options                                                                |
| `DefaultOption` | `string`   | The option that is selected by default                                               |
| `MaxHeight`     | `int`      | Maximum number of visible options at once (the others can be accessed by scrolling)  |
| `Selector`      | `string`   | Character of the selector                                                            |
| `SelectorStyle` | `*Style`   | Style of the `Selector`                                                              |

### Using Options

{% content-ref url="../../tutorials/using-printer-options.md" %}
[using-printer-options.md](../../tutorials/using-printer-options.md)
{% endcontent-ref %}

## Methods

| Method       | Description                          |
| ------------ | ------------------------------------ |
| `Show(text)` | Displays the interactive select menu |

## Full Specification

{% hint style="info" %}
pkg.go.dev contains the full specification for this printer and more technical descriptions.
{% endhint %}

{% embed url="https://pkg.go.dev/github.com/pterm/pterm#InteractiveSelectPrinter" %}
