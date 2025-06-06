from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime

class ReimbursementStatus(str, Enum):
    FULLY_REIMBURSED = "FULLY_REIMBURSED"
    PARTIALLY_REIMBURSED = "PARTIALLY_REIMBURSED"
    DECLINED = "DECLINED"

class InvoiceAnalysis(BaseModel):
    invoice_id: str = Field(..., description="Unique identifier for the invoice")
    employee_name: str = Field(..., description="Name of the employee")
    invoice_date: datetime = Field(..., description="Date of the invoice")
    total_amount: float = Field(..., description="Total amount of the invoice")
    reimbursable_amount: float = Field(..., description="Amount that can be reimbursed")
    status: ReimbursementStatus = Field(..., description="Reimbursement status")
    reason: str = Field(..., description="Detailed reason for the reimbursement status")
    policy_violations: Optional[List[str]] = Field(default=None, description="List of policy violations if any")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class InvoiceAnalysisResponse(BaseModel):
    success: bool = Field(..., description="Whether the analysis was successful")
    message: str = Field(..., description="Response message")
    analysis: Optional[InvoiceAnalysis] = Field(default=None, description="Analysis results if successful")

class InvoiceAnalysisRequest(BaseModel):
    employee_name: str = Field(..., description="Name of the employee")
    policy_text: str = Field(..., description="Text content of the reimbursement policy")
    invoice_text: str = Field(..., description="Text content of the invoice") 