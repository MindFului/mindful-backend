# app/core/database.py
from supabase import create_client, Client
from core.config import SUPABASE_URL, SUPABASE_KEY

# Singleton para el cliente de Supabase
_supabase_client: Client = None

def get_supabase_client() -> Client:
    """
    Obtiene el cliente de Supabase (singleton).
    """
    global _supabase_client
    if _supabase_client is None:
        _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _supabase_client

# Instancia global
supabase: Client = get_supabase_client()
