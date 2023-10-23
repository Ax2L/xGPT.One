import requests
from pathlib import Path
import random
import streamlit as st
import numpy as np
from PIL import Image, ImageOps

from components.utils import colorHelper



# colorHelper.local_css("local_styles.css")

# Init state. This is only run whenever a new session starts (i.e. each time a new
# browser tab is opened).
if not st.session_state:
    st.session_state.primaryColor = "#7792E3"
    st.session_state.backgroundColor = "#1C1B1F"
    st.session_state.secondaryBackgroundColor = "#1A202C"
    st.session_state.textColor = "#FFFFFF"
    st.session_state.is_dark_theme = True
    st.session_state.first_time = True

# # Show header.
# header_img = st.empty()
# header_img.image(
#     "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/271/woman-artist_1f469-200d-1f3a8.png",
#     width=100,
# )
# 
# header_text = st.empty()
# header_text.write(
#     """
#     # Streamlit Theme Generator
# 
#     Generate beautiful color themes for Streamlit, powered by [colormind.io](http://colormind.io/bootstrap/).
#     Scroll down to see the theme in action 🎈
#     """
# )
# 
# ""

col1, col2 = st.beta_columns([0.35, 0.65])
new_theme_clicked = col1.button("🔄 Generate new theme")
theme_type = col2.radio("", ["Light theme", "Dark theme"])
# spinner = st.empty()
# if not state.first_time:
#     ""
#     "Done! Scroll down to see your new theme 🎈 "
# TODO: Use a checkbox here instead. Doesn't work with current wheel file.
# dark_checked = st.checkbox("Use dark themes")  # "Black is beautiful" or "Make it dark"

"---"

quote = st.beta_container()

# Show current theme colors.
locked = []
columns = st.beta_columns(4)
labels = ["backgroundColor", "secondaryBackgroundColor", "primaryColor", "textColor"]
for column, label in zip(columns, labels):
    # c = column.color_picker(
    #     label.rstrip("Color").replace("B", " b").capitalize(),
    #     state[label],
    #     key="color_picker" + label,
    # )
    # st.write(c)
    # st.text_input("c", state[label], key="test" + label)
    img = Image.new("RGB", (100, 50), st.session_state[label])
    img = ImageOps.expand(img, border=1, fill="black")
    column.image(img, width=150)
    column.markdown(
        f"<small>{label.rstrip('Color').replace('B', ' b').capitalize()}</small>",
        unsafe_allow_html=True,
    )
    # TODO: Do this with st.checkbox, but doesn't return the proper value with current wheel.
    lock_value = column.radio("", ["Locked", "Unlocked"], index=1, key="lock-" + label)
    locked.append(lock_value == "Locked")
    # TODO: Show colorpicker above instead of images.


def apply_theme_from_session_state():
    """Retrieve theme from session state and apply it to streamlit config."""
    # Only apply if theme in state differs from the current config. This is important
    # to not trigger rerun repeatedly.
    if st.config.get_option("theme.primaryColor") != st.session_state.primaryColor:
        st.config.set_option("theme.primaryColor", st.session_state.primaryColor)
        st.config.set_option("theme.backgroundColor", st.session_state.backgroundColor)
        st.config.set_option(
            "theme.secondaryBackgroundColor", st.session_state.secondaryBackgroundColor
        )
        st.config.set_option("theme.textColor", st.session_state.textColor)

        # Trigger manual rerun (required to actually apply the theme to the app).
        st.experimental_rerun()


def generate_new_theme():
    """Retrieve new theme from colormind, store in state, and apply to app."""
    if any(locked):
        # Generate only new colors for the colors that are not locked. These need to be
        # represented as "N" in the list below. Locked colors need to be represented by
        # their RGB values, e.g. [123, 123, 123].
        input_list = ["N", "N", "N", "N", "N"]
        # TODO: Refactor this.
        if locked[0]:
            if st.session_state.is_dark_theme:
                input_list[4] = colorHelper.hex2rgb(st.session_state.backgroundColor)
            else:
                input_list[0] = colorHelper.hex2rgb(st.session_state.backgroundColor)
        if locked[1]:
            if st.session_state.is_dark_theme:
                input_list[3] = colorHelper.hex2rgb(st.session_state.secondaryBackgroundColor)
            else:
                input_list[1] = colorHelper.hex2rgb(st.session_state.secondaryBackgroundColor)
        if locked[2]:
            input_list[2] = colorHelper.hex2rgb(st.session_state.primaryColor)
        if locked[3]:
            if st.session_state.is_dark_theme:
                input_list[0] = colorHelper.hex2rgb(st.session_state.textColor)
            else:
                input_list[4] = colorHelper.hex2rgb(st.session_state.textColor)
        res = requests.get(
            "http://colormind.io/api/", json={"input": input_list, "model": "ui"}
        )
    else:
        # Generate new colors for all colors.
        res = requests.get("http://colormind.io/api/", json={"model": "ui"})

    # Retrieve results from colormind.io and convert to hex.
    rgb_colors = res.json()["result"]
    hex_colors = [colorHelper.rgb2hex(*rgb) for rgb in res.json()["result"]]

    # TODO: Refactor this with the stuff above.
    # Store colors in session state. This is required so that separate tabs/users can
    # have different themes. If we would apply the theme directly to `st.config`,
    # every user would see the same theme!
    if theme_type == "Light theme":
        st.session_state.primaryColor = hex_colors[2]
        st.session_state.backgroundColor = hex_colors[0]
        st.session_state.secondaryBackgroundColor = hex_colors[1]
        st.session_state.textColor = hex_colors[4]
        st.session_state.is_dark_theme = False
    else:
        st.session_state.primaryColor = hex_colors[2]
        st.session_state.backgroundColor = hex_colors[4]
        st.session_state.secondaryBackgroundColor = hex_colors[3]
        st.session_state.textColor = hex_colors[0]
        st.session_state.is_dark_theme = True


