# components/style/cssgen.py
# This Script will be used to generate style.css file before starting Streamlit, which will then be loaded into the app via Markdown html import.
# Check main.py and main.sh for more details.


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


# * CUSTOM CSS BLOCK -----------------------------------------------------------
custom_css_block = """

/* 
#& Streamlit to deaktivate:*/
/*#^Sidebar Default Page Navi */
div[data-testid="stSidebarNav"] {
    display: none;
    height: 0px;
    width: 0px;
}

/*#^Sidebar Root
section[data-testid="stSidebar"] {
    background: linear-gradient(to bottom, #1e2a38, #0a111f);
    top: 93px;
    box-shadow: -6.22302px -6.22302px 0.0 #1E2A38, 6.22302px 6.22302px 0.0 #000000;
}*/

section[data-testid="stSidebar"] {
    background: linear-gradient(to bottom, #1e2a38, #0a111f);
    box-shadow: -6.22302px -6.22302px 0.0 #1E2A38, 6.22302px 6.22302px 0.0 #000000;
    width: 244px;
}

/*#^Sidebar DevHeader */
header[data-testid="stHeader"] {
    display: none;
    height: 0px;
    width: 0px;
    border-radius: 90px;
}

/*#^Sidebar Open Button 
button[data-testid="baseButton-headerNoPadding"] {
    margin-top: 0px;
    margin-left: 0px;
    border-radius: 90px;
    height: 15px;
    background-color: #632D8F;
    color: #DFDFDFDF;


}*/

/*#!Sidebar Open Button #!TEST */
button[data-testid="baseButton-headerNoPadding"] {
    border-end-end-radius: Opx;
    border-radius: 4px;
    box-sizing: border-box;
    color: #DFDFDFDF;
    font-family: -apple-system, BlinkMacSystemFont,
    "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto
    Sans", sans-serif, "Apple Color Emoji", "Segoe UI
    Emoji", "Segoe UI Symbol", "Noto Color Emoji";
    font-size: 14px;
    inset-inline-end: -8px;
    line-height: 22px;
    list-style: none;
    margin: 0px;
    padding: 0px 10px;
    position: absolute;
    white-space: nowrap;
    :where(.css-lytssn) [class^="ant-ribbon"] [class^="ant-ribbon"]:: before
        box-sizing: border-box;
    :where (.css-lytssn) [class^="ant-ribbon"]::before
        box-sizing: border-box;
    left: 5px;
    background: linear-gradient(to left, #632D8F, #1E2A38);

}


/*#^Sidebar Close Button */
button[data-testid="baseButton-header"] {
    border-end-end-radius: Opx;
    border-radius: 4px;
    box-sizing: border-box;
    color: #DFDFDFDF;
    font-family: -apple-system, BlinkMacSystemFont,
    "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto
    Sans", sans-serif, "Apple Color Emoji", "Segoe UI
    Emoji", "Segoe UI Symbol", "Noto Color Emoji";
    font-size: 14px;
    inset-inline-end: -8px;
    line-height: 22px;
    list-style: none;
    margin: 0px;
    padding: 0px 8px;
    position: absolute;
    white-space:nowrap;
    :where(.css-lytssn) [class^="ant-ribbon"]
    [class^="ant-ribbon"]:: before
    box-sizing: border-box;
    :where (.css-lytssn) [class^="ant-ribbon"]::before
    box-sizing: border-box;
    top: 42px;
}


section[data-testid="stSidebar"] [title="streamlit_elements.core.render.streamlit_elements"] {
    background: transparent;

    min-height: 50px;

}

div[data-testid="stSidebarUserContent"] {
    padding: 0rem 0rem 4rem;
    

}


section[data-testid="stSidebar"] div:nth-of-type(2) {

}

/*#& Logo */
img {
    -webkit-filter: drop-shadow(5px 5px 5px #222);
    filter: drop-shadow(5px 5px 5px #222);
}



/* 
#& Unsorted
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(to bottom, #1e2a38, #0a111f);
}*/

button {
    box-shadow: 0px 1px 0px 0px rgba(255, 255, 255, 0.30) inset, 0px 3px 5px 0px rgba(0, 0, 0, 0.40);
}

button[type="button"] {
    box-shadow: 0px 1px 0px 0px rgba(255, 255, 255, 0.30) inset, 0px 3px 5px 0px rgba(0, 0, 0, 0.40);
}

.MuiButtonBase-root {
    box-shadow: 0px 1px 0px 0px rgba(255, 255, 255, 0.30) inset, 0px 3px 5px 0px rgba(0, 0, 0, 0.40);
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
    min-width: 102%;
    z-index: 100;
    background: #FFF;
}
*/

/* 
#& >- Header --> 
#todo|- Header frame -|
section[tabindex="0"] iframe:nth-of-type(1) {
    position: fixed;
    display: flex;
    justify-content: space-between;
    align-items: left;
    vertical-align: middle;
    margin: 0;
    padding: 10;
    margin-top: 0;
    margin-bottom: auto;
    margin-left: auto;
    margin-right: auto;
    padding-top: 0 !important;
    top: -7px !important;
    left: -7px !important;
    right: 0 !important;
    min-width: 102%;
    z-index: 100;
    background: linear-gradient(to bottom, #1e2a38, #0a111f) !important;
}*/

/*
iframe[title="streamlit_elements.core.render.streamlit_elements"] {
    position: relative;
    display: flex;
    justify-content: space-between;
    align-items: left;
    vertical-align: middle;
    margin: 0;
    padding: 10;
    margin-top: 0;
    margin-bottom: auto;
    margin-left: auto;
    margin-right: auto;
    padding-top: 0 !important;
    top: -7px !important;
    left: -7px !important;
    right: 0 !important;
    min-width: 102%;
    z-index: 100;
    background: linear-gradient(to bottom, #1e2a38, #0a111f) !important;
    body {
        margin: 0 !important;
    }
}*/

/*
section[data-testid="stSidebar"] [title="streamlit_elements.core.render.streamlit_elements"] {
    display: flex;
    justify-content: space-between;
    align-items: left;
    vertical-align: middle;
    margin: 0;
    padding: 10;
    margin-top: 0;
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    opacity: 0;
    visibility: hidden;
    padding-top: 0 !important;
    top: -7px !important;
    left: -7px !important;
    right: 0 !important;
    min-width: 270px;
    z-index: 100;
    background: linear-gradient(to bottom, #1e2a38, #0a111f) !important;
    body {
        margin: 0 !important;
    }
}*/


section[tabindex="0"] [data-testid="block-container"] {
    
    padding: 0;
    padding-top: 0 ;
    padding-left: 1rem ;
    padding-right: 1rem ;
    
}

section[tabindex="0"] iframe:nth-of-type(1) body:nth-of-type(1) {
    margin: 0;
}

body[data-gr-ext-disabled="forever"] {
    margin: 0 !important;
}



/* Should be only for Header 
section[tabindex="0"] div:nth-of-type(1) {
    padding-left: 0px !important;
    padding-right: 0px !important;
    padding-top: 0px !important;
    margin-left: 0 !important;
    margin-right: 0 !important;
    margin-top: 0 !important;
    max-width: 101%;
}
*/

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
    box-shadow: 0px 1px 0px 0px rgba(255, 255, 255, 0.30) inset, 0px 3px 5px 0px rgba(0, 0, 0, 0.40);
}

/*
#*      MultiSelectBox
*/
section[data-testid='stSidebar'] div[data-testid="stMultiSelect"] {
    background-color: #000;
    color: #111878;
    border: 1;
    border-color: #000;
    box-shadow: 0px 1px 0px 0px rgba(255, 255, 255, 0.30) inset, 0px 3px 5px 0px rgba(0, 0, 0, 0.40);
}


/*
#^V.:|  InputLabelText
*/
section[data-testid='stSidebar'] div[data-testid="stWidgetLabel"] {
    background-color: #000;
    color: #111878;
    box-shadow: 0px 1px 0px 0px rgba(255, 255, 255, 0.30) inset, 0px 3px 5px 0px rgba(0, 0, 0, 0.40);
}


/*
#^V.:|  DropdownSelect
*/
section[data-testid='stSidebar'] div[data-baseweb="select"] {
    background-color: #666333;
    box-shadow: 0px 1px 0px 0px rgba(255, 255, 255, 0.30) inset, 0px 3px 5px 0px rgba(0, 0, 0, 0.40);
}


/*
#*      TextBox
*/
section[data-testid='stSidebar'] div[data-testid="stTextInput"] {
    background-color: #000;
    color: #111878;
    border: 1;
    border-color: #000;
    box-shadow: 0px 1px 0px 0px rgba(255, 255, 255, 0.30) inset, 0px 3px 5px 0px rgba(0, 0, 0, 0.40);
}

/*
#^V.:|  TextInput
*/
section[data-testid='stSidebar'] input[type="text"] {
    background-color: #666333;
    box-shadow: 0px 1px 0px 0px rgba(255, 255, 255, 0.30) inset, 0px 3px 5px 0px rgba(0, 0, 0, 0.40);
}

/*
#todo|- Sidebar Button -|
#^V.:|  primary     
*/

section[data-testid='stSidebar'] button[kind="primary"] {
    background: #663333;
    box-shadow: 0px 1px 0px 0px rgba(255, 255, 255, 0.30) inset, 0px 3px 5px 0px rgba(0, 0, 0, 0.40);
}

/*
#^V.:|  secondary  
*/
section[data-testid='stSidebar'] button[kind="secondary"] {
    background: #666333;
    box-shadow: 0px 1px 0px 0px rgba(255, 255, 255, 0.30) inset, 0px 3px 5px 0px rgba(0, 0, 0, 0.40);
}

/*
#todo|- Sidebar Toggle -|
*/


section[data-testid='stSidebar'] {
    border: 1px;
    background-color: transparent!;
    button {
        top: 5px;
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
.tab, .MuiTab-root {
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
    box-shadow: 0px 1px 0px 0px rgba(255, 255, 255, 0.30) inset, 0px 3px 5px 0px rgba(0, 0, 0, 0.40);
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
