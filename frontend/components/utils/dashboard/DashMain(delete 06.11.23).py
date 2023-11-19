from components.utils.dashboard.DashConfig import (
    configure_dash_items,
    configure_dash_layouts,
    dashboard_test,
)


def dash_items(page):
    configure_dash_items(page)


def dash_layouts(page):
    configure_dash_layouts(page)


def dash_build(page):
    dashboard_test(page)
