from rich.console import Console, Group
from rich.markdown import Markdown
from rich.padding import Padding
from rich.panel import Panel
from rich.text import Text
from rich.console import Console

# Colors based on the original repo
ACCENT = "#7aa2f7"
USER = "#9ece6a"
TOOL = "#e0af68"
MUTED = "#565f89"

class UI:
    def __init__(self):
        self.console = Console()

    def banner(self):
        self.console.print()
        self.console.print(
            Padding(Text("🚀 SAJAL'S AI CODER", style=f"bold {ACCENT}"), (0, 0, 0, 2))
        )
        self.console.print(
            Padding(Text("Memory: Persistent  ·  Tools: Active  ·  Type 'quit' to exit", style=MUTED), (0, 0, 0, 2))
        )

    def user(self, text):
        self.console.print(
            Padding(Text(f"You: {text.strip()}", style=f"bold {USER}"), (1, 0, 0, 2))
        )

    def agent(self, text):
        self.console.print(
            Padding(
                Group(
                    Text("Agent", style=f"bold {ACCENT}"),
                    Padding(Markdown(text.strip()), (1, 0, 0, 0)),
                ),
                (1, 2, 0, 2),
            )
        )

    def tool(self, name, args, result):
        # Create a nice panel for the tool execution
        header = Text.assemble(
            (f"🛠️ {name} ", f"bold {TOOL}"),
            (str(args), MUTED),
        )
        self.console.print(
            Padding(
                Panel(
                    Text(result, style=MUTED),
                    title=header,
                    border_style=MUTED,
                    padding=(0, 1),
                ),
                (1, 2, 0, 2),
            )
        )

    def working(self, label="Thinking"):
        """returns a status context manager"""
        return self.console.status(
            Text(label, style=MUTED), spinner="dots", spinner_style=ACCENT
        )

ui = UI()
