from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.api.models.chat import ChatMessage, ChatResponse
from app.api.models.invoice import InvoiceAnalysis
from app.services.vector_store import VectorStore
from typing import List, Optional
from app.core.config import settings
from datetime import datetime

class Chatbot:
    def __init__(self, vector_store: VectorStore):
        self.llm = ChatOpenAI(
            model_name=settings.LLM_MODEL_NAME,
            base_url=settings.OPENAI_BASE_URL,
            temperature=0.7
        )
        self.vector_store = vector_store
        
        self.chat_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an AI assistant specialized in helping users query and understand invoice reimbursement analyses.
            You have access to a database of invoice analyses and can provide detailed information about them.
            
            When responding:
            1. Use markdown formatting for better readability
            2. Be concise but informative
            3. If you reference specific invoices, mention their IDs
            4. If you're unsure about something, say so
            5. Use the provided context to answer questions accurately
            
            Previous conversation:
            {chat_history}
            
            Relevant invoice analyses:
            {invoice_analyses}
            
            User query: {query}
            """),
        ])

    async def process_query(
        self,
        query: str,
        chat_history: Optional[List[ChatMessage]] = None
    ) -> ChatResponse:
        # Search for relevant invoice analyses
        relevant_analyses = self.vector_store.search_analyses(query)
        
        # Format chat history
        formatted_history = ""
        if chat_history:
            formatted_history = "\n".join([
                f"{msg.role}: {msg.content}"
                for msg in chat_history
            ])
        
        # Format invoice analyses
        formatted_analyses = "\n\n".join([
            f"Invoice ID: {analysis.invoice_id}\n"
            f"Employee: {analysis.employee_name}\n"
            f"Status: {analysis.status}\n"
            f"Amount: ${analysis.total_amount}\n"
            f"Reimbursable: ${analysis.reimbursable_amount}\n"
            f"Reason: {analysis.reason}"
            for analysis in relevant_analyses
        ])
        
        # Prepare the prompt
        prompt = self.chat_prompt.format_messages(
            chat_history=formatted_history,
            invoice_analyses=formatted_analyses,
            query=query
        )
        
        # Get LLM response
        response = await self.llm.ainvoke(prompt)
        
        # Create new chat messages
        new_messages = []
        if chat_history:
            new_messages.extend(chat_history)
        
        new_messages.extend([
            ChatMessage(role="user", content=query),
            ChatMessage(role="assistant", content=response.content)
        ])
        
        # Create response
        return ChatResponse(
            response=response.content,
            relevant_invoices=[analysis.invoice_id for analysis in relevant_analyses],
            chat_history=new_messages
        ) 