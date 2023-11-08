import json
import colorsys


def generate_css(base_color):
    # Convert hex to RGB
    base_color = base_color.lstrip("#")
    r, g, b = tuple(int(base_color[i : i + 2], 16) for i in (0, 2, 4))

    # Convert RGB to HLS
    h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)

    # Adjusting the lightness for dark mode: darker background, lighter text
    dark_mode_l = max(0, l * 0.2)  # Darken more for background
    light_text_l = min(1, l * 1.8 if l * 1.8 < 1 else 1)  # Lighten for text

    # Convert HLS back to RGB for dark mode background
    dark_mode_rgb = colorsys.hls_to_rgb(h, dark_mode_l, s)

    # Convert HLS back to RGB for light text
    light_text_rgb = colorsys.hls_to_rgb(h, light_text_l, s)

    # Convert RGB back to HEX
    background_color = "#%02x%02x%02x" % tuple(int(x * 255) for x in dark_mode_rgb)
    text_color = "#%02x%02x%02x" % tuple(int(x * 255) for x in light_text_rgb)

    # Preparing the dark mode CSS
    css = {
        "BackgroundColor": background_color,
        "TextColor": text_color,
        "BorderColor": text_color,
        "HoverBackgroundColor": "#" + base_color,  # Base color for hover
        "HoverTextColor": text_color,
        "ActiveBackgroundColor": background_color,
        "ActiveTextColor": "#FFFFFF",  # White for active text
        "BoxShadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2)",
        "ActiveBoxShadow": "inset 0 2px 4px 0 rgba(255, 255, 255, 0.2)",
    }

    return css


def save_css_to_json(color_list, file_name):
    css_blocks = {}

    for name, color in color_list:
        css_blocks[name] = generate_css(color)

    with open(file_name, "w") as json_file:
        json.dump(css_blocks, json_file, indent=4)


# Example usage with a list of color names and their corresponding base colors
color_list = [
    ("Menu0", "#EEA981"),
    ("Menu1", "#AA6769"),
    ("Menu2", "#8F6F80"),
    ("Menu3", "#B09288"),
    ("Menu4", "#83B5B7"),
    ("Menu5", "#D0708E"),
    ("Menu6", "#556F84"),
    ("Menu7", "#A5C2DB"),
    ("Menu8", "#9C5AA0"),
    ("Menu9", "#49648D"),
]

color_list_v1 = [
    ("Menu0", "#866EBB"),
    ("Menu1", "#765081"),
    ("Menu2", "#234783"),
    ("Menu3", "#81BE9E"),
    ("Menu4", "#4C5353"),
    ("Menu5", "#EF7E3F"),
    ("Menu6", "#FED673"),
    ("Menu7", "#A5C2DB"),
    ("Menu8", "#1C223B"),
    ("Menu9", "#090F11"),
]

# Save to a JSON file
save_css_to_json(color_list, "menu_colors.json")
