from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Case, User
from app.auth import get_current_user
from app.utils.pdf_generator import generate_case_report_pdf, generate_all_cases_report_pdf

router = APIRouter(prefix="/api/v1/reports", tags=["Reports"])


@router.get("/case/{case_id}/pdf")
def download_case_pdf(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate and download PDF report for a specific case."""
    case = db.query(Case).filter(Case.id == case_id).first()
    
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    # Generate PDF
    pdf_buffer = generate_case_report_pdf(case, db)
    
    # Return as downloadable file
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=case_{case.case_id}_report.pdf"
        }
    )


@router.get("/all-cases/pdf")
def download_all_cases_pdf(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate and download PDF report for all cases."""
    # Generate PDF
    pdf_buffer = generate_all_cases_report_pdf(db)
    
    # Return as downloadable file
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=all_cases_report.pdf"
        }
    )
