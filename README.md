# AER Directive Knowledge Assistant

**Industrial RAG System for Alberta Energy Regulator Compliance**

AI-powered multi-document retrieval system for AER directives, providing instant access to regulatory requirements, technical procedures, and compliance information.

---

## 🎯 System Overview

### **Architecture**
- **Vector Database**: ChromaDB with persistent SQLite backend
- **Embeddings**: OpenAI text-embedding-3-small (1536 dimensions)
- **LLM**: OpenAI GPT-4o-mini for response generation
- **Interface**: Professional Gradio web application
- **Documents**: AER Directive 001 & Directive 017 (450+ pages total)

### **Key Features**
✅ **Multi-Document Search** - Query across multiple directives simultaneously  
✅ **Source Attribution** - All responses cite specific directives  
✅ **Document Filtering** - Narrow search to specific directives  
✅ **Semantic Search** - Natural language understanding of technical queries  
✅ **Production-Ready** - Clean, professional interface ready for deployment

---

## 📋 Prerequisites

- Python 3.8+
- OpenAI API key
- 2GB disk space (for PDFs and vector database)
- Internet connection (for initial setup)

---

## 🚀 Quick Start

### **Step 1: Clone/Download Project**

```bash
cd your-project-directory
```

### **Step 2: Create Virtual Environment**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **Step 3: Install Dependencies**

```bash
pip install -r requirements_production.txt
```

### **Step 4: Set OpenAI API Key**

```bash
export OPENAI_API_KEY='your-api-key-here'
```

Or create `.env` file:
```
OPENAI_API_KEY=your-api-key-here
```

### **Step 5: Download AER Directives**

```bash
# Download Directive 001 (Site-Specific Liability)
curl -o directive_001.pdf "https://static.aer.ca/prd/documents/directives/Directive001.pdf"

# Download Directive 017 (Measurement Requirements) - 400+ pages
curl -o directive_017.pdf "https://static.aer.ca/prd/documents/directives/Directive017.pdf"
```

### **Step 6: Build Vector Database**

```bash
python3 industrial_rag_system.py
```

**Expected time:** 3-5 minutes  
**Expected output:** ~1,500+ chunks indexed

### **Step 7: Launch Application**

```bash
python3 industrial_app.py
```

Open browser to: **http://localhost:7860**

---

## 📂 Project Structure

```
industrial-rag-system/
├── industrial_rag_system.py      # Core RAG implementation
├── industrial_app.py              # Web interface
├── requirements_production.txt   # Dependencies
├── README.md                     # This file
├── .env                          # API key (create this)
│
├── directive_001.pdf             # AER Directive 001 (download)
├── directive_017.pdf             # AER Directive 017 (download)
│
└── chroma_db/                    # Vector database (generated)
    ├── chroma.sqlite3
    └── [index files]
```

---

## 💬 Using the System

### **Web Interface**

1. **Ask Questions** in natural language:
   - "What are the measurement accuracy requirements for natural gas?"
   - "What documentation is required for liability assessments?"

2. **Filter by Document**:
   - Select specific directive from dropdown
   - Or search across all documents

3. **View Sources**:
   - Each answer cites specific directives
   - Relevance scores show confidence

### **Example Queries**

**Directive 001 (Compliance):**
- "What are the requirements for site-specific liability assessment?"
- "What documentation is required for liability assessments?"
- "What are the reporting requirements under Directive 001?"

**Directive 017 (Measurement):**
- "What are the measurement accuracy requirements for natural gas?"
- "How should differential pressure meters be calibrated?"
- "What are the temperature compensation requirements?"
- "What inspection procedures are required for measurement equipment?"

---

## 🛠️ System Configuration

### **Chunk Settings** (in `industrial_rag_system.py`)

```python
chunk_size = 500        # Characters per chunk
overlap = 100           # Overlap between chunks
```

### **Search Settings**

```python
top_k = 5              # Number of chunks retrieved per query
temperature = 0.3      # LLM temperature (lower = more factual)
max_tokens = 600       # Maximum response length
```

### **Model Configuration**

```python
embedding_model = "text-embedding-3-small"  # OpenAI embeddings
chat_model = "gpt-4o-mini"                  # Response generation
```

---

## 💰 Cost Analysis

### **One-Time Setup Costs**

| Task | Tokens | Cost |
|------|--------|------|
| Directive 001 embeddings | ~50K | ~$0.001 |
| Directive 017 embeddings | ~500K | ~$0.010 |
| **Total Setup** | ~550K | **~$0.01** |

### **Per-Query Costs**

| Component | Cost |
|-----------|------|
| Query embedding | ~$0.0001 |
| Response generation (GPT-4o-mini) | ~$0.002 |
| **Total per Query** | **~$0.002** |

### **Monthly Estimate (1000 queries)**
- **~$2-3 per month** for active usage

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| **Index Build Time** | 3-5 minutes |
| **Query Response Time** | 2-4 seconds |
| **Total Chunks** | ~1,500 (Directive 001 + 017) |
| **Storage Size** | ~50-100 MB |
| **Supported Documents** | 450+ pages |

