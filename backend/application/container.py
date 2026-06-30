"""Application dependency container."""

from dataclasses import dataclass

from config.settings import Settings


@dataclass(frozen=True, slots=True)
class AppContainer:
    """Root dependency container for application-scoped objects."""

    settings: Settings
