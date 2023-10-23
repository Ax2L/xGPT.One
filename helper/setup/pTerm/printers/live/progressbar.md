---
description: >-
  The progress bar printer can be used to display the current progress of an
  action
---

# Progressbar

{% embed url="https://raw.githubusercontent.com/pterm/pterm/master/_examples/progressbar/demo/animation.svg" %}
[https://github.com/pterm/pterm/tree/master/\_examples/progressbar](https://github.com/pterm/pterm/tree/master/\_examples/progressbar)
{% endembed %}

## Basic Usage

```go
progressbar := pterm.DefaultProgressbar.WithTotal(totalSteps).Start()
// Logic here
progressbar.Increment()
// More logic
```

## Options

| Name                        | Type            | Description                                                                         |
| --------------------------- | --------------- | ----------------------------------------------------------------------------------- |
| `Title`                     | `string`        | Title of the progress bar                                                           |
| `Total`                     | `int`           | Total amount of steps                                                               |
| `Current`                   | `int`           | Current amount of steps                                                             |
| `BarCharacter`              | `string`        | Character that should be used for the bar filling                                   |
| `LastCharacter`             | `string`        | Las character of the progress bar                                                   |
| `ElapsedTimeRoundingFactor` | `time.Duration` | Factor that determines how the time should be rounded (seconds, milliseconds, etc.) |
| `BarFiller`                 | `string`        | Character that is used when the bar has not yet reached its point                   |
| `MaxWidth`                  | `int`           | Maximum width of the progress bar                                                   |
| `ShowElapsedTime`           | `bool`          | Sets if the elapsed time should be displayed                                        |
| `ShowCount`                 | `bool`          | Sets if the current and total amount of steps should be displayed                   |
| `ShowTitle`                 | `bool`          | Sets if the title should be displayed                                               |
| `ShowPercentage`            | `bool`          | Sets if the current percentage should be displayed                                  |
| `RemoveWhenDone`            | `bool`          | Sets if the progress bar should be removed when `Stop()` is called                  |
| `TitleStyle`                | `*Style`        | Style of the title                                                                  |
| `BarStyle`                  | `*Style`        | Style of the progress bar itself                                                    |
| `IsActive`                  | `bool`          | True when the progress bar was started but not yet stopped                          |

### Using Options

{% content-ref url="../../tutorials/using-printer-options.md" %}
[using-printer-options.md](../../tutorials/using-printer-options.md)
{% endcontent-ref %}

## Methods

| Name               | Description                                                                       |
| ------------------ | --------------------------------------------------------------------------------- |
| `Add(count int)`   | Adds `count` to the current progress                                              |
| `GetElapsedTime()` | Returns the duration since the progress bar was started                           |
| `Increment()`      | Adds `1` to the current progress - you can call this function when a step is done |
| `UpdateTitle()`    | Updates and re-renders the title of the progress bar                              |

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

{% embed url="https://pkg.go.dev/github.com/pterm/pterm#ProgressbarPrinter" %}
