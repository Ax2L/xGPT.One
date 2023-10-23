---
description: Welcome to the documentation of PTerm - a TUI framework for Go
---

# 👋 Welcome

✨ PTerm is a modern TUI framework written in Go to beautify console output.

It supports interactive printers, such as select menus and confirm prompts, as well as live printers, such as progress bars and spinners. It also features text printers for sections, headers, and info/warning/... messages. 🦕

PTerm has support for visualization, with printers such as bar charts, tables, trees and much more. You can also create custom layouts with grid panels and centered content. 📊

It's completely configurable and 100% cross-platform compatible. 🚀

{% embed url="https://raw.githubusercontent.com/pterm/pterm/master/_examples/demo/demo/animation.svg" %}
Demo written with PTerm in Go
{% endembed %}

## Easy to Use

{% hint style="info" %}
PTerm is super simple to use. It has predefined components (called printers), which do all the work for you.
{% endhint %}

### Prefix Example

```go
// Enable debug messages.
pterm.EnableDebugMessages()

pterm.Debug.Println("Hello, World!")                                                // Print Debug.
pterm.Info.Println("Hello, World!")                                                 // Print Info.
pterm.Success.Println("Hello, World!")                                              // Print Success.
pterm.Warning.Println("Hello, World!")                                              // Print Warning.
pterm.Error.Println("Errors show the filename and linenumber inside the terminal!") // Print Error.
pterm.Info.WithShowLineNumber().Println("Other PrefixPrinters can do that too!")    // Print Error.
pterm.Fatal.Println("Hello, World!") // Print Fatal.
```

![](<.gitbook/assets/image (1).png>)

### Header Example

```go
pterm.DefaultHeader.Println("This is the default header!")
pterm.Println() // spacer
pterm.DefaultHeader.WithFullWidth().Println("This is a full-width header.")
```

![](.gitbook/assets/image.png)

### Table Example

```go
// Create a fork of the default table, fill it with data and print it.
// Data can also be generated and inserted later.
pterm.DefaultTable.WithHasHeader().WithData(pterm.TableData{
	{"Firstname", "Lastname", "Email"},
	{"Paul", "Dean", "nisi.dictum.augue@velitAliquam.co.uk"},
	{"Callie", "Mckay", "egestas.nunc.sed@est.com"},
	{"Libby", "Camacho", "aliquet.lobortis@semper.com"},
}).Render()
```

![](<.gitbook/assets/image (2).png>)

### Progressbar Example

```go
// Slice of strings with placeholder text.
var fakeInstallList = strings.Split("pseudo-excel pseudo-photoshop pseudo-chrome pseudo-outlook pseudo-explorer pseudo-dops pseudo-git pseudo-vsc pseudo-intellij pseudo-minecraft pseudo-scoop pseudo-chocolatey", " ")

// Create progressbar as fork from the default progressbar.
p, _ := pterm.DefaultProgressbar.WithTotal(len(fakeInstallList)).WithTitle("Downloading stuff").Start()

for i := 0; i < p.Total; i++ {
	p.UpdateTitle("Downloading " + fakeInstallList[i])         // Update the title of the progressbar.
	pterm.Success.Println("Downloading " + fakeInstallList[i]) // If a progressbar is running, each print will be printed above the progressbar.
	p.Increment()                                              // Increment the progressbar by one. Use Add(x int) to increment by a custom amount.
	time.Sleep(time.Millisecond * 350)                         // Sleep 350 milliseconds.
}
```

{% embed url="https://raw.githubusercontent.com/pterm/pterm/master/_examples/progressbar/demo/animation.svg" %}

### More examples

{% hint style="info" %}
Click the link below to see all examples!
{% endhint %}

{% embed url="https://github.com/pterm/pterm/tree/master/_examples" %}
