# TextInput

{% embed url="https://raw.githubusercontent.com/pterm/pterm/master/_examples/interactive_textinput/demo/animation.svg" %}
[https://github.com/pterm/pterm/tree/master/\_examples/interactive\_textinput](https://github.com/pterm/pterm/tree/master/\_examples/interactive\_textinput)
{% endembed %}

## Basic Usage

```go
result, _ := pterm.DefaultInteractiveTextInput.Show()
pterm.Info.Printfln("You answered: %s", result)
```

## Options

| Name          | Type     | Description                                            |
| ------------- | -------- | ------------------------------------------------------ |
| `TextStyle`   | `*Style` | Style of the text prompt                               |
| `DefaultText` | `string` | Default prompt text                                    |
| `MultiLine`   | `bool`   | Sets if the input should accept multiple lines of text |

### Using Options

{% content-ref url="../../tutorials/using-printer-options.md" %}
[using-printer-options.md](../../tutorials/using-printer-options.md)
{% endcontent-ref %}

## Methods

| Method       | Description                               |
| ------------ | ----------------------------------------- |
| `Show(text)` | Displays the interactive text input field |

## Full Specification

{% hint style="info" %}
pkg.go.dev contains the full specification for this printer and more technical descriptions.
{% endhint %}

{% embed url="https://pkg.go.dev/github.com/pterm/pterm#InteractiveTextInputPrinter" %}
