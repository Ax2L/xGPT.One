# home.py

import streamlit as st
import streamlit_authenticator as stauth
from streamlit_elements import elements, mui, html
from components.default import sidebar_header_menu
from components.utils.styles import apply_page_settings, apply_styles
from  components.utils.auth_utils import load_config, save_config, send_reset_password_email, send_forgot_username_email
import os

# Initialize Session State
def initialize_session_state():
    st.session_state.setdefault("authentication_status", None)
    st.session_state.setdefault("openai_key", "")
    st.session_state.setdefault("name", "")
initialize_session_state()

# Settings and Styles
apply_page_settings("Home")
# apply_styles() # unstable

# Load Config
config = load_config()

# Initialize Authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

#// region [ rgba(250, 15, 100, 0.05)] Sidebar Initialization
# Sidebar
sidebar_header_menu(authenticator)
#// endregion


# Authenticated Display
def authenticated_display():
    st.header('Home')
    
    with st.container():
        # Home-related Code
        user_name = st.session_state['username']
        st.subheader(f'Welcome {user_name}', divider='gray')    
        col1, col2 = st.columns([1, 1])
        #
        # Column 1
        with col1:
            #TODO Completed: Create a container for the object below.
            with st.expander("User Details 🛈", expanded=True):
                st.write(f"**👤 Username: {st.session_state['username']}**")
                st.write(f"**📛 Name: {st.session_state['name']}**")
                st.write(f"**📧 Email: youremail@example.com**")  # Replace with real email

        # Column 2
        with col2:
            tab1, tab2, tab3 = st.tabs(["Password", "User", "API Keys"])

            # Password Tab
            with tab1:
                # Moved from old version
                with st.spinner('Processing...'):
                    try:
                        if authenticator.reset_password(st.session_state["username"], 'Reset Password 🔄'):
                            st.success('Password modified successfully ✅')
                    except Exception as e:
                        st.error(f"Error: {str(e)} ❌")

            # User Tab
            with tab2:
                # Moved from old version
                with st.spinner('Processing...'):
                    try:
                        if authenticator.update_user_details(st.session_state["username"], 'Update User Details 🔄'):
                            st.success('Entries updated successfully ✅')
                    except Exception as e:
                        st.error(f"Error: {str(e)} ❌")
            
            # API Keys Tab
            with tab3:
                # Moved from old version
                with st.spinner('Processing...'):
                    try:
                        st.subheader("Update your OpenAI Key 🔐")
                        new_key = st.text_input("Your OpenAI API Key", value=st.session_state.openai_key, type="password")
                        if st.button("Update Key"):
                            with st.spinner('Updating OpenAI Key...'):
                                st.session_state.openai_key = new_key
                                st.success("API Key Updated Successfully ✅")
                    except Exception as e:
                        st.error(f"Error: {str(e)} ❌")
                        
    with elements("new_element"):
        # Let's create a Typography element with "Hello world" as children.
        # The first step is to check Typography's documentation on MUI:
        # https://mui.com/components/typography/
        #
        # Here is how you would write it in React JSX:
        #
        # <Typography>
        #   Hello world
        # </Typography>
        mui.Typography("Hello world")

    with elements("multiple_children"):

        # You have access to Material UI icons using: mui.icon.IconNameHere
        #
        # Multiple children can be added in a single element.
        #
        # <Button>
        #   <EmojiPeople />
        #   <DoubleArrow />
        #   Hello world
        # </Button>

        mui.Button(
            mui.icon.EmojiPeople,
            mui.icon.DoubleArrow,
            "Button with multiple children"
        )

        # You can also add children to an element using a 'with' statement.
        #
        # <Button>
        #   <EmojiPeople />
        #   <DoubleArrow />
        #   <Typography>
        #     Hello world
        #   </Typography>
        # </Button>

        with mui.Button:
            mui.icon.EmojiPeople()
            mui.icon.DoubleArrow()
            mui.Typography("Button with multiple children")

    with elements("nested_children"):

        # You can nest children using multiple 'with' statements.
        #
        # <Paper>
        #   <Typography>
        #     <p>Hello world</p>
        #     <p>Goodbye world</p>
        #   </Typography>
        # </Paper>

        with mui.Paper:
            with mui.Typography:
                html.p("Hello world")
                html.p("Goodbye world")

    with elements("properties"):

        # You can add properties to elements with named parameters.
        #
        # To find all available parameters for a given element, you can
        # refer to its related documentation on mui.com for MUI widgets,
        # on https://microsoft.github.io/monaco-editor/ for Monaco editor,
        # and so on.
        #
        # <Paper elevation={3} variant="outlined" square>
        #   <TextField label="My text input" defaultValue="Type here" variant="outlined" />
        # </Paper>

        with mui.Paper(elevation=3, variant="outlined", square=True):
            mui.TextField(
                label="My text input",
                defaultValue="Type here",
                variant="outlined",
            )

        # If you must pass a parameter which is also a Python keyword, you can append an
        # underscore to avoid a syntax error.
        #
        # <Collapse in />

        mui.Collapse(in_=True)

        # mui.collapse(in=True)
        # > Syntax error: 'in' is a Python keyword:

    with elements("style_mui_sx"):

        # For Material UI elements, use the 'sx' property.
        #
        # <Box
        #   sx={{
        #     bgcolor: 'background.paper',
        #     boxShadow: 1,
        #     borderRadius: 2,
        #     p: 2,
        #     minWidth: 300,
        #   }}
        # >
        #   Some text in a styled box
        # </Box>

        mui.Box(
            "Some text in a styled box",
            sx={
                "bgcolor": "background.paper",
                "boxShadow": 1,
                "borderRadius": 2,
                "p": 2,
                "minWidth": 300,
            }
        )



    with elements("style_elements_css"):

        # For any other element, use the 'css' property.
        #
        # <div
        #   css={{
        #     backgroundColor: 'hotpink',
        #     '&:hover': {
        #         color: 'lightgreen'
        #     }
        #   }}
        # >
        #   This has a hotpink background
        # </div>

        html.div(
            "This has a hotpink background",
            css={
                "backgroundColor": "hotpink",
                "&:hover": {
                    "color": "lightgreen"
                }
            }
        )



    with elements("callbacks_retrieve_data"):

        # Some element allows executing a callback on specific event.
        #
        # const [name, setName] = React.useState("")
        # const handleChange = (event) => {
        #   // You can see here that a text field value
        #   // is stored in event.target.value
        #   setName(event.target.value)
        # }
        #
        # <TextField
        #   label="Input some text here"
        #   onChange={handleChange}
        # />

        # Initialize a new item in session state called "my_text"
        if "my_text" not in st.session_state:
            st.session_state.my_text = ""

        # When text field changes, this function will be called.
        # To know which parameters are passed to the callback,
        # you can refer to the element's documentation.
        def handle_change(event):
            st.session_state.my_text = event.target.value

        # Here we display what we have typed in our text field
        mui.Typography(st.session_state.my_text)

        # And here we give our 'handle_change' callback to the 'onChange'
        # property of the text field.
        mui.TextField(label="Input some text here", onChange=handle_change)



    with elements("callbacks_sync"):
    
        # If you just want to store callback parameters into Streamlit's session state
        # like above, you can also use the special function sync().
        #
        # When an onChange event occurs, the callback is called with an event data object
        # as argument. In the example below, we are synchronizing that event data object with
        # the session state item 'my_event'.
        #
        # If an event passes more than one parameter, you can synchronize as many session state item
        # as needed like so:
        # >>> sync("my_first_param", "my_second_param")
        #
        # If you want to ignore the first parameter of an event but keep synchronizing the second,
        # pass None to sync:
        # >>> sync(None, "second_parameter_to_keep")
    
        from streamlit_elements import sync
    
        if "my_event" not in st.session_state:
            st.session_state.my_event = None
    
        if st.session_state.my_event is not None:
            text = st.session_state.my_event.target.value
        else:
            text = ""
    
        mui.Typography(text)
        mui.TextField(label="Input some text here", onChange=sync("my_event"))


    with elements("callbacks_lazy"):

        # With the two first examples, each time you input a letter into the text field,
        # the callback is invoked but the whole app is reloaded as well.
        #
        # To avoid reloading the whole app on every input, you can wrap your callback with
        # lazy(). This will defer the callback invocation until another non-lazy callback
        # is invoked. This can be useful to implement forms.

        from streamlit_elements import lazy

        if "first_name" not in st.session_state:
            st.session_state.first_name = None
            st.session_state.last_name = None

        if st.session_state.first_name is not None:
            first_name = st.session_state.first_name.target.value
        else:
            first_name = "John"

        if st.session_state.last_name is not None:
            last_name = st.session_state.last_name.target.value
        else:
            last_name = "Doe"

        def set_last_name(event):
            st.session_state.last_name = event

        # Display first name and last name
        mui.Typography("Your first name: ", first_name)
        mui.Typography("Your last name: ", last_name)

        # Lazily synchronize onChange with first_name and last_name state.
        # Inputting some text won't synchronize the value yet.
        mui.TextField(label="First name", onChange=lazy(sync("first_name")))

        # You can also pass regular python functions to lazy().
        mui.TextField(label="Last name", onChange=lazy(set_last_name))

        # Here we give a non-lazy callback to onClick using sync().
        # We are not interested in getting onClick event data object,
        # so we call sync() with no argument.
        #
        # You can use either sync() or a regular python function.
        # As long as the callback is not wrapped with lazy(), its invocation will
        # also trigger every other defered callbacks.
        mui.Button("Update first namd and last name", onClick=sync())


    with elements("callbacks_hotkey"):

        # Invoke a callback when a specific hotkey sequence is pressed.
        #
        # For more information regarding sequences syntax and supported keys,
        # go to Mousetrap's project page linked below.
        #
        # /!\ Hotkeys work if you don't have focus on Streamlit Elements's frame /!\
        # /!\ As with other callbacks, this reruns the whole app /!\

        from streamlit_elements import event

        def hotkey_pressed():
            print("Hotkey pressed")

        event.Hotkey("g", hotkey_pressed)

        # If you want your hotkey to work even in text fields, set bind_inputs to True.
        event.Hotkey("h", hotkey_pressed, bindInputs=True)
        mui.TextField(label="Try pressing 'h' while typing some text here.")

        # If you want to override default hotkeys (ie. ctrl+f to search in page),
        # set overrideDefault to True.
        event.Hotkey("ctrl+f", hotkey_pressed, overrideDefault=True)



    with elements("callbacks_interval"):

        # Invoke a callback every n seconds.
        #
        # /!\ As with other callbacks, this reruns the whole app /!\

        def call_every_second():
            print("Hello world")

        event.Interval(1, call_every_second)



    with elements("dashboard"):

        # You can create a draggable and resizable dashboard using
        # any element available in Streamlit Elements.

        from streamlit_elements import dashboard

        # First, build a default layout for every element you want to include in your dashboard

        layout = [
            # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
            dashboard.Item("first_item", 0, 0, 2, 2),
            dashboard.Item("second_item", 2, 0, 2, 2, isDraggable=False, moved=False),
            dashboard.Item("third_item", 0, 2, 1, 1, isResizable=False),
        ]

        # Next, create a dashboard layout using the 'with' syntax. It takes the layout
        # as first parameter, plus additional properties you can find in the GitHub links below.

        with dashboard.Grid(layout):
            mui.Paper("First item", key="first_item")
            mui.Paper("Second item (cannot drag)", key="second_item")
            mui.Paper("Third item (cannot resize)", key="third_item")

        # If you want to retrieve updated layout values as the user move or resize dashboard items,
        # you can pass a callback to the onLayoutChange event parameter.

        def handle_layout_change(updated_layout):
            # You can save the layout in a file, or do anything you want with it.
            # You can pass it back to dashboard.Grid() if you want to restore a saved layout.
            print(updated_layout)

        with dashboard.Grid(layout, onLayoutChange=handle_layout_change):
            mui.Paper("First item", key="first_item")
            mui.Paper("Second item (cannot drag)", key="second_item")
            mui.Paper("Third item (cannot resize)", key="third_item")


# Unauthenticated Display
def unauthenticated_display():
    authenticator.login('Login', 'main')

# Authentication Display Logic
name, authentication_status, username = authenticator.login('Login', 'main')
if authentication_status:
    st.session_state["authentication_status"] = True
    st.session_state["name"] = name
    st.session_state["username"] = username
    authenticated_display()
else:
    unauthenticated_display()
