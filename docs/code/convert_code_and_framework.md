#? Create a Script that does exactly the same as:

# SOURCE (main.sh):
```
#!/bin/bash
# scripts/main.sh

# Initialize PROJECT_DIR
PROJECT_DIR=$(pwd)
export PROJECT_DIR

# Lock file path
LOCK_FILE="$PROJECT_DIR/init.lock"

# GitHub Link
GITHUB_LINK="https://github.com/Ax2L/xGPT.One"

#echo "PROJECT_DIR IS: $PROJECT_DIR"

# region [ rgba(255, 0, 0, 0.05)]
# ####################################### #
#    DO NOT MODIFY THIS FILE DIRECTLY     # 
#   Use .env for all configurations   #
# ####################################### #
# endregion

#// region [ rgba(0, 105, 255, 0.05)]
#*||--------------------------------------------------------------------------------||
#*||                                    Functions                                   ||
#*||--------------------------------------------------------------------------------||

# Function to display header with GitHub link
display_header() {
  echo "#######################################################"
  echo "#                    xGPT.One                         #"
  echo "#                                                     #"
  echo "#     🤖 AI Powered. Human Inspired. 🌍               #"
  echo "#                                                     #"
  echo "#     GitHub: $GITHUB_LINK        #"
  echo "#######################################################"
  echo "## 🚀 Mission Phase: $1 🚀"
}

# Function to clean Docker
clean_docker() {
  echo "Cleaning up Docker..."
  sh $PROJECT_DIR/helper/clean/cleanDocker_and_run.sh || {
    echo "Failed to clean Docker"
  }
  echo "Docker cleaned successfully."
}

# Function to initiate environment
init_environment() {
  if [ -f "$LOCK_FILE" ]; then
    echo "Init script is already running. Please wait..."
    return
  fi
  touch "$LOCK_FILE"
  echo "Initiating environment..."
  "$PROJECT_DIR/init.sh" & 
  wait
  rm "$LOCK_FILE"
  echo "Environment initiated successfully."
}

# Function to load environment variables from .env file
load_env() {
  echo "Load Envirement File .env"
  cp "$PROJECT_DIR/config/global/.env" "$PROJECT_DIR/.env" || true  

  if [ -f "$PROJECT_DIR/.env" ]; then
    echo "🔄 Loading environment variables..."
    export $(grep -v '^#' "$PROJECT_DIR/.env" | xargs)
  else
    echo "🔴 No .env file found. 🔴"
  fi
}


# Function to build Docker Compose config using Python helper script
build_docker_compose() {
  load_env
  echo "Generating docker-compose.yml..."
  python3 $PROJECT_DIR/scripts/build_docker-compose.yml.py || {
    echo "Failed to build docker-compose.yml"
    exit 1
  }
}

# Function to build Docker image
build_docker() {
  load_env # Load the environment variables
  # setup_virtualenv # Set up Python virtual environment

  echo "Building Docker Image..."
  pwd || {
    echo "Failed to change directory to apps/xgpt/"
    exit 1
  }
  # build_docker_compose # Build docker-compose.yml
  docker build -f $PROJECT_DIR/apps/xgpt/docker/Dockerfile . -t "xgpt-streamlit" || {
    echo "Failed to build Docker image"
    exit 1
  }
  cd $PROJECT_DIR || {
    echo "Failed to navigate back to root folder"
    exit 1
  }
  echo "Docker image built successfully."
}


# Function to run Docker
run_docker() {
  load_env
  wait
  echo "Creating Docker network..."
  docker network create xgpt || {
    echo "Docker network exists or failed to create"
  }
  echo "Running/Updating Production..."
  cd $PROJECT_DIR/apps/xgpt/docker || {
  cp $PROJECT_DIR/apps/xgpt/.env $PROJECT_DIR/apps/xgpt/docker/.env || true
    echo "Failed to change directory to apps/xgpt/"
    exit 1
  }
  #build_docker_compose # Build docker-compose.yml
  docker-compose up -d || {
    echo "Failed to run Docker"
    exit 1
  }
  cd $PROJECT_DIR || {
    echo "Failed to navigate back to root folder"
    exit 1
  }
  echo "Production running/updating successfully."
}

# Function to run local dev
run_local_dev() {
  load_env
  echo "Running local dev..."
  ./apps/xgpt/dev.sh || {
    echo "Failed to run local dev"
    exit 1
  }
  cd $PROJECT_DIR || {
    echo "Failed to navigate back to root folder"
    exit 1
  }
  echo "Local dev running successfully."
}

# Function to run local db
run_local_db() {
  load_env
  echo "Running local db..."
  docker-compose -f docker-compose-db-only.yml up -d || {
    echo "Failed to run local db"
    exit 1
  }
  cd $PROJECT_DIR || {
    echo "Failed to navigate back to root folder"
    exit 1
  }
  echo "Local db running successfully."
}



#// endregion

#// region [ rgba(100, 15, 100, 0.05)]
#?||--------------------------------------------------------------------------------||
#?||                               Init .env                                    ||
#?||--------------------------------------------------------------------------------||
# Copy initial configuration files only if config/global/.env doesn't exist, use the template as default.
if [ ! -f "config/global/.env" ]; then
    cp config/global/one.template.env config/global/.env || true
fi
# Copy the .env into xgpt to use it for its container.
cp config/global/.env apps/xgpt/.env || true
# Copy .env into the docker folder.
cp config/global/.env apps/xgpt/docker/.env || true
# Copy now the user config.yaml.
cp config/user/config.yaml apps/xgpt/config.yaml || true
# Copy the Streamlit Theme and default sqldb user
cp -r config/streamlit apps/xgpt/.streamlit || true
# Copy the pyproject.toml inside the xgpt directory
cp pyproject.toml apps/xgpt/pyproject.toml || true
# Now source the final .env and proceed.
source config/global/.env || handle_error "Activating AI Environment Failed"
#// endregion


# Main execution
while true; do
  display_header "Main Menu"
  
  echo "Choose an option:"
  echo "1) Run/Update Production"
  echo "2) Build Image"
  echo "3) Developer-Menu"
  echo "4) Clean Docker"
  
  [ ! -f "$LOCK_FILE" ] && echo "5) Initiate Environment"

  echo "6) Exit"

  read -r -p "Your choice: " choice

  case "$choice" in
  1) run_docker ;;
  2) build_docker ;;
  3)
    while true; do
      display_header "Developer Menu"
      echo "Developer Menu:"
      echo "1) Run Local Dev"
      echo "2) Run Local DB"
      echo "3) Back to Main Menu"
      # Add more options here if needed

      read -r -p "Developer choice: " dev_choice
      case "$dev_choice" in
      1) run_local_dev ;;
      2) run_local_db ;;
      3) break ;;
      *) echo "🔴 Invalid choice. Please try again. 🔴" ;;
      esac
    done
    ;;
  4) clean_docker ;;
  5) [ ! -f "$LOCK_FILE" ] && init_environment || echo "Init is already running." ;;
  6)
    echo "👋 Exiting... See you next time in the AI universe! 👋"
    exit 0
    ;;
  *) echo "🔴 Invalid choice. Please try again. 🔴" ;;
  esac
done
```

#? But in the language "Go" and using the following modules and the TUI framework "PTerm" where i will send you all the files in a segment stream, please go ahead and process each time you receive that, the information about TUI and Pterm, and upgrade the "Go" Version of our "main.sh".:
# PTerm Documentation:
```````
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

```````



# Extra ################


Please update your complete code from your last response with the use of the next Documentation Page of PTerm below, as one copy-and-paste-ready response, and only that, no other comments that are not in the code, please.:
````````````




````````````

