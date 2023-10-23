# Multiselect

{% embed url="https://raw.githubusercontent.com/pterm/pterm/master/_examples/interactive_multiselect/demo/animation.svg" %}
[https://github.com/pterm/pterm/tree/master/\_examples/interactive\_multiselect](https://github.com/pterm/pterm/tree/master/\_examples/interactive\_multiselect)
{% endembed %}

## Basic Usage

```go
result, _ := pterm.DefaultInteractiveMultiselect.
	WithOptions([]string{"a", "b", "c", "d"}).
	Show()
pterm.Info.Printfln("You answered: %s", result)
```

## Options

| Name             | Type       | Description                                                                          |
| ---------------- | ---------- | ------------------------------------------------------------------------------------ |
| `DefaultText`    | `string`   | Default prompt text                                                                  |
| `TextStyle`      | `*Style`   | Style of the prompt text                                                             |
| `Options`        | `[]string` | List of menu options                                                                 |
| `OptionStyle`    | `*Style`   | Style of menu options                                                                |
| `DefaultOptions` | `[]string` | Options, which should be selected by default                                         |
| `MaxHeight`      | `int`      | Maximum number of visible options at once (the others can be accessed by scrolling)  |
| `Selector`       | `string`   | Character of the selector                                                            |
| `SelectorStyle`  | `*Style`   | Style of the `Selector`                                                              |

### Using Options

{% content-ref url="../../tutorials/using-printer-options.md" %}
[using-printer-options.md](../../tutorials/using-printer-options.md)
{% endcontent-ref %}

## Methods

| Method       | Description                               |
| ------------ | ----------------------------------------- |
| `Show(text)` | Displays the interactive multiselect menu |

## Full Specification

{% hint style="info" %}
pkg.go.dev contains the full specification for this printer and more technical descriptions.
{% endhint %}

{% embed url="https://pkg.go.dev/github.com/pterm/pterm#InteractiveMultiselectPrinter" %}
