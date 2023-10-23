# Getting Started

## Adding PTerm to Your Project

{% hint style="info" %}
Make sure to run this command inside your project, when you’re using go modules 😉
{% endhint %}

{% code title="PTerm Installation Command" %}
```bash
go get github.com/pterm/pterm
```
{% endcode %}

## Write Your First `Hello World` App With PTerm

```go
package main

import (
	"github.com/pterm/pterm"
	"github.com/pterm/pterm/putils" 
)

func main() {
	// Create a new header as a fork from pterm.DefaultHeader.
	// ┌ new header variable
	// │                 ┌ Fork it from the default header
	// │                 │            ┌ Set options
	header := pterm.DefaultHeader.WithBackgroundStyle(pterm.NewStyle(pterm.BgRed))

	// Print the header centered in your terminal.
	//      ┌ Use the default CenterPrinter
	//      │              ┌ Print a string ending with a new line
	//      │              │      ┌ Use our new header to format the input string
	pterm.DefaultCenter.Println(header.Sprint("Hello, World"))

	// Print a big text to the terminal.
	//          ┌ Use the default BigTextPrinter
	//          │              ┌ Set the Letters option
	//          |              |            ┌ Use the PTerm Utils (putils) package to create objects faster
	//          │              │            |           ┌ Generate Letters from string
	//          │              │            |           |                     ┌ Render output to the console
	_ = pterm.DefaultBigText.WithLetters(putils.LettersFromString("Hello")).Render()

	// ┌──────────────────────────────────────────────────────────┐
	// │There are many more features, which are waiting for you :)│
	// └──────────────────────────────────────────────────────────┘

	// TODO: If you want, you can try to make the big text centered.
}
```

## The 4 Printer Categories

If you want to start with PTerm, you have to know the 4 printer categories.

### Interactive Printers

{% hint style="info" %}
Interactive printers respond to user input. Similar to live printers, interactive printers can update their output. This allows the creation of interactive menus and queries. The `Show()` method shows the interactive prompt in the terminal.&#x20;
{% endhint %}

If you need a printer, which a user can interact with, look here:

{% content-ref url="printers/interactive.md" %}
[interactive.md](printers/interactive.md)
{% endcontent-ref %}

#### Can be used for

* Select Menus
* Confirm Prompts
* User Text Input
* ...

### Live Printers

{% hint style="info" %}
Live printers can update their output dynamically and are therefore well suited to display changing data like progress bars and live charts. They feature a `Start()` and `Stop()` method.
{% endhint %}

If you need a printer, which can update its own content, look here:

{% content-ref url="printers/live/" %}
[live](printers/live/)
{% endcontent-ref %}

#### Can be used for

* Live Performance Tracking
* Visualizing Progress
* Live Charts
* Live System Stats
* ....&#x20;

### Renderable Printers

{% hint style="info" %}
Renderable printers print text similarily to text printers, but they do not share the same functions as fmt. They have a `Render()` and `Srender()` function. This is because the output is to complex and the printer has to be configured to use specific data via options.
{% endhint %}

If you need a printer, which prints complex output from some sort of data, look here:

{% content-ref url="printers/renderable/" %}
[renderable](printers/renderable/)
{% endcontent-ref %}

#### Can be used for

* Charts
* Tables
* Statistics
* ...

### Text Printers

{% hint style="info" %}
Text printers are printers, which can be used like the standard library's `fmt` package. They have functions, such as `Print()`, `Sprint()`, `Println()`, `Sprintln()`, `Printf()`, `Sprintf()`, `Printfln()`, `Sprintfln()`, etc.
{% endhint %}

If you need a printer, which has a single text input, look here:

{% content-ref url="printers/text/" %}
[text](printers/text/)
{% endcontent-ref %}

#### Can be used for

* Debug / Info / Warning / Error / ... Messages
* Headers
* Sections
* Paragraphs
* ...
