from streamlit_elements import elements, mui, html
# TODO: Create a function that saves the layout every 30 sec, without rereun the page.
# TODO: Make a function to read the last dashboard settings.
# TODO: Create a function that dynamically creates the elements ondemand. But also removes them if a certain number of unused elemnents are rachend.
# TODO: Create a Presentation about this Topic for git,
# TODO: add the frature Bheir or so....

with elements("dashboard"):
    # You can create a draggable and resizable dashboard using
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
        mui.Paper("First item clone", key="first_item")
        mui.Paper("Second item clone (cannot drag)", key="second_item")
        mui.Paper("Third item clone (cannot resize)", key="third_item")