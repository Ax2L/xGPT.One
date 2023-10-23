# Confirm

{% embed url="https://raw.githubusercontent.com/pterm/pterm/master/_examples/interactive_confirm/demo/animation.svg" %}
[https://github.com/pterm/pterm/tree/master/\_examples/interactive\_confirm](https://github.com/pterm/pterm/tree/master/\_examples/interactive\_confirm)
{% endembed %}

## Basic Usage

```go
result, _ := pterm.DefaultInteractiveConfirm.Show()
pterm.Info.Printfln("You answered: %s", result)
```

## Options

| Name           | Type     | Description                                                               |
| -------------- | -------- | ------------------------------------------------------------------------- |
| `DefaultValue` | `bool`   | The value that is selected by default and submitted when enter is pressed |
| `DefaultText`  | `string` | Default prompt text                                                       |
| `TextStyle`    | `*Style` | Style of the prompt text                                                  |
| `ConfirmText`  | `string` | Text that is printed when "y" is pressed (defaults to "yes")              |
| `ConfirmStyle` | `*Style` | Style of the `ConfirmText`                                                |
| `RejectText`   | `string` | Text that is printed when "n" is pressed (defaults to "no")               |
| `RejectStyle`  | `*Style` | Style of the `RejectText`                                                 |
| `SuffixStyle`  | `*Style` | Style of the suffix                                                       |

### Using Options

{% content-ref url="../../tutorials/using-printer-options.md" %}
[using-printer-options.md](../../tutorials/using-printer-options.md)
{% endcontent-ref %}

## Methods

| Method       | Description                             |
| ------------ | --------------------------------------- |
| `Show(text)` | Displays the interactive confirm prompt |

## Full Specification

{% hint style="info" %}
pkg.go.dev contains the full specification for this printer and more technical descriptions.
{% endhint %}

{% embed url="https://pkg.go.dev/github.com/pterm/pterm#InteractiveConfirmPrinter" %}
