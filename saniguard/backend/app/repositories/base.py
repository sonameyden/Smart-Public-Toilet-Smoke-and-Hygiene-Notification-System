from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseRepository(ABC):
    """
    Marker base class for all repositories.
    Enforces that every repository declares a table name
    and provides a consistent interface pattern.
    Repositories are the ONLY layer that touches the database.
    """

    @property
    @abstractmethod
    def table(self) -> str:
        """Return the Supabase table name this repository manages."""
        ...
