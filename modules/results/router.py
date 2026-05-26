from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from modules.users.service import users_service
import io
import openpyxl
from modules.results.service import resultsService
from modules.results.schemas import ResultDTO


router = APIRouter()
@router.get("/all")
def get_all_results():
    results =  resultsService.get_all_results()
    return results

@router.get("/organization/{organization_id}")
def get_results_by_organization(organization_id: str):
    results =  resultsService.get_results_by_organization(organization_id)
    return results

@router.get("/organization/{organization_id}/export")
def export_results_by_organization(organization_id: str):
    users = users_service.get_by_organization(organization_id)
    results = resultsService.get_results_by_organization(organization_id)

    user_by_id = {user.get("id"): user for user in (users or [])}

    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = "results"

    worksheet.append(
        [
            "Nombre",
            "Apellido",
            "Telefono",
            "Correo",
            "Colegio",
            "Grado",
            "Seccion",
            "Depresion",
            "Level",
        ]
    )

    for result in results or []:
        user = user_by_id.get(result.get("userId"))
        if not user:
            continue
        worksheet.append(
            [
                user.get("nombre", ""),
                user.get("apellido", ""),
                user.get("telefono", ""),
                user.get("email", ""),
                user.get("colegio", ""),
                user.get("grado", ""),
                user.get("seccion", ""),
                result.get("result", ""),
                result.get("level", ""),
            ]
        )

    output = io.BytesIO()
    workbook.save(output)
    output.seek(0)

    filename = f"results_organization_{organization_id}.xlsx"
    headers = {"Content-Disposition": f"attachment; filename={filename}"}

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers,
    )

@router.get("/user/{user_id}")
def get_results_by_user(user_id: str):
    results =  resultsService.get_result_by_user(user_id)
    return results