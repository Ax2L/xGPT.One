# Text Printers

{% hint style="info" %}
Text printers are printers, which can be used like the standard library's `fmt` package. They have functions, such as `Print()`, `Sprint()`, `Println()`, `Sprintln()`, `Printf()`, `Sprintf()`, `Printfln()`, `Sprintfln()`, etc.
{% endhint %}

## Interface

{% hint style="info" %}
PTerm exposes a `TextPrinter` interface.
{% endhint %}

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

### Full Specification

{% hint style="info" %}
pkg.go.dev contains the full specification for this interface and a more technical description.
{% endhint %}

{% embed url="https://pkg.go.dev/github.com/pterm/pterm#TextPrinter" %}
