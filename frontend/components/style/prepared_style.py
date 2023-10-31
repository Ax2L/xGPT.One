import os
import streamlit as st
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simple CSS Generator
class Rule:
    def __init__(self, selector, rule_type, properties, attribute=None, attribute_value=None):
        self.selector = selector
        self.rule_type = rule_type
        self.properties = properties
        self.attribute = attribute
        self.attribute_value = attribute_value

    def __str__(self):
        properties_str = "\n".join([f"    {k}: {v};" for k, v in self.properties.items()])
        
        if self.rule_type == 'class':
            return f".{self.selector} {{\n{properties_str}\n}}"
        elif self.rule_type == 'id':
            return f"#{self.selector} {{\n{properties_str}\n}}"
        elif self.rule_type == 'attribute':
            return f"{self.selector}[{self.attribute}='{self.attribute_value}'] {{\n{properties_str}\n}}"
        else:
            return f"{self.selector} {{\n{properties_str}\n}}"


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
        with open(path, 'w') as f:
            f.write(str(self))


# Define rules and styles
container = Rule(
    selector='container',
    rule_type='class',
    properties={
        'position': 'relative',
        'width': '100%'
    }
)

button_secondary_st_submit = Rule(
    selector='button',
    rule_type='attribute',
    attribute='kind',
    attribute_value='secondaryFormSubmit',
    properties={
        'position': 'relative !important',
        'width': '100% !important',
        'background': '#FFF !important',
        'color': '#FF0000 !important',

    }
)
button_secondary_st = Rule(
    selector='button',
    rule_type='attribute',
    attribute='kind',
    attribute_value='secondary',
    properties={
        'position': 'relative !important',
        'width': '100% !important',
        'background': '#FFF !important',
        'color': '#FF0000 !important',

    },
)

css_rules = [button_secondary_st, container, button_secondary_st]

stylesheet = StyleSheet()

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
        stylesheet.save_to_file('style.css', overwrite=True)  # Overwrite set to True to ensure file is updated
        logger.info("Generated and saved CSS successfully.")

    except Exception as e:
        logger.error(f"Error generating CSS: {e}")
    finally:
        # Ensure lock file is always deleted
        if os.path.exists("gen_css.lock"):
            os.remove("gen_css.lock")
            logger.info("Removed gen_css.lock file.")


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


# Ensure styles are loaded into session state
#if "style_settings" in st.session_state:
#    generate_css_file()
#    apply_css_file()


if __name__ == "__main__":
    generate_css_file()