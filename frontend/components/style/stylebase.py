from components.style.menu_lists import menu_list as import_menu_list

# This is the central Color collection for all the menu items. Of Steamlit, MaterialUI and most of the CSS classes.
# Check header.py, cssgen.py for more details.

menu_list = import_menu_list

button = {
    "Color": "#333",
    "Hover": "#555",
    "Active": "#111",
    "BoxShadow": "0px 1px 0px 0px rgba(255, 255, 255, 0.30) inset, 0px 3px 5px 0px rgba(0, 0, 0, 0.40)",
    "ActiveBoxShadow": "inset -4px -4px 8px rgba(255, 255, 255, 0.15), inset 4px 4px 8px rgba(25, 28, 30, 0.7)",
    "BoxShadowUp": "-6.22302px -6.22302px 18.6691px #3B4451, 6.22302px 6.22302px 18.6691px #000000",
    "BoxShadowDown": "inset -6.22302px -6.22302px 6.22302px #3B4451, inset 3.73381px 3.73381px 6.22302px #000000",
    "BGColor": "#eee",
    "HeaderTabs": "#666",
    "HeaderTabsHover": "#888",
    "HeaderTabsActive": "#444",
    "HeaderTabsBGColor": "#ddd",
    "Header": "#666",
    "HeaderHover": "#888",
    "HeaderActive": "#444",
    "HeaderBGColor": "#ddd",
    "HeaderIcon": "default",
    "HeaderIconHover": "secondary",
    "HeaderIconActive": "primary",
    "HeaderIconBGColor": "#ddd",
    "Sidebar": "#666",
    "SidebarHover": "#888",
    "SidebarActive": "#444",
    "SidebarBGColor": "#ddd",
    "Content": "#666",
    "ContentHover": "#888",
    "ContentActive": "#444",
    "ContentBGColor": "#ddd",
    "Prime": "#2196F3",
    "PrimeHover": "#64B5F6",
    "PrimeActive": "#0D47A1",
    "PrimeBGColor": "#BBDEFB",
    "Secondary": "#FFC107",
    "SecondaryHover": "#FFD54F",
    "SecondaryActive": "#FFA000",
    "SecondaryBGColor": "#FFECB3",
    "Green": "#4CAF50",
    "GreenHover": "#81C784",
    "GreenActive": "#2E7D32",
    "GreenBGColor": "#C8E6C9",
    "Red": "#F44336",
    "RedHover": "#E57373",
    "RedActive": "#B71C1C",
    "RedBGColor": "#FFCDD2",
    "Yellow": "#FFEB3B",
    "YellowHover": "#FFF176",
    "YellowActive": "#FBC02D",
    "YellowBGColor": "#FFF9C4",
    "Icons": "#757575",
    "IconsHover": "#BDBDBD",
    "IconsActive": "#424242",
    "IconsBGColor": "#E0E0E0",
}

container = {
    "Color": "#444",
    "Hover": "#666",
    "Active": "#222",
    "BoxShadow": "",
    "ActiveBoxShadow": "inset -4px -4px 8px rgba(255, 255, 255, 0.15), inset 4px 4px 8px rgba(25, 28, 30, 0.7)",
    "BGColor": "#fafafa",
    "Header": "#777",
    "HeaderHover": "#999",
    "HeaderActive": "#555",
    "HeaderBG": "linear-gradient(to bottom, #1e2a38, #0a111f)",
    "HeaderBGColor": "#1e2a38",
    "SubHeader": "#666",
    "SubHeaderHover": "#888",
    "SubHeaderActive": "#444",
    "SubHeaderBG": "linear-gradient(to bottom, #1e2a38, #1E2A38)",
    "SubHeaderBGColor": "#334155",
    "Sidebar": "#666",
    "SidebarHover": "#888",
    "SidebarActive": "#444",
    "SidebarBGColor": "linear-gradient(to bottom, #1e2a38, #0a111f)",
    "Content": "#777",
    "ContentHover": "#999",
    "ContentActive": "#555",
    "ContentBGColor": "#f0f0f0",
    "Prime": "#64B5F6",
    "PrimeHover": "#90CAF9",
    "PrimeActive": "#42A5F5",
    "PrimeBGColor": "#BBDEFB",
    "Secondary": "#FFD54F",
    "SecondaryHover": "#FFE082",
    "SecondaryActive": "#FFCA28",
    "SecondaryBGColor": "#FFECB3",
    "Green": "#81C784",
    "GreenHover": "#A5D6A7",
    "GreenActive": "#66BB6A",
    "GreenBGColor": "#C8E6C9",
    "Red": "#E57373",
    "RedHover": "#EF9A9A",
    "RedActive": "#E53935",
    "RedBGColor": "#FFCDD2",
    "Yellow": "#FFF176",
    "YellowHover": "#FFF59D",
    "YellowActive": "#FFEB3B",
    "YellowBGColor": "#FFF9C4",
    "Icons": "#BDBDBD",
    "IconsHover": "#E0E0E0",
    "IconsActive": "#8D8D8D",
    "IconsBGColor": "#ECECEC",
}

text = {
    "Default": "#D0D0D0D0",
    "Color": "#000",
    "Colorbg": "#FFF",
    "ColorHover": "#555",
    "ColorActive": "#111",
    "BGColor": "#EEE",
}


header_special = """
    box-shadow: -6.22302px -6.22302px 0.0 #1E2A38, 6.22302px 6.22302px 0.0 #000000;
    background: linear-gradient(to bottom, #1e2a38, #1E2A38);
"""


hover_filter = {
    "filter": "drop-shadow(3px 5px 2px rgb(0 0 0 / 0.4))",
    "hover_filter": "drop-shadow(3px 5px 2px rgb(255 255 255 / 0.2))",
}
