from rich import print
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns

# Panel demonstration
title = "Hello, Rich!"
content = "Rich makes it easy to produce beautiful terminal text."
panel = Panel(content, title=title, expand=False)
print(panel)

# Columns demonstration
columns = Columns([Text("Column 1"), Text("Column 2"), Text("Column 3")])
print(columns)

# Table demonstration
table = Table(show_header=True, header_style="bold blue")
table.add_column("Date", style="dim", width=12)
table.add_column("Title")
table.add_column("Production Budget", justify="right")
table.add_column("Box Office", justify="right")
table.add_row("Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$275,000,000", "$373,525,625")
table.add_row("May 25, 2018", "Solo: A Star Wars Story", "$275,000,000", "$393,151,347")
table.add_row("Dec 15, 2017", "Star Wars Ep. VIII: The Last Jedi", "$262,000,000", "$1,332,539,889")
print(table)

# Progress bar demonstration
from rich.progress import track

for _ in track(range(100), description="Processing..."):
    pass

print("Task completed!")
