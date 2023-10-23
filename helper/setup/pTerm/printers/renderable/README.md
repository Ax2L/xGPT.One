# Renderable Printers

{% hint style="info" %}
Renderable printers print text similarily to text printers, but they do not share the same functions as fmt. They have a `Render()` and `Srender()` function. This is because the output is to complex and the printer has to be configured to use specific data via options.
{% endhint %}

## Interface

{% hint style="info" %}
PTerm exposes a `RenderablePrinter` interface.
{% endhint %}

| Method      | Description                                           |
| ----------- | ----------------------------------------------------- |
| `Render()`  | Prints to the terminal or uses the specified `Writer` |
| `Srender()` | Returns the rendered string                           |

### Full Specification

{% hint style="info" %}
pkg.go.dev contains the full specification for this interface and a more technical description.
{% endhint %}

{% embed url="https://pkg.go.dev/github.com/pterm/pterm#RenderablePrinter" %}