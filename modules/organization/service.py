from core.database import supabase
class OrganizationService:
    def get_all_organizations(self):
        # Aquí iría la lógica para obtener las organizaciones desde la base de datos
        # Por ejemplo, podrías usar supabase para hacer una consulta a la tabla de organizaciones
        try:
            response = supabase.table("organization").select("*").execute()
            return response.data
        except Exception as e:
            print(f"Error fetching organizations: {e}")
            return []
    def get_organization_by_name(self, name):
        try:
            response = supabase.table("organization").select("*").eq("name", name).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error fetching organization by name: {e}")
            return None


organizationService = OrganizationService()