# Live Printers

{% hint style="info" %}
Live printers can update their output dynamically and are therefore well suited to display changing data like progress bars and live charts. They feature a `Start()` and `Stop()` method.
{% endhint %}

Interface

{% hint style="info" %}
PTerm exposes a `LivePrinter` interface.
{% endhint %}

| Method           | Description                                  |
| ---------------- | -------------------------------------------- |
| `Start()`        | Returns itself and errors                    |
| `Stop()`         | Returns itself and errors                    |
| `GenericStart()` | Returns the started `LivePrinter` and errors |
| `GenericStop()`  | Returns the stopped `LivePrinter` and errors |

### Full Specification

{% hint style="info" %}
pkg.go.dev contains the full specification for this interface and a more technical description.
{% endhint %}

{% embed url="https://pkg.go.dev/github.com/pterm/pterm#LivePrinter" %}