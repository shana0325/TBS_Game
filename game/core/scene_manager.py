"""Scene management interfaces."""


class SceneManager:
    """Tracks and switches active scenes."""

    def change_scene(self, scene_name: str) -> None:
        """Switch to another scene by name."""
        pass
