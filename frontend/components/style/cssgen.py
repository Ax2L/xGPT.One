# components/style/cssgen.py

# ? Importing required modules
import os
import streamlit as st
import time
import logging
import json

# * Logging Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# & CLASS DEFINITIONS ----------------------------------------------------------
with open("components/style/base.json", "r") as file:
    data = json.load(file)
# ^ Store "Base" values for CSS
base_colors = data["base_colors"]
typography = data["typography"]
layout = data["layout"]
headers = data["headers"]
sidebar = data["sidebar"]
inputs = data["inputs"]
logo = data["logo"]
submenu = data["submenu"]
buttons = data["buttons"]
containers = data["containers"]
unsorted = data["unsorted"]
header_frame = data["header_frame"]
base_body = data["body"]
# ? Rule class to generate individual CSS rules
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
        if self.rule_type == "class":
            return f".{self.selector} {{\n{properties_str}\n}}"
        elif self.rule_type == "id":
            return f"#{self.selector} {{\n{properties_str}\n}}"
        elif self.rule_type == "attribute":
            return f"{self.selector}[{self.attribute}='{self.attribute_value}'] {{\n{properties_str}\n}}"
        else:
            return f"{self.selector} {{\n{properties_str}\n}}"


# ? StyleSheet class to create and manage a collection of Rule objects
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


# & CSS RULE DEFINITIONS -------------------------------------------------------
# Example:
# container = Rule(
#     selector="container",
#     rule_type="class",
#     properties={"position": "relative", "width": "100%"}
# )
#
# button_secondary_st_submit = Rule(
#     selector="button",
#     rule_type="attribute",
#     attribute="kind",
#     attribute_value="secondaryFormSubmit",
#     properties={
#         "position": "relative !important",
#         "width": "100% !important",
#         "background": "#000 !important",
#         "color": "#FF0000 !important"
#     }
# )

# ? Define the CSS rules
# ^ Remove Streamlit stuff
stheader = Rule(
    selector="header",
    rule_type="attribute",
    attribute="data-testid",
    attribute_value="stHeader",
    properties={
        "display": "none",
        "width": "0",
        "height": "0",
    },
)

# ^ Header


# ^ Sidebar
sidebar = Rule(
    selector="section",
    rule_type="attribute",
    attribute="data-testid",
    attribute_value="stSidebar",
    properties={
        "background": header_frame["background_color"],
        "color": sidebar["button_color"],
    },
)

# ^ Button
button_secondary_st = Rule(
    selector="button",
    rule_type="attribute",
    attribute="kind",
    attribute_value="secondary",
    properties={
        "display": buttons["display"],
        "padding": buttons["padding"],
        "border": buttons["border"],
        "cursor": buttons["cursor"],
        "transition": buttons["transition"],
        "color": buttons["color"],
        "background": buttons["bg"],
        "box-shadow": buttons["box_shadow"],
        "filter": buttons["filter"],
        "border-radius": buttons["border_radius"],
    },
)

button_secondary_st_submit = Rule(
    selector="button",
    rule_type="attribute",
    attribute="kind",
    attribute_value="secondaryFormSubmit",
    properties={
        "position": "relative !important",
        "width": "100% !important",
        "background": "#000 !important",
        "color": "#FF0000 !important",
    },
)

# ^ Tabs


# ^ Expander

# ^ More...


# * Add rules to the stylesheet
css_rules = [stheader, button_secondary_st, button_secondary_st_submit, sidebar]

stylesheet = StyleSheet()

# & CUSTOM CSS BLOCK -----------------------------------------------------------
custom_css_block = """
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(to bottom, #1e2a38, #0a111f);
    margin: 0;
    padding: 50px;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}
div[data-testid="stSidebarNav"] {
    display: none;
    height: 0px;
    width: 0px;
}

section[data-testid='stSidebar'] {
    top: 61px !important;
}
section[tabindex="0"] dsdiv[data-testid="block-container"] {
    padding-left: 0px !important;
    padding-right: 0px !important;
    padding-top: 0px !important;
    margin-left: 0 !important;
    margin-right: 0 !important;
    margin-top: 0 !important;

}

button {
    "box-shadow": "0px 1px 0px 0px rgba(255, 255, 255, 0.30) inset, 0px 3px 5px 0px rgba(0, 0, 0, 0.40)",
}

.MuiButtonBase-root {
    "box-shadow": "0px 1px 0px 0px rgba(255, 255, 255, 0.30) inset, 0px 3px 5px 0px rgba(0, 0, 0, 0.40)",
    "min-height": "min-content !important";
}

section[tabindex="0"] iframe:nth-of-type(1) {
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
    background: linear-gradient(to bottom, #1e2a38, #0a111f);
}
section[tabindex="0"] iframe:nth-of-type(1) header:nth-of-type(1) {
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
}
"""

# & FUNCTIONS ------------------------------------------------------------------


# ? Function to generate the CSS file
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
        for cssrule in css_rules:
            stylesheet.add_rule(cssrule)
        with open("style.css", "w") as css_file:
            css_file.write(str(stylesheet))
            css_file.write(custom_css_block)  # Add the custom CSS block
        logger.info("Generated and saved CSS successfully.")

    except Exception as e:
        logger.error(f"Error generating CSS: {e}")
    finally:
        # Ensure lock file is always deleted
        if os.path.exists("gen_css.lock"):
            os.remove("gen_css.lock")
            logger.info("Removed gen_css.lock file.")


# ? Function to apply the generated CSS to the Streamlit app
def apply_css_file(page_name=None):
    retry_count = 0
    # Wait if lock file exists
    while os.path.exists("gen_css.lock") and retry_count < 5:
        logger.info("CSS generation in progress. Waiting to apply CSS...")
        time.sleep(1)
        retry_count += 1
    if not os.path.exists("gen_css.lock"):
        try:
            if os.path.exists("style.css"):
                with open("style.css", "r") as css_file:
                    custom_css = css_file.read()
                    st.markdown(f"<style>{custom_css}</style>", unsafe_allow_html=True)
                    logger.info("CSS applied to Streamlit app.")
                    return
            else:
                raise FileNotFoundError("style.css not found.")
        except Exception as e:
            logger.error(f"Error applying CSS: {e}")
            st.error(f"Failed to apply CSS: {e}")
    else:
        msg = "Failed to apply CSS because CSS generation is currently in progress."
        logger.error(msg)
        st.error(msg)


# & MAIN EXECUTION -------------------------------------------------------------

if __name__ == "__main__":
    generate_css_file()
