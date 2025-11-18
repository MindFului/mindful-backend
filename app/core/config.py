# app/core/config.py
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv('.env.local')

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
