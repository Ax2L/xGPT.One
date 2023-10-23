---
description: The area printer can be used to display dynamically updating live content
---

# Area

{% embed url="https://raw.githubusercontent.com/pterm/pterm/master/_examples/area/demo/animation.svg" %}
[https://github.com/pterm/pterm/tree/master/\_examples/area](https://github.com/pterm/pterm/tree/master/\_examples/area)
{% endembed %}

## Basic Usage

```go
area, _ := pterm.DefaultArea.Start() // Start the Area printer.
for i := 0; i < 10; i++ {
    str, _ := pterm.DefaultBigText.WithLetters(pterm.NewLettersFromString(time.Now().Format("15:04:05"))).Srender() // Save current time in str.
    str = pterm.DefaultCenter.Sprint(str) // Center str.
    area.Update(str) // Update Area contents.
    time.Sleep(time.Second)
}
area.Stop()
```

## Options

| Name             | Type   | Description                                                |
| ---------------- | ------ | ---------------------------------------------------------- |
| `RemoveWhenDone` | `bool` | Sets if the area should be removed when `Stop()` is called |
| `Fullscreen`     | `bool` | Sets if the area should be the same size as the terminal   |
| `Center`         | `bool` | Sets if the content of the area should be centered         |

### Using Options

{% content-ref url="../../tutorials/using-printer-options.md" %}
[using-printer-options.md](../../tutorials/using-printer-options.md)
{% endcontent-ref %}

## Methods

| Name                          | Description                             |
| ----------------------------- | --------------------------------------- |
| `Clear()`                     | Clears the content of the area          |
| `GetContent()`                | Returns the current content of the area |
| `Update(text ...interface{})` | Updates the content of the area         |

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

{% embed url="https://pkg.go.dev/github.com/pterm/pterm#AreaPrinter" %}
