package main

// //region [ rgba(150, 150, 250, 0.1) ] Imports and Variables

import (
	"os"
	"os/exec"
	"path/filepath"
	"runtime"

	"github.com/pterm/pterm"
)

var (
	projectDir = getCurrentDirectory()
	lockFile   = filepath.Join(projectDir, "init.lock")
	githubLink = "https://github.com/Ax2L/xGPT.One"
)

// //endregion

// //region [ rgba(150, 250, 150, 0.1) ] Utility Functions

// clearTerminal clears the terminal screen based on the operating system.
func clearTerminal() {
	var cmd *exec.Cmd
	switch os := runtime.GOOS; os {
	case "windows":
		cmd = exec.Command("cmd", "/c", "cls")
	default:
		cmd = exec.Command("clear")
	}

	cmd.Stdout = os.Stdout
	cmd.Run()
}

// getCurrentDirectory retrieves and returns the current working directory.
func getCurrentDirectory() string {
	dir, err := os.Getwd()
	if err != nil {
		pterm.Fatal.Println("Failed to get the current directory:", err)
	}
	return dir
}

func displayHeader() {
	// Build on top of DefaultHeader
	pterm.DefaultHeader. // Use DefaultHeader as base
				WithMargin(15).
				WithBackgroundStyle(pterm.NewStyle(pterm.BgCyan)).
				WithTextStyle(pterm.NewStyle(pterm.FgBlack)).
				Println("This is a custom header!")
}

// //endregion

// //region [ rgba(250, 150, 250, 0.1) ] Core Functionality

// cleanDocker executes a shell script to clean Docker.
func cleanDocker() {
	pterm.DefaultSection.Println("Cleaning up Docker...")
	executeShellScript("helper/clean/cleanDocker_and_run.sh", "Failed to clean Docker:")
}

// runUpdateProduction executes a shell script to update the production environment.
func runUpdateProduction() {
	pterm.DefaultSection.Println("Running/Updating Production...")
	executeShellScript("scripts/runUpdateProduction.sh", "Failed to run/update production:")
}

// buildImage executes a shell script to build a Docker image.
func buildImage() {
	pterm.DefaultSection.Println("Building Image...")
	executeShellScript("scripts/buildImage.sh", "Failed to build image:")
}

// initiateEnvironment executes a shell script to initialize the environment.
func initiateEnvironment() {
	pterm.DefaultSection.Println("Initiating Environment...")
	executeShellScript("scripts/initEnvironment.sh", "Failed to initiate environment:")
}

// executeShellScript executes the specified shell script and displays logs based on its success or failure.
func executeShellScript(scriptPath string, errorMsg string) {
	cmd := exec.Command("sh", filepath.Join(projectDir, scriptPath))
	cmdOutput, err := cmd.CombinedOutput()
	if err != nil {
		pterm.Error.Println(errorMsg, string(cmdOutput))
		return
	}
	pterm.Success.Println("Operation completed successfully.")
}

// //endregion

// //region [ rgba(250, 250, 150, 0.1) ] Developer Functionality

// developerMenu provides options and functionality specific to developers.
// Note: To be implemented in the future.
func developerMenu() {
	pterm.Info.Println("Developer menu coming soon!")
}

// //endregion

// //region [ rgba(150, 150, 150, 0.1) ] Main Function

func main() {
	for {
		displayHeader()

		menuItems := []string{
			"Run/Update Production",
			"Build Image",
			"Developer-Menu",
			"Clean Docker",
			"Initiate Environment",
			"Exit",
		}

		selectedItem, err := pterm.DefaultInteractiveSelect.
			WithOptions(menuItems).
			Show()
		if err != nil {
			pterm.Error.Println("Menu selection error:", err)
			continue
		}

		switch selectedItem {
		case "Run/Update Production":
			runUpdateProduction()
		case "Build Image":
			buildImage()
		case "Developer-Menu":
			developerMenu()
		case "Clean Docker":
			cleanDocker()
		case "Initiate Environment":
			initiateEnvironment()
		case "Exit":
			exitMsg := pterm.DefaultCenter.Sprintf("👋 Exiting... See you next time in the AI universe! 👋")
			pterm.DefaultBox.Println(exitMsg)
			return
		default:
			pterm.Error.Println("Invalid choice. Please try again.")
		}
	}
}

// //endregion
