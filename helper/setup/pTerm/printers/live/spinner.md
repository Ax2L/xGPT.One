---
description: >-
  The spinner printer can be used to show the user that the program is doing
  something in the background
---

# Spinner

{% embed url="https://raw.githubusercontent.com/pterm/pterm/master/_examples/spinner/demo/animation.svg" %}
[https://github.com/pterm/pterm/tree/master/\_examples/spinner](https://github.com/pterm/pterm/tree/master/\_examples/spinner)
{% endembed %}

## Basic Usage

```go
pterm.DefaultSpinner.Start()
// do something...
pterm.DefaultSpinner.Stop()
```

## Options

| Name                  | Type            | Description                                                   |
| --------------------- | --------------- | ------------------------------------------------------------- |
| `Text`                | `string`        | Message of the spinner                                        |
| `Sequence`            | `[]string`      | The spinner animation steps                                   |
| `Style`               | `*Style`        | Style of the spinner                                          |
| `Delay`               | `time.Duration` | Delay between animation steps                                 |
| `MessageStyle`        | `*Style`        | Style of the message                                          |
| `SuccessPrinter`      | `TextPrinter`   | Printer that is used when `Success()` is called               |
| `FailPrinter`         | `TextPrinter`   | Printer that is used when `Fail()` is called                  |
| `WarningPrinter`      | `TextPrinter`   | Printer that is used when `Warning()` is called               |
| `RemoveWhenDone`      | `bool`          | Sets if the spinner should be removed when `Stop()` is called |
| `ShowTimer`           | `bool`          | Sets if the timer should be displayed                         |
| `TimerRoundingFactor` | `time.Duration` | Rounding factor of the timer (seconds, milliseconds, etc.)    |
| `TimerStyle`          | `*Style`        | Style of the timer                                            |
| `IsActive`            | `bool`          | True when the spinner was started, but not yet stopped        |

### Using Options

{% content-ref url="../../tutorials/using-printer-options.md" %}
[using-printer-options.md](../../tutorials/using-printer-options.md)
{% endcontent-ref %}

## Methods

| Name                  | Description                                |
| --------------------- | ------------------------------------------ |
| `Fail(message)`       | Lets the spinner fail and prints a message |
| `Success(message)`    | Prints a success message                   |
| `Warning(message)`    | Prints a warning message                   |
| `UpdateText(message)` | Updates the spinner text                   |

{% hint style="info" %}
This printer implements the `LivePrinter` interface.
{% endhint %}

{% content-ref url="./" %}
[.](./)
{% endcontent-ref %}

| Method           | Description                                  |
| ---------------- | -------------------------------------------- |
| `Start()`        | Returns itself and errors                    |
| `Stop()`         | Returns itself and errors                    |
| `GenericStart()` | Returns the started `LivePrinter` and errors |
| `GenericStop()`  | Returns the stopped `LivePrinter` and errors |

## Full Specification

{% hint style="info" %}
pkg.go.dev contains the full specification for this printer and more technical descriptions.
{% endhint %}

{% embed url="https://pkg.go.dev/github.com/pterm/pterm#SpinnerPrinter" %}
