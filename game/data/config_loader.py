"""Configuration loading interfaces."""


class ConfigLoader:
    """Loads static JSON configs."""

    def load(self, path: str) -> dict:
        """Return placeholder config object."""
        return {}
