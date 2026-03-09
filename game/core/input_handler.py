"""Input handling interfaces."""


class InputHandler:
    """Receives and routes player input."""

    def poll(self) -> None:
        """Poll input source once."""
        pass
