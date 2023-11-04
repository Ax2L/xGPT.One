import re
from selenium import webdriver
import chromedriver_autoinstaller

def extract_streamlit_components(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        matches = re.findall(r'\bst\.\w+', content)
    return list(set(matches))

def filter_components(components_list):
    unwanted = ['st.write', 'st.set_option','st.session_state']  # Add any other unwanted components to this list
    return [comp for comp in components_list if comp not in unwanted]

def extract_html_for_components(components_list, url="http://localhost:8501"):
    # Automatically download and install ChromeDriver
    chromedriver_autoinstaller.install()

    browser = webdriver.Chrome()  # Using Chrome; you can use Firefox or others
    browser.get(url)

    component_html_snippets = {}

    for component in components_list:
        component_name = component.split('.')[-1]  # Extracting the name after 'st.'
        
        # Now using data-testid attribute for finding the element
        try:
            element = browser.find_element_by_xpath(f"div[data-testid='{component_name}']")
            component_html_snippets[component] = element.get_attribute('outerHTML')
        except:
            component_html_snippets[component] = "Not Found"

    browser.quit()

    return component_html_snippets

if __name__ == "__main__":
    file_path = input("Enter the filepath of your Streamlit script: ")
    components = extract_streamlit_components(file_path)
    filtered_components = filter_components(components)
    html_snippets = extract_html_for_components(filtered_components)

    for component, snippet in html_snippets.items():
        print(f"{component}:\n{snippet}\n\n")
