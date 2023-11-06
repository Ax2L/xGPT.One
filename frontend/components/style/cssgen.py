# components/style/cssgen.py

# ^ Importing required modules
import os
import streamlit as st
import time
import logging

# ^ Logging Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# & Rule class to generate individual CSS rules
class Rule:
    def __init__(
        self, selector, rule_type, properties, attribute=None, attribute_value=None
    ):
        self.selector = selector
        self.rule_type = rule_type
        self.properties = properties
        self.attribute = attribute
        self.attribute_value = attribute_value

    def __str__(self):
        properties_str = "\n".join(
            [f"    {k}: {v};" for k, v in self.properties.items()]
        )

        # Determine the rule type and return the corresponding CSS rule string
        rule_types = {
            "class": f".{self.selector}",
            "id": f"#{self.selector}",
            "attribute": f"{self.selector}[{self.attribute}='{self.attribute_value}']",
        }
        return (
            f"{rule_types.get(self.rule_type, self.selector)} {{\n{properties_str}\n}}"
        )


# & StyleSheet class to create and manage a collection of Rule objects
class StyleSheet:
    def __init__(self):
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def __str__(self):
        return "\n".join([str(rule) for rule in self.rules])

    def save_to_file(self, path, overwrite=True):
        if os.path.exists(path) and not overwrite:
            raise Exception("File already exists. To overwrite, set 'overwrite=True'")
        with open(path, "w") as f:
            f.write(str(self))


# ^ Define the CSS rules based on the provided styles
css_rules = [
    Rule(
        "header",
        "attribute",
        {"display": "none", "width": "0", "height": "0"},
        "data-testid",
        "stHeader",
    ),
    Rule("container", "class", {"width": "100%", "margin": "0 auto", "padding": "0"}),
    Rule(
        "header",
        "class",
        {
            "background-color": "#1e2a38",
            "height": "60px",
            "line-height": "60px",
            "color": "white",
            "text-align": "center",
            "font-size": "24px",
            "font-weight": "bold",
        },
    ),
    Rule("content", "class", {"padding": "20px", "background-color": "#0a111f"}),
    Rule(
        "footer",
        "class",
        {
            "background-color": "#1e2a38",
            "height": "40px",
            "line-height": "40px",
            "color": "white",
            "text-align": "center",
            "font-size": "14px",
        },
    ),
]

