from sqlalchemy.orm import Session
from typing import List, Optional

from app.models import DCA
from app.schemas import DCACreate, DCAUpdate


class DCAService:
    """Service layer for DCA management operations."""
    
    @staticmethod
    def create_dca(db: Session, dca_data: DCACreate) -> DCA:
        """Create a new DCA."""
        dca = DCA(**dca_data.model_dump())
        db.add(dca)
        db.commit()
        db.refresh(dca)
        return dca
    
    @staticmethod
    def get_dca(db: Session, dca_id: int) -> Optional[DCA]:
        """Get DCA by ID."""
        return db.query(DCA).filter(DCA.id == dca_id).first()
    
    @staticmethod
    def list_dcas(
        db: Session,
        active_only: bool = False,
        skip: int = 0,
        limit: int = 100
    ) -> List[DCA]:
        """List all DCAs."""
        query = db.query(DCA)
        
        if active_only:
            query = query.filter(DCA.is_active == True)
        
        return query.order_by(DCA.performance_score.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_dca(db: Session, dca_id: int, dca_data: DCAUpdate) -> Optional[DCA]:
        """Update DCA information."""
        dca = DCAService.get_dca(db, dca_id)
        if not dca:
            return None
        
        update_data = dca_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(dca, field, value)
        
        db.commit()
        db.refresh(dca)
        return dca
    
    @staticmethod
    def delete_dca(db: Session, dca_id: int) -> bool:
        """Delete a DCA (soft delete by marking inactive)."""
        dca = DCAService.get_dca(db, dca_id)
        if not dca:
            return False
        
        dca.is_active = False
        db.commit()
        return True
