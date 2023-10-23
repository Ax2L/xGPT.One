---
description: The big text printer can be used to write big headlines
---

# BigText

{% embed url="https://raw.githubusercontent.com/pterm/pterm/master/_examples/bigtext/demo/animation.svg" %}
[https://github.com/pterm/pterm/tree/master/\_examples/bigtext](https://github.com/pterm/pterm/tree/master/\_examples/bigtext)
{% endembed %}

## Basic Usage

```go
// Print a large text with the LetterStyle from the standard theme.
// Useful for title screens.
pterm.DefaultBigText.WithLetters(putils.LettersFromString("PTerm")).Render()

// Print a large text with differently colored letters.
pterm.DefaultBigText.WithLetters(
    putils.LettersFromStringWithStyle("P", pterm.NewStyle(pterm.FgCyan)),
    putils.LettersFromStringWithStyle("Term", pterm.NewStyle(pterm.FgLightMagenta))).
    Render()

// LettersFromStringWithRGB can be used to create a large text with a specific RGB color.
pterm.DefaultBigText.WithLetters(
    putils.LettersFromStringWithRGB("PTerm", pterm.NewRGB(255, 215, 0))).
    Render()
```

## Options

| Name            | Type                | Description                                       |
| --------------- | ------------------- | ------------------------------------------------- |
| `BigCharacters` | `map[string]string` | Dictonary to convert normal letters into big ones |
| `Letters`       | `Letters`           | Styled letters                                    |
| `Writer`        | `io.Writer`         | Sets a custom writer                              |

### Using Options

{% content-ref url="../../tutorials/using-printer-options.md" %}
[using-printer-options.md](../../tutorials/using-printer-options.md)
{% endcontent-ref %}

## Methods

{% hint style="info" %}
This printer implements the `RenderablePrinter` interface.
{% endhint %}

{% content-ref url="./" %}
[.](./)
{% endcontent-ref %}

| Method      | Description                                           |
| ----------- | ----------------------------------------------------- |
| `Render()`  | Prints to the terminal or uses the specified `Writer` |
| `Srender()` | Returns the rendered string                           |

## Full Specification

{% hint style="info" %}
pkg.go.dev contains the full specification for this printer and more technical descriptions.
{% endhint %}

{% embed url="https://pkg.go.dev/github.com/pterm/pterm#BigTextPrinter" %}