---

## 🔧 Troubleshooting

### **Issue: "OPENAI_API_KEY not set"**
```bash
export OPENAI_API_KEY='your-key'
# Or add to .env file
```

### **Issue: "directive_001.pdf not found"**
```bash
curl -o directive_001.pdf "https://static.aer.ca/prd/documents/directives/Directive001.pdf"
curl -o directive_017.pdf "https://static.aer.ca/prd/documents/directives/Directive017.pdf"
```

### **Issue: "ChromaDB collection not found"**
```bash
rm -rf ./chroma_db/
python3 industrial_rag_system.py
```

### **Issue: Gradio compatibility errors**
```bash
pip install gradio==4.44.1 --force-reinstall
pip install huggingface_hub==0.20.3
```

### **Issue: Port 7860 already in use**
```bash
# Kill existing process
lsof -ti:7860 | xargs kill -9

# Or change port in industrial_app.py:
server_port=7861
```

---

## 🚀 Deployment Options

### **Option 1: Local Deployment**
Current setup - runs on localhost:7860

### **Option 2: Internal Network**
Change `server_name="0.0.0.0"` to make accessible on local network

### **Option 3: Cloud Deployment**

**Gradio Cloud (Hugging Face Spaces):**
```python
demo.launch(share=True)  # Creates public URL
```

**Docker Deployment:**
```dockerfile
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements_production.txt
CMD ["python3", "industrial_app.py"]
```

**AWS/GCP/Azure:**
- Deploy as containerized application
- Use environment variables for API keys
- Mount persistent storage for ChromaDB

---

## 🔒 Security Considerations

### **Production Deployment**
- ✅ Never commit API keys to Git
- ✅ Use environment variables or secrets management
- ✅ Implement authentication (add to Gradio interface)
- ✅ Enable HTTPS for production
- ✅ Regular security audits

### **Data Privacy**
- ⚠️ PDF content sent to OpenAI for embeddings
- ⚠️ Queries sent to OpenAI for responses
- ✅ ChromaDB data stored locally
- ✅ No data retention beyond session (unless logged)

---

## 📈 Scaling Recommendations

### **Current System: Good For**
- ✅ 1-1000 queries per day
- ✅ 10-50 concurrent users
- ✅ 1000-10,000 document chunks

### **To Scale Beyond:**

**1. Add More Documents (10K+ chunks)**
- Switch to Qdrant for better performance
- Implement caching layer (Redis)

**2. High Traffic (1000+ concurrent users)**
- Deploy behind load balancer
- Use async processing
- Implement request queuing

**3. Enterprise Requirements**
- Add user authentication
- Implement audit logging
- Add usage analytics
- Enable A/B testing

---

## 🎓 Technical Deep Dive

### **RAG Pipeline**

```
1. User Query
   ↓
2. Query Embedding (OpenAI)
   ↓
3. Vector Search (ChromaDB)
   ↓
4. Retrieve Top-K Chunks
   ↓
5. Build Context with Citations
   ↓
6. LLM Generation (GPT-4o-mini)
   ↓
7. Return Answer + Sources
```

### **ChromaDB Implementation**

- **Storage**: SQLite backend for persistence
- **Indexing**: Automatic with ChromaDB
- **Search**: Cosine similarity on normalized vectors
- **Metadata**: Document source, type, chunk index

### **Semantic Search Details**

- **Embedding Dimension**: 1536
- **Distance Metric**: Cosine similarity
- **Normalization**: L2 normalization
- **Chunk Strategy**: Overlapping windows for context preservation

---

## 📝 Adding More Documents

To add additional AER directives:

```python
# In industrial_rag_system.py, modify main():

documents = [
    {
        'path': 'directive_001.pdf',
        'name': 'Directive 001',
        'type': 'Site-Specific Liability'
    },
    {
        'path': 'directive_017.pdf',
        'name': 'Directive 017',
        'type': 'Measurement Requirements'
    },
    # Add new document:
    {
        'path': 'directive_060.pdf',
        'name': 'Directive 060',
        'type': 'Flaring & Venting'
    }
]
```

Then rebuild index:
```bash
rm -rf ./chroma_db/
python3 industrial_rag_system.py
```

---

## 🤝 Maintenance

### **Updating Directives**
When AER publishes updated directives:

1. Download new PDF
2. Replace old PDF
3. Rebuild index: `python3 industrial_rag_system.py`

### **Model Updates**
To use different OpenAI models:

```python
# In industrial_rag_system.py
model = "gpt-4"  # Higher quality, higher cost
# OR
model = "gpt-3.5-turbo"  # Lower cost, faster
```

---

## 📄 License

This is a demonstration project for industrial RAG systems. Ensure compliance with AER terms of use for directive documents.

---

## 🆘 Support

For issues:
1. Check Troubleshooting section
2. Verify all prerequisites met
3. Ensure PDFs are downloaded correctly
4. Check ChromaDB database exists

---

**Built with Python • ChromaDB • OpenAI • Gradio**

*Production-ready RAG system demonstrating enterprise-grade AI architecture for regulatory compliance*