# * CUSTOM CSS BLOCK -----------------------------------------------------------
custom_css_block = """

/* 
#& Streamlit to deaktivate:
*/
div[data-testid="stSidebarNav"] {
    display: none;
    height: 0px;
    width: 0px;
}

header[data-testid="stHeader"] {
    display: none;
    height: 0px;
    width: 0px;
}

/* 
#& Unsorted
*/
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(to bottom, #1e2a38, #0a111f);
}

button {
    box-shadow: 0px 1px 0px 0px rgba(255, 255, 255, 0.30) inset, 0px 3px 5px 0px rgba(0, 0, 0, 0.40);
}

.MuiButtonBase-root {
    box-shadow: 0px 1px 0px 0px rgba(255, 255, 255, 0.30) inset, 0px 3px 5px 0px rgba(0, 0, 0, 0.40);
    min-height: min-content !important;
}

/* 
#& >- Header --> 
#todo|- Header frame -|
OLDsection[tabindex="0"] iframe:nth-of-type(1) {
    position: fixed;
    display: flex;
    justify-content: space-between;
    align-items: center;
    vertical-align: middle;
    margin-top: auto;
    margin-bottom: auto;
    padding-top: 0 !important;
    margin-left: -7px !important;
    margin-top: -7px !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    min-width: 101%;
    z-index: 100;
    background: #FFF;
}
*/

/* 
#& >- Header --> 
#todo|- Header frame -|*/
section[tabindex="0"] iframe:nth-of-type(1) {
    position: fixed !important;
    display: flex;
    justify-content: space-between;
    align-items: center;
    vertical-align: middle;
    margin-top: auto;
    margin-bottom: auto;
    padding-top: 0 !important;
    margin-left: -7px !important;
    margin-top: -7px !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    min-width: 101%;
    background-color: #334155;
    z-index: 0;
}

section[tabindex="0"] div:nth-of-type(1) {
    padding-left: 0px !important;
    padding-right: 0px !important;
    padding-top: 0px !important;
    margin-left: 0 !important;
    margin-right: 0 !important;
    margin-top: 0 !important;
    max-width: 101%;
}


/* #todo|- Header button -|*/
/* #todo|- Header Tabs -|*/
/* #todo|- Header IconButton -|*/
/* #todo|- Header UserMenu -|*/
/* #todo|- Header Breadcomb -|*/
/* #todo|- Header Searchbar -|*/
/* #todo|- Header Navibar -|*/
/* #todo|- Header Sidebar -|*/

/* 
#& >- Sidebar --> 
#todo|- Sidebar Container -|*/

/*
#todo|---------------------------|    Input    |----------------|
#*      SelectBox
*/
section[data-testid='stSidebar'] div[data-testid="stSelectbox"] {
    background-color: #000;
    color: #111878;
    border: 1;
    border-color: #000;
}

/*
#*      MultiSelectBox
*/
section[data-testid='stSidebar'] div[data-testid="stMultiSelect"] {
    background-color: #000;
    color: #111878;
    border: 1;
    border-color: #000;
}


/*
#^V.:|  InputLabelText
*/
section[data-testid='stSidebar'] div[data-testid="stTextInput"] {
    background-color: #000;
    color: #111878;
}


/*
#^V.:|  DropdownSelect
*/
section[data-testid='stSidebar'] div[data-baseweb="select"] {
    background-color: #666333;
}


/*
#*      TextBox
*/
section[data-testid='stSidebar'] div[data-testid="stTextInput"] {
    background-color: #000;
    color: #111878;
    border: 1;
    border-color: #000;
}

/*
#^V.:|  TextInput
*/
section[data-testid='stSidebar'] input[type="text"] {
    background-color: #666333;
}

/*
#todo|- Sidebar Button -|
#^V.:|  primary     
*/

section[data-testid='stSidebar'] button[kind="primary"] {
    background: #663333;
}

/*
#^V.:|  secondary  
*/
section[data-testid='stSidebar'] button[kind="secondary"] {
    background: #666333;
}

/*
#todo|- Sidebar Toggle -|
*/


section[data-testid='stSidebar'] {
    top: 61px !important;      
    button {
        top: 61px !important;
        background: #663333;
    }
}


/*
#& >- Content --> 
#todo|- Content Container -|
*/

/*
#todo|- Content Button -|
*/

/*
#todo|- Content Forms -|
*/

.tab-bar, .MuiTabs-root {
    display: flex;
    background: #252c3a;
    border-radius: 30px;
    width: 100%;
}
.tab, MuiTab-root {
    flex: 1;
    text-align: center;
    padding: 15px 0;
    transition: background 0.3s ease, color 0.3s ease, transform 0.3s ease;
    font-weight: 600;
    font-size: 16px;
    color: #bfbfbf;
    cursor: pointer;
    position: relative;
    overflow: hidden;
}
.tab:before, MuiTab-root:before {
    content: "";
    position: absolute;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    height: 100%;
    background: rgba(0, 123, 255, 0.4);
    opacity: 0;
    transition: opacity 0.3s ease;
}
.tab:hover:before, MuiTab-root:hover:before {
    opacity: 1;
}
.tab:hover, MuiTab-root:hover {
    background: #2a3241;
    color: #fff;
    transform: translateY(-3px);
}
.tab.active, MuiTab-root.active {
    background: #007BFF;
    color: #fff;
    transform: translateY(-3px);
}
.tab.active:before, MuiTab-root.active:before {
    opacity: 1;
}
.tab.active::before, MuiTab-root.active::before {
    content: "";
    position: absolute;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    height: 100%;
    background: rgba(0, 123, 255, 0.4);
}
"""
# * FUNCTIONS ------------------------------------------------------------------


# & Function to generate the CSS file
def generate_css_file():
    global stylesheet
    stylesheet = StyleSheet()  # Reset stylesheet every time function is called

    if os.path.exists("gen_css.lock"):
        logger.info("CSS generation is already in progress by another process.")
        return

    try:
        # Create lock file
        with open("gen_css.lock", "w") as lock:
            lock.write("CSS generation in progress")
            logger.info("Created gen_css.lock file.")

        # Generate CSS for each rule and save
        # for cssrule in css_rules:
        #    stylesheet.add_rule(cssrule)
        with open("style.css", "w") as css_file:
            # css_file.write(str(stylesheet))
            css_file.write(custom_css_block)  # Add the custom CSS block
        logger.info("Generated and saved CSS successfully.")

    except Exception as e:
        logger.error(f"Error generating CSS: {e}")
    finally:
        # Ensure lock file is always deleted
        if os.path.exists("gen_css.lock"):
            os.remove("gen_css.lock")
            logger.info("Removed gen_css.lock file.")


# & Function to apply the generated CSS to the Streamlit app
def apply_css_file(page_name=None):
    retry_count = 0
    # Wait if lock file exists
    while os.path.exists("gen_css.lock") and retry_count < 5:
        logger.info("Waiting for gen_css.lock to be deleted...")
        time.sleep(2)
        retry_count += 1

    if retry_count >= 5:
        logger.error("Failed to apply CSS due to gen_css.lock timeout.")
        return

    if not os.path.exists("style.css"):
        logger.error("style.css does not exist!")
        return

    with open("style.css", "r") as f:
        css_data = f.read()

    # Add CSS to Streamlit
    st.markdown(f"<style>{css_data}</style>", unsafe_allow_html=True)
    logger.info(f"Applied CSS for page: {page_name or 'Default'}")


# & MAIN EXECUTION -------------------------------------------------------------

if __name__ == "__main__":
    generate_css_file()
