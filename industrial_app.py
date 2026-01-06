"""
AER Directive Knowledge Assistant - Redesigned UI
Professional interface following Alberta Environmental Consulting best practices
"""
import os
import gradio as gr
from industrial_rag_system import IndustrialRAGSystem
from datetime import datetime
class IndustrialWebInterface:
    """Professional web interface for industrial compliance queries"""
    
    def __init__(self):
        self.rag = None
        self.conversation_history = []
        self.initialize_system()
    
    def initialize_system(self):
        """Initialize the RAG system"""
        print("Initializing Industrial RAG System...")
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set")
        
        try:
            self.rag = IndustrialRAGSystem(api_key=api_key)
            
            if os.path.exists("./chroma_db"):
                print("Loading existing index...")
                self.rag.load_index()
                stats = self.rag.get_stats()
                print(f"✓ Loaded {stats['total_chunks']} chunks from {stats['total_documents']} documents")
            else:
                raise FileNotFoundError(
                    "ChromaDB index not found. Please run 'python3 industrial_rag_system.py' first"
                )
            
            print("✓ System ready")
            
        except Exception as e:
            print(f"ERROR: {e}")
            raise
    
    def chat(self, message, history, document_filter):
            """Process chat message"""
            if not message or not message.strip():
                return history
            
            # 1. Append User Message
            history.append({"role": "user", "content": message})
            
            # 2. Append Assistant Placeholder
            history.append({"role": "assistant", "content": "⚙️ Searching directives..."})
            yield history
            
            try:
                # Get response
                response = self.rag.generate_response(
                    message,
                    top_k=5,
                    document_filter=document_filter if document_filter != "All Documents" else None
                )
                
                # Store conversation (internal logging)
                self.conversation_history.append({
                    'timestamp': datetime.now().isoformat(),
                    'query': message,
                    'answer': response['answer'],
                    'sources': response['sources'],
                    'filter': document_filter
                })
                
                # 3. Update Assistant Message with real answer
                history[-1]['content'] = response['answer']
                yield history
                
            except Exception as e:
                error_msg = f"Error processing query: {str(e)}\n\nPlease try rephrasing your question."
                # Update error in the last message
                history[-1]['content'] = error_msg
                yield history
    
    def clear_chat(self):
        """Clear conversation"""
        self.conversation_history = []
        return []
    
    def get_document_list(self):
        """Get list of available documents"""
        stats = self.rag.get_stats()
        docs = ["All Documents"]
        if 'documents' in stats:
            docs.extend([info['name'] for info in stats['documents'].values()])
        return docs
