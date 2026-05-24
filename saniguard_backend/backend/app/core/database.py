from supabase import create_client, Client
from app.core.config import settings

_client: Client | None = None


def get_db() -> Client:
    """
    Returns a singleton Supabase client.
    Called inside each repository method — never called directly from routers.
    """
    global _client
    if _client is None:
        _client = create_client(settings.supabase_url, settings.supabase_key)
    return _client
