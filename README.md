# Intelligent Invoice Reimbursement System

An advanced system for automating invoice analysis and providing intelligent querying capabilities using Large Language Models (LLMs) and vector databases.

## Features

- **Automated Invoice Analysis**: Process PDF invoices against company reimbursement policies
- **Intelligent Data Storage**: Store analysis results in a vector database for efficient retrieval
- **Smart Querying**: Natural language chatbot interface for querying invoice information
- **Policy Compliance**: Automated comparison of invoices against company policies

## System Components

### 1. Invoice Analysis Endpoint
- Processes PDF invoices and company policies
- Uses LLM for intelligent analysis
- Determines reimbursement status (Fully/Partially Reimbursed or Declined)
- Stores results in vector database

### 2. RAG Chatbot Endpoint
- Natural language query interface
- Context-aware responses
- Intelligent retrieval of invoice information
- Support for metadata filtering

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Sibikrish3000/invoice-reimbursement-system.git
cd invoice-reimbursement-system
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with:
```
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=your_endpoint_url
```

## Usage

1. Start the server:
```bash
uvicorn app.main:app --reload
```

2. Access the API documentation at `http://localhost:8000/docs`

### API Endpoints

#### Invoice Analysis
- **POST** `/api/v1/analyze-invoice`
  - Input: PDF files (policy and invoices), employee name
  - Output: Analysis results with reimbursement status

#### Chatbot Query
- **POST** `/api/v1/chat`
  - Input: Natural language query
  - Output: Markdown formatted response

## Technical Details

### Technologies Used
- **Framework**: FastAPI
- **LLM Integration**: LangChain with OpenAI
- **Vector Store**: ChromaDB
- **Embedding Model**: Sentence Transformers
- **Document Processing**: PyPDF

### Architecture
- Modular design with separate services for invoice processing and querying
- Vector database for efficient similarity search
- RAG implementation for context-aware responses

## Development

### Project Structure
```
invoice-reimbursement-system/
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── routes/
│   │   └── models/
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── services/
│   │   ├── invoice_processor.py
│   │   ├── vector_store.py
│   │   └── chatbot.py
│   └── utils/
│       ├── pdf_processor.py
│       └── embeddings.py
├── tests/
├── requirements.txt
└── README.md
```

## License

MIT License


## Containerization

To build and run your container:
```bash
docker build -t invoice-reimbursement-system .
docker run -p 8000:8000 --env-file .env invoice-reimbursement-system 