def create_interface():
    """Create professional Gradio interface with Alberta environmental consulting design"""
    
    interface = IndustrialWebInterface()
    
    # Professional Alberta environmental consulting color scheme
    # Inspired by AER branding: deep blues, earth tones, clean professional aesthetic
    custom_css = """
    @import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@300;400;600;700&family=Merriweather:wght@400;700&display=swap');
    
    :root {
        --aer-primary: #003366;
        --aer-secondary: #004d99;
        --aer-accent: #0073cf;
        --earth-green: #2d5a3d;
        --earth-brown: #5c4033;
        --sky-light: #e8f4fc;
        --stone-gray: #64748b;
        --warm-white: #fafbfc;
        --border-light: #d1d9e0;
        --text-dark: #1e293b;
        --text-muted: #64748b;
        --text-light: #ffffff;
        --text-light-muted: rgba(255, 255, 255, 0.85);
    }
    
    * {
        box-sizing: border-box;
    }
    
    .gradio-container {
        font-family: 'Source Sans Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        max-width: 1400px !important;
        margin: 0 auto !important;
        background: linear-gradient(180deg, #f0f4f8 0%, #ffffff 100%) !important;
        min-height: 100vh;
        padding: 0 !important;
    }
    
    /* ===== HEADER SECTION ===== */
    .main-header {
        background: linear-gradient(135deg, var(--aer-primary) 0%, var(--aer-secondary) 50%, var(--earth-green) 100%);
        padding: 0;
        margin: 0 0 2rem 0;
        border-radius: 0 0 24px 24px;
        box-shadow: 0 4px 20px rgba(0, 51, 102, 0.15);
        overflow: hidden;
        position: relative;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        pointer-events: none;
    }
    
    .header-content {
        padding: 2.5rem 3rem;
        position: relative;
        z-index: 1;
    }
    
    .header-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1.5rem;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    .logo-section {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .logo-icon {
        width: 56px;
        height: 56px;
        background: rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.75rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: #ffffff;
    }
    
    .logo-text h1 {
        color: #ffffff;
        font-size: 1.75rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.02em;
        font-family: 'Merriweather', Georgia, serif;
    }
    
    .logo-text span {
        color: rgba(255, 255, 255, 0.85);
        font-size: 0.875rem;
        font-weight: 400;
        letter-spacing: 0.02em;
    }
    
    .header-badge {
        background: rgba(255, 255, 255, 0.12);
        color: #ffffff;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    .header-description {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.125rem;
        line-height: 1.6;
        max-width: 700px;
        margin: 0;
    }
    
    /* ===== INFO CARDS SECTION ===== */
    .info-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.25rem;
        padding: 0 1.5rem;
        margin-bottom: 2rem;
    }
    
    .info-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid var(--border-light);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        transition: all 0.2s ease;
    }
    
    .info-card:hover {
        box-shadow: 0 4px 16px rgba(0, 51, 102, 0.08);
        transform: translateY(-2px);
    }
    
    .info-card-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
    }
    
    .info-card-icon {
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
    }
    
    .icon-compliance { background: rgba(0, 115, 207, 0.1); }
    .icon-sources { background: rgba(45, 90, 61, 0.1); }
    .icon-accuracy { background: rgba(92, 64, 51, 0.1); }
    
    .info-card h3 {
        color: var(--text-dark);
        font-size: 1rem;
        font-weight: 600;
        margin: 0;
    }
    
    .info-card p {
        color: var(--text-muted);
        font-size: 0.9rem;
        line-height: 1.6;
        margin: 0;
    }
    
    /* ===== MAIN CONTENT AREA ===== */
    .main-content {
        padding: 0 1.5rem;
        display: grid;
        grid-template-columns: 1fr 320px;
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    @media (max-width: 1024px) {
        .main-content {
            grid-template-columns: 1fr;
        }
    }
    
    /* ===== CHAT SECTION ===== */
    .chat-section {
        background: #ffffff;
        border-radius: 20px;
        border: 1px solid var(--border-light);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
        overflow: hidden;
    }
    
    .chat-header {
        background: linear-gradient(90deg, var(--sky-light) 0%, #ffffff 100%);
        padding: 1.25rem 1.5rem;
        border-bottom: 1px solid var(--border-light);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .chat-title {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .chat-title h2 {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-dark);
        margin: 0;
    }
    
    .chat-status {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.8rem;
        color: var(--earth-green);
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        background: var(--earth-green);
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    #chatbot {
        height: 480px !important;
        border: none !important;
        background: #fafbfc !important;
    }
    
    #chatbot .message {
        font-family: 'Source Sans Pro', sans-serif !important;
        font-size: 0.95rem !important;
        line-height: 1.65 !important;
    }
    
    /* FIXED: User message text is now white on dark blue background */
    #chatbot .user {
        background: linear-gradient(135deg, var(--aer-primary) 0%, var(--aer-secondary) 100%) !important;
        color: #ffffff !important;
        border-radius: 18px 18px 4px 18px !important;
    }
    
    #chatbot .user * {
        color: #ffffff !important;
    }
    
    #chatbot .user p,
    #chatbot .user span,
    #chatbot .user div {
        color: #ffffff !important;
    }
    
    #chatbot .bot {
        background: #ffffff !important;
        border: 1px solid var(--border-light) !important;
        border-radius: 18px 18px 18px 4px !important;
        color: var(--text-dark) !important;
    }
    
    #chatbot .bot * {
        color: var(--text-dark) !important;
    }
    
    /* Additional Gradio chatbot overrides for text visibility */
    #chatbot .message.user .message-content,
    #chatbot .message.user .prose,
    #chatbot .message.user p {
        color: #ffffff !important;
    }
    
    #chatbot .message.bot .message-content,
    #chatbot .message.bot .prose,
    #chatbot .message.bot p {
        color: var(--text-dark) !important;
    }
    
    /* ===== INPUT AREA ===== */
    .input-area {
        padding: 1.25rem 1.5rem;
        background: #ffffff;
        border-top: 1px solid var(--border-light);
    }
    
    .input-row {
        display: flex;
        gap: 0.75rem;
        align-items: stretch;
    }
    
    .input-row textarea {
        flex: 1;
        border: 2px solid var(--border-light) !important;
        border-radius: 12px !important;
        padding: 0.875rem 1rem !important;
        font-size: 0.95rem !important;
        font-family: 'Source Sans Pro', sans-serif !important;
        resize: none !important;
        background: var(--warm-white) !important;
        transition: all 0.2s ease !important;
        min-height: 52px !important;
        color: var(--text-dark) !important;
    }
    
    .input-row textarea:focus {
        border-color: var(--aer-accent) !important;
        box-shadow: 0 0 0 3px rgba(0, 115, 207, 0.1) !important;
        background: #ffffff !important;
    }
    
    .input-row textarea::placeholder {
        color: var(--text-muted) !important;
    }
    
    .send-btn {
        background: linear-gradient(135deg, var(--aer-primary) 0%, var(--aer-secondary) 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        min-width: 100px !important;
    }
    
    .send-btn:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(0, 51, 102, 0.25) !important;
    }
    
    .clear-btn {
        background: transparent !important;
        color: var(--text-muted) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-size: 0.85rem !important;
        cursor: pointer !important;
        margin-top: 0.75rem !important;
        transition: all 0.2s ease !important;
    }
    
    .clear-btn:hover {
        background: var(--warm-white) !important;
        color: var(--text-dark) !important;
    }
    
    /* ===== SIDEBAR ===== */
    .sidebar {
        display: flex;
        flex-direction: column;
        gap: 1.25rem;
    }
    
    .sidebar-card {
        background: #ffffff;
        border-radius: 16px;
        border: 1px solid var(--border-light);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        overflow: hidden;
    }
    
    .sidebar-card-header {
        background: linear-gradient(90deg, var(--sky-light) 0%, #ffffff 100%);
        padding: 1rem 1.25rem;
        border-bottom: 1px solid var(--border-light);
    }
    
    .sidebar-card-header h3 {
        font-size: 0.95rem;
        font-weight: 600;
        color: var(--text-dark);
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .sidebar-card-content {
        padding: 1.25rem;
    }
    
    .filter-dropdown {
        width: 100%;
    }
    
    .filter-dropdown select {
        width: 100% !important;
        padding: 0.75rem 1rem !important;
        border: 2px solid var(--border-light) !important;
        border-radius: 10px !important;
        font-size: 0.9rem !important;
        color: var(--text-dark) !important;
        background: var(--warm-white) !important;
        cursor: pointer !important;
    }
    
    .filter-dropdown select:focus {
        border-color: var(--aer-accent) !important;
        box-shadow: 0 0 0 3px rgba(0, 115, 207, 0.1) !important;
    }
    
    /* Document list styling */
    .doc-list {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    
    .doc-item {
        padding: 0.875rem;
        border-radius: 10px;
        background: var(--warm-white);
        margin-bottom: 0.625rem;
        border: 1px solid transparent;
        transition: all 0.2s ease;
    }
    
    .doc-item:hover {
        border-color: var(--border-light);
        background: #ffffff;
    }
    
    .doc-item:last-child {
        margin-bottom: 0;
    }
    
    .doc-name {
        font-weight: 600;
        color: var(--text-dark);
        font-size: 0.9rem;
        margin-bottom: 0.25rem;
    }
    
    .doc-meta {
        font-size: 0.8rem;
        color: var(--text-muted);
    }
    
    .doc-tag {
        display: inline-block;
        background: rgba(0, 115, 207, 0.1);
        color: var(--aer-accent);
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        margin-right: 0.5rem;
    }
    
    /* ===== EXAMPLES SECTION ===== */
    .examples-section {
        padding: 0 1.5rem;
        margin-bottom: 2rem;
    }
    
    .examples-card {
        background: #ffffff;
        border-radius: 16px;
        border: 1px solid var(--border-light);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        overflow: hidden;
    }
    
    .examples-header {
        background: linear-gradient(90deg, rgba(45, 90, 61, 0.05) 0%, #ffffff 100%);
        padding: 1rem 1.5rem;
        border-bottom: 1px solid var(--border-light);
    }
    
    .examples-header h3 {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-dark);
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .examples-grid {
        padding: 1.25rem;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 0.75rem;
    }
    
    .example-btn {
        background: var(--warm-white) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: 10px !important;
        padding: 0.875rem 1rem !important;
        text-align: left !important;
        font-size: 0.875rem !important;
        color: var(--text-dark) !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        line-height: 1.5 !important;
    }
    
    .example-btn:hover {
        background: #ffffff !important;
        border-color: var(--aer-accent) !important;
        box-shadow: 0 2px 8px rgba(0, 115, 207, 0.1) !important;
    }
    
    /* ===== FOOTER - FIXED COLORS ===== */
    .main-footer {
        background: var(--aer-primary);
        color: #ffffff;
        padding: 2rem 1.5rem;
        margin-top: 2rem;
        border-radius: 24px 24px 0 0;
    }
    
    .footer-content {
        max-width: 1200px;
        margin: 0 auto;
        display: grid;
        grid-template-columns: 2fr 1fr;
        gap: 2rem;
        align-items: center;
    }
    
    @media (max-width: 768px) {
        .footer-content {
            grid-template-columns: 1fr;
            text-align: center;
        }
    }
    
    .footer-main h4 {
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0 0 0.5rem 0;
        color: #ffffff;
    }
    
    .footer-main p {
        font-size: 0.875rem;
        color: rgba(255, 255, 255, 0.85);
        margin: 0;
        line-height: 1.6;
    }
    
    .footer-tech {
        text-align: right;
    }
    
    @media (max-width: 768px) {
        .footer-tech {
            text-align: center;
        }
    }
    
    .footer-tech-label {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: rgba(255, 255, 255, 0.6);
        margin-bottom: 0.5rem;
    }
    
    .footer-tech-stack {
        display: flex;
        gap: 0.5rem;
        justify-content: flex-end;
        flex-wrap: wrap;
    }
    
    @media (max-width: 768px) {
        .footer-tech-stack {
            justify-content: center;
        }
    }
    
    .tech-badge {
        background: rgba(255, 255, 255, 0.15);
        color: #ffffff;
        padding: 0.35rem 0.75rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 500;
    }
    
    .footer-disclaimer {
        margin-top: 1.5rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(255, 255, 255, 0.15);
        text-align: center;
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.7);
        line-height: 1.6;
    }
    
    /* ===== GRADIO OVERRIDES ===== */
    .contain {
        background: transparent !important;
    }
    
    .gr-box {
        border: none !important;
        background: transparent !important;
    }
    
    .gr-padded {
        padding: 0 !important;
    }
    
    label {
        font-family: 'Source Sans Pro', sans-serif !important;
    }
    
    .label-wrap {
        margin-bottom: 0.5rem !important;
    }
    
    /* Hide unnecessary elements */
    .gr-form {
        background: transparent !important;
        border: none !important;
    }
    """
    
    with gr.Blocks(title="AER Directive Knowledge Assistant") as demo:
        
        # ===== HEADER =====
        gr.HTML("""
        <div class="main-header">
            <div class="header-content">
                <div class="header-top">
                    <div class="logo-section">
                        <div class="logo-icon">⚡</div>
                        <div class="logo-text">
                            <h1>AER Directive Assistant</h1>
                            <span>Knowledge-Based Regulatory Guidance System</span>
                        </div>
                    </div>
                    <div class="header-badge">AI-Powered</div>
                </div>
                <p class="header-description">
                    Access intelligent guidance on Alberta Energy Regulator directives. 
                    Get accurate compliance information, technical specifications, and regulatory requirements 
                    with full source attribution.
                </p>
            </div>
        </div>
        """)
        
        # ===== INFO CARDS =====
        gr.HTML("""
        <div class="info-grid">
            <div class="info-card">
                <div class="info-card-header">
                    <div class="info-card-icon icon-compliance">📋</div>
                    <h3>Compliance Guidance</h3>
                </div>
                <p>Query regulatory requirements, procedures, and standards from official AER directives with confidence.</p>
            </div>
            <div class="info-card">
                <div class="info-card-header">
                    <div class="info-card-icon icon-sources">📚</div>
                    <h3>Source Attribution</h3>
                </div>
                <p>Every response includes specific directive citations so you can verify and reference the official documentation.</p>
            </div>
            <div class="info-card">
                <div class="info-card-header">
                    <div class="info-card-icon icon-accuracy">🎯</div>
                    <h3>Technical Accuracy</h3>
                </div>
                <p>Access measurement requirements, calibration procedures, and technical specifications with precision.</p>
            </div>
        </div>
        """)
        
        # ===== MAIN CONTENT =====
        with gr.Row(elem_classes=["main-content"]):
            # Chat Section
            with gr.Column(scale=3, elem_classes=["chat-section"]):
                gr.HTML("""
                <div class="chat-header">
                    <div class="chat-title">
                        <span>💬</span>
                        <h2>Ask Your Question</h2>
                    </div>
                    <div class="chat-status">
                        <span class="status-dot"></span>
                        System Ready
                    </div>
                </div>
                """)
                
                chatbot = gr.Chatbot(
                    [],
                    elem_id="chatbot",
                    show_label=False
                )
                
                gr.HTML('<div class="input-area">')
                with gr.Row(elem_classes=["input-row"]):
                    msg = gr.Textbox(
                        placeholder="Ask about AER directives, compliance requirements, or technical procedures...",
                        show_label=False,
                        scale=5,
                        container=False,
                        lines=1
                    )
                    submit_btn = gr.Button("Send", variant="primary", scale=1, elem_classes=["send-btn"])
                
                clear_btn = gr.Button("🗑️ Clear Conversation", elem_classes=["clear-btn"])
                gr.HTML('</div>')
            
            # Sidebar
            with gr.Column(scale=1, elem_classes=["sidebar"]):
                # Document Filter Card
                gr.HTML("""
                <div class="sidebar-card">
                    <div class="sidebar-card-header">
                        <h3>📁 Document Filter</h3>
                    </div>
                    <div class="sidebar-card-content">
                """)
                
                document_filter = gr.Dropdown(
                    choices=interface.get_document_list(),
                    value="All Documents",
                    label="",
                    show_label=False,
                    elem_classes=["filter-dropdown"]
                )
                
                gr.HTML("""
                    </div>
                </div>
                """)
                
                # Available Documents Card
                stats = interface.rag.get_stats()
                doc_html = """
                <div class="sidebar-card">
                    <div class="sidebar-card-header">
                        <h3>📄 Available Documents</h3>
                    </div>
                    <div class="sidebar-card-content">
                        <ul class="doc-list">
                """
                
                if 'documents' in stats:
                    for doc_id, info in stats['documents'].items():
                        doc_html += f"""
                        <li class="doc-item">
                            <div class="doc-name">{info['name']}</div>
                            <div class="doc-meta">
                                <span class="doc-tag">{info['type']}</span>
                                {info['chunks']} indexed sections
                            </div>
                        </li>
                        """
                
                doc_html += """
                        </ul>
                    </div>
                </div>
                """
                
                gr.HTML(doc_html)
        
        # ===== EXAMPLES SECTION =====
        gr.HTML("""
        <div class="examples-section">
            <div class="examples-card">
                <div class="examples-header">
                    <h3>💡 Example Queries</h3>
                </div>
                <div class="examples-grid">
        """)
        
        examples = gr.Examples(
            examples=[
                "What are the requirements for site-specific liability assessment?",
                "What are the measurement accuracy requirements for natural gas?",
                "How should differential pressure meters be calibrated?",
                "What documentation is required for liability assessments?",
                "What are the temperature compensation requirements for gas measurement?",
                "What inspection procedures are required for measurement equipment?",
                "What are the reporting requirements for measurement errors?",
                "How are volumetric conversions calculated for gas measurement?"
            ],
            inputs=msg,
            label=None,
            examples_per_page=8
        )
        
        gr.HTML("""
                </div>
            </div>
        </div>
        """)
        
        # ===== FOOTER =====
        gr.HTML("""
        <div class="main-footer">
            <div class="footer-content">
                <div class="footer-main">
                    <h4>Alberta Energy Regulator Directive Assistant</h4>
                    <p>Providing intelligent access to regulatory compliance information for Alberta's energy sector professionals.</p>
                </div>
                <div class="footer-tech">
                    <div class="footer-tech-label">Powered By</div>
                    <div class="footer-tech-stack">
                        <span class="tech-badge">ChromaDB</span>
                        <span class="tech-badge">OpenAI GPT-4</span>
                        <span class="tech-badge">RAG Architecture</span>
                    </div>
                </div>
            </div>
            <div class="footer-disclaimer">
                ⚠️ All responses are based on official AER directives. Always verify critical compliance information with current regulations. 
                This tool is intended as a reference aid and does not constitute legal or regulatory advice.
            </div>
        </div>
        """)
        
        # ===== EVENT HANDLERS =====
        def submit_and_clear(message, history, doc_filter):
            for response in interface.chat(message, history, doc_filter):
                yield response, ""
        
        msg.submit(
            submit_and_clear,
            inputs=[msg, chatbot, document_filter],
            outputs=[chatbot, msg]
        )
        
        submit_btn.click(
            submit_and_clear,
            inputs=[msg, chatbot, document_filter],
            outputs=[chatbot, msg]
        )
        
        clear_btn.click(
            interface.clear_chat,
            outputs=[chatbot]
        )
    
    return demo, custom_css
def main():
    """Launch the application"""
    print("="*60)
    print("AER Directive Knowledge Assistant")
    print("Professional UI for Alberta Environmental Consulting")
    print("="*60)
    
    try:
        demo, custom_css = create_interface()
        
        print("\n✓ Starting web server...")
        print("\nAccess the application at: http://localhost:7860")
        print("Press Ctrl+C to stop\n")
        
        demo.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            show_error=True,
            css=custom_css,
            theme=gr.themes.Soft()
        )
        
    except Exception as e:
        print(f"\nERROR: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure OPENAI_API_KEY is set")
        print("2. Run 'python3 industrial_rag_system.py' to build index")
        print("3. Check that directive PDFs are downloaded")
        raise
if __name__ == "__main__":
    main()