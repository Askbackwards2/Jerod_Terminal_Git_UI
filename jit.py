from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Label, Button, ListItem, ListView
from textual.containers import HorizontalGroup
import subprocess

MY_USERNAME = "jdepifanio"

class GitStuff():

    @staticmethod
    def get_branch_name() -> str:
        output: str = subprocess.run(
                    ["git", "status"],
                    capture_output=True,
                    text=True,
                    check=True
                ).stdout
        return output.split("\n")[0].strip()

    @staticmethod
    def get_branches() -> list[str]:
        subprocess.run(args=["git", "fetch"])
        output: str = subprocess.run(
                args=["git", "branch", "-r"],
                capture_output=True,
                text=True,
                check=True
            ).stdout
        lines_array = [line.strip() for line in output.splitlines() if line.strip()]
        output_array: list[str] = []
        for line in lines_array:
            if MY_USERNAME in line:
                output_array.append(line)
        return output_array


class BranchStatus(HorizontalGroup):
    """Shows git branch status"""

    def compose(self) -> ComposeResult:
        """Create child widgets of a stopwatch."""
        yield Label(GitStuff.get_branch_name())
        yield ListView(*tuple(ListItem(Label(line)) for line in GitStuff.get_branches()))
        yield Button("Fetch", id="fetch")


class Jit(App):
    """A Textual app to manage stopwatches."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield BranchStatus()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


if __name__ == "__main__":
    app = Jit()
    app.run()
