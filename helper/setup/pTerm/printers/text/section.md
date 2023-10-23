---
description: The section printer can be used to separate sections
---

# Section

{% embed url="https://raw.githubusercontent.com/pterm/pterm/master/_examples/section/demo/animation.svg" %}
[https://github.com/pterm/pterm/tree/master/\_examples/section](https://github.com/pterm/pterm/tree/master/\_examples/section)
{% endembed %}

## Basic Usage

```go
pterm.DefaultSection.Println("Hello, World!")
```

## Options

| Name              | Type        | Description                                          |
| ----------------- | ----------- | ---------------------------------------------------- |
| `TextStyle`       | `*Style`    | Style of the text                                    |
| `BackgroundStyle` | `*Style`    | Style of the header background                       |
| `Margin`          | `int`       | Empty space to the sides                             |
| `FullWidth`       | `bool`      | Sets if the header should be as wide as the terminal |
| `Writer`          | `io.Writer` | Sets a custom writer                                 |

### Using Options

{% content-ref url="../../tutorials/using-printer-options.md" %}
[using-printer-options.md](../../tutorials/using-printer-options.md)
{% endcontent-ref %}

## Methods

{% hint style="info" %}
This printer implements the `TextPrinter` interface.
{% endhint %}

{% content-ref url="./" %}
[.](./)
{% endcontent-ref %}

| Method                                           | Description                                                                                                                                   |
| ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `Sprint(a ...interface{})`                       | Returns a string                                                                                                                              |
| `Sprintln(a ...interface{})`                     | Returns a string with a new line at the end                                                                                                   |
| `Sprintf(format string, a ...interface{})`       | Returns a string, formatted according to a format specifier                                                                                   |
| `Sprintfln(format string, a ...interface{})`     | Returns a string, formatted according to a format specifier with a new line at the end                                                        |
| `Print(a ...interface{})`                        | Prints to the terminal (or specified custom `Writer`)                                                                                         |
| `Println(a ...interface{})`                      | Prints to the terminal (or specified custom `Writer`) with a new line at the end                                                              |
| `Printf(format string, a ...interface{})`        | Prints to the terminal (or specified custom `Writer`), formatted according to a format specifier                                              |
| `Printfln(format string, a ...interface{})`      | Prints to the terminal (or specified custom `Writer`), formatted according to a format specifier with a new line at the end                   |
| `PrintOnError(a ...interface{})`                 | Prints every error which is not nil. If every error is nil, nothing will be printed. This can be used for simple error checking.              |
| `PrintOnErrorf(format string, a ...interface{})` | Wraps every error which is not nil and prints it. If every error is nil, nothing will be printed. This can be used for simple error checking. |

## Full Specification

{% hint style="info" %}
pkg.go.dev contains the full specification for this printer and more technical descriptions.
{% endhint %}

{% embed url="https://pkg.go.dev/github.com/pterm/pterm#SectionPrinter" %}
