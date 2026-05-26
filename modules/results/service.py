# app/modules/results/service.py
import uuid
from core.database import supabase

class ResultsService:
    def process_save(self,user_id,result,level):
        result_data ={
            "userId": user_id,
            "result": result.get("result"),
            "level": level
        }
        try:
            supabase.table("results").insert(result_data).execute()
        except Exception as e:
            print(f"Error saving result: {e}")

    def get_all_results(self):
        try:
            response = supabase.table("results").select("*").execute()
            return response.data
        except Exception as e:
            print(f"Error fetching results: {e}")
            return []
    def get_result_by_user(self, user_id):
        try:
            response = (
                supabase.table("results")
                .select("*")
                .eq("userId", user_id)
                .order("created_at", desc=True)
                .limit(1)
                .execute()
            )
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error fetching results for user {user_id}: {e}")
            return None
        
    def get_results_by_organization(self, organization_id):
        try:
            users_response = (
                supabase.table("users")
                .select("id")
                .eq("organizationId", organization_id)
                .execute()
            )
            user_ids = [user["id"] for user in (users_response.data or [])]

            if not user_ids:
                return []

            results_response = (
                supabase.table("results")
                .select("*")
                .in_("userId", user_ids)
                .execute()
            )
            return results_response.data
        except Exception as e:
            print(f"Error fetching results for organization {organization_id}: {e}")
            return []
        
resultsService = ResultsService()