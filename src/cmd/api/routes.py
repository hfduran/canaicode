from datetime import datetime
import io
from typing import Any, Dict, List

from fastapi import APIRouter, Body, Depends, File, HTTPException, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel

from src.auth.verify_user_access import verify_user_access
from src.auth.dual_auth import get_user_id_dual_auth
from src.dependencies.dependency_setters import set_create_user_dependencies
from src.dependencies.dependency_setters import set_validate_user_dependencies
from src.dependencies.dependency_setters import set_get_commit_metrics_dependencies
from src.dependencies.dependency_setters import set_get_copilot_metrics_dependencies
from src.dependencies.dependency_setters import set_get_xlsx_commit_metrics_dependencies
from src.dependencies.dependency_setters import set_get_calculated_metrics_dependencies
from src.dependencies.dependency_setters import set_get_copilot_metrics_by_language_dependencies
from src.dependencies.dependency_setters import set_get_copilot_metrics_by_period_dependencies
from src.dependencies.dependency_setters import set_get_copilot_users_metrics_dependencies
from src.dependencies.dependency_setters import set_create_github_app_dependencies
from src.dependencies.dependency_setters import set_create_api_key_dependencies
from src.dependencies.dependency_setters import set_list_api_keys_dependencies
from src.dependencies.dependency_setters import set_revoke_api_key_dependencies
from src.domain.entities.commit_metrics import CommitMetrics
from src.domain.use_cases.dtos.calculated_metrics import CalculatedMetrics, CopilotMetricsByLanguage, CopilotMetricsByPeriod, CopilotUsersMetrics
from src.domain.use_cases.dtos.token import Token
from src.domain.use_cases.dtos.user_response import UserResponse
from src.domain.use_cases.dtos.api_key_response import ApiKeyResponse, ApiKeyListItem
from src.infrastructure.database.connection.database_connection import SessionLocal


class RegisterRequest(BaseModel):
    username: str
    password: str
    full_name: str
    enterprise_name: str = ""
    email: str
    cellphone: str
    cpf_cnpj: str


class CreateApiKeyRequest(BaseModel):
    user_id: str
    key_name: str
    expires_at: str = ""  # Optional: ISO format datetime string

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_db() -> Any:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=UserResponse)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
)-> UserResponse:
    create_user_use_case = set_create_user_dependencies(db)
    response = create_user_use_case.execute(
        request.username,
        request.password,
        request.full_name,
        request.enterprise_name,
        request.email,
        request.cellphone,
        request.cpf_cnpj
    )
    return response


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Token:
    validate_user_use_case = set_validate_user_dependencies(db)
    response = validate_user_use_case.execute(form_data.username, form_data.password)
    return response


@router.get("/commit_metrics/upload_deprecated/{team_name}")
def get_commit_metrics(
    team_name: str,
    user_id: str = "",
    date_string: str = "",
    db: Session = Depends(get_db),
) -> List[CommitMetrics]:
    date = datetime.strptime(date_string, "%Y-%m-%d").date()
    get_commit_metrics_use_case = set_get_commit_metrics_dependencies(db)
    response = get_commit_metrics_use_case.execute(date, team_name, user_id)
    return response


@router.post("/copilot_metrics/upload")
async def get_copilot_metrics(
    file: UploadFile = File(...),
    user_id: str = Body(..., embed=True),
    authenticated_user_id: str = Depends(get_user_id_dual_auth),
    db: Session = Depends(get_db),
) -> Dict[str, List[Any]]:
    if authenticated_user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied: cannot access other user's data")

    file_content = await file.read()
    data = json.loads(file_content)
    get_copilot_metrics_use_case = set_get_copilot_metrics_dependencies(db)
    response = get_copilot_metrics_use_case.execute(data, user_id)
    return response


@router.post("/commit_metrics/upload")
async def get_commit_metrics_xlsx(
    file: UploadFile = File(...),
    user_id: str = Body(..., embed=True),
    authenticated_user_id: str = Depends(get_user_id_dual_auth),
    db: Session = Depends(get_db),
) -> List[CommitMetrics]:
    # Verify the authenticated user matches the requested user_id
    if authenticated_user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied: cannot access other user's data")

    file_content = io.BytesIO(await file.read())
    get_xlsx_commit_metrics_use_case = set_get_xlsx_commit_metrics_dependencies(db)
    response = get_xlsx_commit_metrics_use_case.execute(file_content, user_id)
    return response


