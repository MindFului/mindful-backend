# app/core/config.py
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv('.env')

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# Debug: confirm which Supabase URL is loaded
if SUPABASE_URL:
	print(f"[config] SUPABASE_URL loaded: {SUPABASE_URL}")
else:
	print("[config] SUPABASE_URL is empty")

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
