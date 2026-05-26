from fastapi import APIRouter
from modules.organization.service import organizationService
router = APIRouter()
@router.get("/all")
def get_all_organizations():
    organizations = organizationService.get_all_organizations()
    return organizations
@router.get("/{name}")
def get_organization_by_name(name: str):
    organization = organizationService.get_organization_by_name(name)
    return organization
