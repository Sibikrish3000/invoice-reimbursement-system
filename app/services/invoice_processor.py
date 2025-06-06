from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from app.api.models.invoice import InvoiceAnalysis, ReimbursementStatus
from app.core.config import settings
import uuid
from datetime import datetime
import json

class InvoiceProcessor:
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name=settings.LLM_MODEL_NAME,
            temperature=0
        )
        self.parser = PydanticOutputParser(pydantic_object=InvoiceAnalysis)
        
        self.analysis_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert at analyzing expense invoices against company reimbursement policies.
            Your task is to analyze the given invoice against the provided policy and determine:
            1. The reimbursement status (FULLY_REIMBURSED, PARTIALLY_REIMBURSED, or DECLINED)
            2. The reimbursable amount
            3. Detailed reasons for the decision
            4. Any policy violations found
            
            Policy:
            {policy_text}
            
            Invoice:
            {invoice_text}
            
            {format_instructions}
            """),
        ])

    async def analyze_invoice(self, employee_name: str, policy_text: str, invoice_text: str) -> InvoiceAnalysis:
        # Generate a unique invoice ID
        invoice_id = str(uuid.uuid4())
        
        # Prepare the prompt
        prompt = self.analysis_prompt.format_messages(
            policy_text=policy_text,
            invoice_text=invoice_text,
            format_instructions=self.parser.get_format_instructions()
        )
        
        # Get LLM response
        response = await self.llm.ainvoke(prompt)
        
        # Parse the response
        try:
            analysis = self.parser.parse(response.content)
            # Ensure the invoice_id is set
            analysis.invoice_id = invoice_id
            analysis.employee_name = employee_name
            return analysis
        except Exception as e:
            # If parsing fails, create a default analysis
            return InvoiceAnalysis(
                invoice_id=invoice_id,
                employee_name=employee_name,
                invoice_date=datetime.utcnow(),
                total_amount=0.0,
                reimbursable_amount=0.0,
                status=ReimbursementStatus.DECLINED,
                reason=f"Error analyzing invoice: {str(e)}",
                policy_violations=["Failed to parse invoice"]
            ) 