from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..celery_utils import celery_app
from .. import models

router = APIRouter(
    prefix="/invoices",
    tags=["invoices"],
)

@router.post("/{invoice_id}/generate-pdf")
def generate_pdf(invoice_id: int, db: Session = Depends(get_db)):
    # Verify invoice exists (optional, task handles it too but better to fail fast)
    # Using raw SQL for simplicity since we didn't map Invoice model in FastAPI yet, 
    # OR assume we map it. 
    # For now, let's just send the task. The task handles "Invoice not found".
    
    # We must match the task name defined in Django. 
    # Django app name is 'billing', task is 'generate_invoice_pdf'.
    # Shared tasks usually get name 'billing.tasks.generate_invoice_pdf'
    
    task_name = "billing.tasks.generate_invoice_pdf"
    task = celery_app.send_task(task_name, args=[invoice_id])
    
    return {"message": "PDF generation started", "task_id": str(task.id)}