@router.get("/calculated_metrics/{user_id}")
def get_calculated_metrics(
    user_id: str,
    period: str = "",
    productivity_metric: str = "",
    initial_date_string: str = "",
    final_date_string: str = "",
    languages_string: str = "",
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> CalculatedMetrics | None:
    verify_user_access(token, user_id)
    initial_date = datetime.strptime(initial_date_string, "%Y-%m-%d")
    final_date = datetime.strptime(final_date_string, "%Y-%m-%d")
    languages: List[str] = []
    if(languages_string):
        languages = languages_string.split(',')
    get_calculated_metrics_use_case = set_get_calculated_metrics_dependencies(db)
    response = get_calculated_metrics_use_case.execute(user_id, period, productivity_metric, initial_date, final_date, languages) # type: ignore
    return response


@router.get("/copilot_metrics/language/{user_id}")
def get_copilot_metrics_by_language(
    user_id: str,
    initial_date_string: str = "",
    final_date_string: str = "",
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> List[CopilotMetricsByLanguage]:
    verify_user_access(token, user_id)
    initial_date = None
    final_date = None
    if(initial_date_string):
        initial_date = datetime.strptime(initial_date_string, "%Y-%m-%d")
    if(final_date_string):
        final_date = datetime.strptime(final_date_string, "%Y-%m-%d")
    get_copilot_metrics_by_language_use_case = set_get_copilot_metrics_by_language_dependencies(db)
    response = get_copilot_metrics_by_language_use_case.execute(user_id, initial_date, final_date)
    return response

@router.get("/copilot_metrics/period/{user_id}")
def get_copilot_metrics_by_period(
    user_id: str,
    period: str = "",
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> List[CopilotMetricsByPeriod]:
    verify_user_access(token, user_id)
    get_copilot_metrics_by_period_use_case = set_get_copilot_metrics_by_period_dependencies(db)
    response = get_copilot_metrics_by_period_use_case.execute(user_id, period) # type: ignore
    return response


@router.get("/copilot_metrics/users/{user_id}")
def get_copilot_metrics_by_users(
    user_id: str,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> List[CopilotUsersMetrics]:
    verify_user_access(token, user_id)
    get_copilot_users_metrics_use_case = set_get_copilot_users_metrics_dependencies(db)
    response = get_copilot_users_metrics_use_case.execute(user_id)
    return response

@router.post("/github_app")
def create_github_app(
    user_id: str = Body(..., embed=True),
    organization_name: str = Body(..., embed=True),
    app_id: str = Body(..., embed=True),
    installation_id: str = Body(..., embed=True),
    private_key: str = Body(..., embed=True),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> None:
    verify_user_access(token, user_id)
    create_github_app_use_case = set_create_github_app_dependencies(db)
    create_github_app_use_case.execute(user_id, organization_name, app_id, installation_id, private_key)


@router.post("/api_keys", response_model=ApiKeyResponse)
def create_api_key(
    request: CreateApiKeyRequest,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> ApiKeyResponse:
    verify_user_access(token, request.user_id)

    # Parse expiration date if provided
    expires_at = None
    if request.expires_at:
        expires_at = datetime.strptime(request.expires_at, "%Y-%m-%d")

    create_api_key_use_case = set_create_api_key_dependencies(db)
    full_key, api_key_entity = create_api_key_use_case.execute(
        request.user_id,
        request.key_name,
        expires_at
    )

    return ApiKeyResponse(
        id=api_key_entity.id,  # type: ignore
        key=full_key,
        key_name=api_key_entity.key_name,
        created_at=api_key_entity.created_at,  # type: ignore
        expires_at=api_key_entity.expires_at,
    )


@router.get("/api_keys/{user_id}", response_model=List[ApiKeyListItem])
def list_api_keys(
    user_id: str,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> List[ApiKeyListItem]:
    verify_user_access(token, user_id)
    list_api_keys_use_case = set_list_api_keys_dependencies(db)
    api_keys = list_api_keys_use_case.execute(user_id)

    # Convert to list items with masked keys
    return [
        ApiKeyListItem(
            id=key.id,  # type: ignore
            key_prefix=f"{key.key_prefix}...{key.key_prefix[-3:]}",  # Show first 15 and last 3 chars
            key_name=key.key_name,
            created_at=key.created_at,  # type: ignore
            last_used_at=key.last_used_at,
            expires_at=key.expires_at,
        )
        for key in api_keys
    ]


@router.delete("/api_keys/{key_id}")
def revoke_api_key(
    key_id: str,
    user_id: str = Body(..., embed=True),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Dict[str, str]:
    verify_user_access(token, user_id)
    revoke_api_key_use_case = set_revoke_api_key_dependencies(db)
    revoke_api_key_use_case.execute(user_id, key_id)
    return {"message": "API key revoked successfully"}