""


if new_theme_clicked:
    if st.session_state.first_time:
        # Show some 🎈 🎈 the first time the user creates a new theme ;)
        st.balloons()
        st.session_state.first_time = False
    wait_texts = [
        "🎨 Mixing colors...",
        "🌈 Collecting rainbows...",
        "🖌️ Painting...",
        "🐿️ Making happy little accidents...",
        "🌲 Decision time...",
        "☀️ Lighting up...",
    ]
    # spinner.info(random.choice(wait_texts))
    generate_new_theme()

# TODO: Try to do everything after this call, because this triggers a re-run.
apply_theme_from_session_state()


# st.write("---")
""

"""
To use this theme in your app, just create a file *.streamlit/config.toml* in your app's 
root directory and add the following code:
"""

config = colorHelper.CONFIG_TEMPLATE.format(
    st.session_state.primaryColor,
    st.session_state.backgroundColor,
    st.session_state.secondaryBackgroundColor,
    st.session_state.textColor,
)
st.code(config)

mode = st.radio("App mode", ["Normal", "Cute 🐿️"], key="mode")
# if mode == "Cute 🐿️":
#     # header_img.image(
#     #     "https://images0.gerstaecker.de/out/pictures/generated/1500_1500/pboxx-pixelboxx-47382/BOB+ROSS%C2%AE+Soft-%C3%96lfarben+%E2%80%93+Tiere.jpg",
#     #     width=100,
#     # )
#     # header_text.write(
#         """
#         # The Joy of Streamlitting
# 
#         Welcome back,
# 
#         today we want to bring some color to this little Streamlit app. Everything you need 
#         is your mouse to hit the button below. Let's start, and whatever you do, always remember:
#         There are no mistakes – only happy little accidents! 🐿️
# 
#         And with that, I wish you happy streamlitting, and god bless my friend.
#         """
#     )
#     st.write("And now scroll up ☝️")

#    bob_quotes = [
#        '🌈 *"If we all painted the same way, what a boring world it would be."*',
#        '☀️ *"...that may be the true joy of painting, when you share it with other people. I really believe that\'s the true joy."*',
#        '🌲 *"Friends are the most important commodity in the world. Even a tree needs a friend."*',
#        '🌚 *"We put some dark in, only so our light will show. You have to have dark in order to show the light."*',
#        '👩‍🎨️ *"There\'s an artist hidden at the bottom of every single one of us."*',
#        '☁️ *"Let\'s make some nice little clouds that just float around and have fun all day."*',
#        '🖌️ *"Every day is a good day when you paint."*',
#        '🦄 *"However you think it should be, that\'s exactly how it should be."*',
#        '🕊️ *"I aspire to create tranquility, a peaceful atmosphere to take people away form their everyday problems and frustrations."*',
#        '👣 *"You\'ll never believe what you can do until you get in there and try it."*',
#    ]
#    block_methods = [st.error, st.warning, st.info, st.success]
#    with quote:
#        random.choice(block_methods)(random.choice(bob_quotes))
#        st.write("")


st.write("---")


# Draw some dummy content in main page and sidebar.
def draw_all(
    key,
    plot=False,
):
    st.write(
        """
        ## Example Widgets
        
        These widgets don't do anything. But look at all the new colors they got 👀 
    
        ```python
        # First some code.
        streamlit = "cool"
        theming = "fantastic"
        both = "💥"
        ```
        """
    )

    st.checkbox("Is this cool or what?", key=key + "check")
    st.radio(
        "How many balloons?",
        ["1 balloon 🎈", "2 balloons 🎈🎈", "3 balloons 🎈🎈🎈"],
        key=key + "radio",
    )
    st.button("🤡 Click me", key=key + "button")

    #// if plot:
    #//     st.write("Oh look, a plot:")
    #//     x1 = np.random.randn(200) - 2
    #//     x2 = np.random.randn(200)
    #//     x3 = np.random.randn(200) + 2
    
    #//     hist_data = [x1, x2, x3]
    #//     group_labels = ["Group 1", "Group 2", "Group 3"]
    #//     fig = ff.create_distplot(hist_data, group_labels, bin_size=[0.1, 0.25, 0.5])
    #//     st.plotly_chart(fig, use_container_width=True)
    #// st.file_uploader("You can now upload with style", key=key + "file_uploader")
    st.slider(
        "From 10 to 11, how cool are themes?",
        min_value=10,
        max_value=11,
        key=key + "slider",
    )
    # st.select_slider("Pick a number", [1, 2, 3], key=key)
    st.number_input("So many numbers", key=key + "number")
    # st.text_area("A little writing space for you :)", key=key + "text")
    st.selectbox(
        "My favorite thing in the world is...",
        ["Streamlit", "Theming", "Baloooons 🎈 "],
        key=key + "select",
    )
    # st.multiselect("Pick a number", [1, 2, 3], key=key)
    # st.color_picker("Colors, colors, colors", key=key)
    with st.beta_expander("Expand me!"):
        st.write("Hey there! Nothing to see here 👀 ")
    st.write("")
    # st.write("That's our progress on theming:")
    # st.progress(0.99)
    if plot:
        st.write("And here's some data and plots")
        st.json({"data": [1, 2, 3, 4]})
        st.dataframe({"data": [1, 2, 3, 4]})
        st.table({"data": [1, 2, 3, 4]})
        st.line_chart({"data": [1, 2, 3, 4]})
        # st.help(st.write)
    st.write("This is the end. Have fun building themes!")


draw_all("main", plot=True)

with st.sidebar:
    draw_all("sidebar")