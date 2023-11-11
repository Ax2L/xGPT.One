import re


def extract_and_save_css(html_file_path):
    # Read the HTML file
    with open(html_file_path, "r") as file:
        html_content = file.read()

    # Find all CSS inside <style> tags
    css = "\n".join(re.findall(r"<style[^>]*>(.*?)<\/style>", html_content, re.DOTALL))

    # Write the CSS to a new file
    css_file_path = html_file_path.replace(".html", ".css")
    with open(css_file_path, "w") as file:
        file.write(css)

    # Remove the CSS from the HTML content
    updated_html = re.sub(
        r"<style[^>]*>.*?<\/style>", "", html_content, flags=re.DOTALL
    )

    # Write the updated HTML to a new file
    updated_html_file_path = html_file_path.replace(".html", "_updated.html")
    with open(updated_html_file_path, "w") as file:
        file.write(updated_html)

    return css_file_path, updated_html_file_path


# Example usage
css_file, updated_html_file = extract_and_save_css("helper/css/test/test.html")
print(f"CSS saved to: {css_file}")
print(f"Updated HTML saved to: {updated_html_file}")
