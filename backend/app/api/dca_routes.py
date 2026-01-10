from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas import DCACreate, DCAUpdate, DCAResponse
from app.models import User, RoleEnum
from app.services import DCAService
from app.auth import get_current_active_user, require_role

router = APIRouter(prefix="/api/v1/dcas", tags=["DCAs"])


@router.post("/", response_model=DCAResponse, status_code=status.HTTP_201_CREATED)
def create_dca(
    dca_data: DCACreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.ADMIN]))
):
    """Create a new DCA (Admin only)."""
    try:
        dca = DCAService.create_dca(db, dca_data)
        return dca
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[DCAResponse])
def list_dcas(
    active_only: bool = Query(False),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List all DCAs."""
    dcas = DCAService.list_dcas(db, active_only=active_only, skip=skip, limit=limit)
    return dcas


@router.get("/{dca_id}", response_model=DCAResponse)
def get_dca(
    dca_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get DCA by ID."""
    dca = DCAService.get_dca(db, dca_id)
    if not dca:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"DCA {dca_id} not found"
        )
    return dca


@router.patch("/{dca_id}", response_model=DCAResponse)
def update_dca(
    dca_id: int,
    dca_data: DCAUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.ADMIN]))
):
    """Update DCA information (Admin only)."""
    dca = DCAService.update_dca(db, dca_id, dca_data)
    if not dca:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"DCA {dca_id} not found"
        )
    return dca


@router.delete("/{dca_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dca(
    dca_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.ADMIN]))
):
    """Delete a DCA (Admin only)."""
    success = DCAService.delete_dca(db, dca_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"DCA {dca_id} not found"
        )
    return None
