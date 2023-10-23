package main

import (
	"log"

	"github.com/pterm/pterm"
)

func mai213n() {
	_createAliases()
	_configureWidgets()
	_defineLayout()
}

func _createAliases() {
	// Define your TIM aliases here.
}

func _configureWidgets() {
	// Define your global widget configurations here.
	pterm.Style = pterm.NewStyle(pterm.FgLightWhite)

	// Example: pterm.ButtonStyles.Primary = "myapp.button.label"
}

func _defineLayout() {
	layout := pterm.NewLayout()

	header := pterm.NewWindow().
		WithBox(pterm.NewBox("", pterm.BoxDrawingsLight))
	header.Content.Print("xGPT.One - AI Powered. Human Inspired.")
	layout.Add(header)

	body := pterm.NewWindow().
		WithBox(pterm.NewBox("", pterm.BoxDrawingsLight))
	body.Content.Print("My body window")
	layout.Add(body)

	bodyRight := pterm.NewWindow().
		WithBox(pterm.NewBox("", pterm.BoxDrawingsLight))
	bodyRight.Content.Print("My sidebar")
	layout.Add(bodyRight)

	footer := pterm.NewWindow().
		WithBox(pterm.NewBox("", pterm.BoxDrawingsLight))
	footer.Content.Print("Quit")
	layout.Add(footer)

	layout.Run()
	log.Println("Goodbye!")
}
