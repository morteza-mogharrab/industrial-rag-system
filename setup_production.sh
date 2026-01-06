set -e  # Exit on error

echo "============================================================"
echo "AER Directive Knowledge Assistant - Production Setup"
echo "============================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo -e "${YELLOW}⚠️  Virtual environment not activated${NC}"
    echo ""
    echo "Please activate your virtual environment first:"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    exit 1
fi

# Check for API key
if [[ -z "$OPENAI_API_KEY" ]]; then
    echo -e "${YELLOW}⚠️  OPENAI_API_KEY not set${NC}"
    echo ""
    echo "Please set your OpenAI API key:"
    echo "  export OPENAI_API_KEY='your-api-key-here'"
    echo ""
    echo "Or create a .env file with:"
    echo "  OPENAI_API_KEY=your-api-key-here"
    exit 1
fi

echo -e "${GREEN}✓${NC} Virtual environment: activated"
echo -e "${GREEN}✓${NC} API key: configured"
echo ""

# Step 1: Install dependencies
echo "Step 1: Installing Python dependencies..."
pip install -r requirements_production.txt -q
echo -e "${GREEN}✓${NC} Dependencies installed"
echo ""

# Step 2: Download PDFs
echo "Step 2: Downloading AER Directives..."

# Directive 001
if [ ! -f "directive_001.pdf" ]; then
    echo "  Downloading Directive 001..."
    curl -# -o directive_001.pdf "https://static.aer.ca/prd/documents/directives/Directive001.pdf"
    echo -e "${GREEN}✓${NC} Directive 001 downloaded"
else
    echo -e "${GREEN}✓${NC} Directive 001 already exists"
fi

# Directive 017
if [ ! -f "directive_017.pdf" ]; then
    echo "  Downloading Directive 017 (400+ pages, may take a moment)..."
    curl -# -o directive_017.pdf "https://static.aer.ca/prd/documents/directives/Directive017.pdf"
    echo -e "${GREEN}✓${NC} Directive 017 downloaded"
else
    echo -e "${GREEN}✓${NC} Directive 017 already exists"
fi

echo ""

# Step 3: Build vector database
echo "Step 3: Building vector database..."
echo "  This will take 3-5 minutes..."
echo ""

python3 industrial_rag_system.py

echo ""
echo -e "${GREEN}✓${NC} Vector database built successfully"
echo ""

# Step 4: Completion
echo "============================================================"
echo -e "${GREEN}✅ SETUP COMPLETE!${NC}"
echo "============================================================"
echo ""
echo "Your AER Directive Knowledge Assistant is ready to use."
echo ""
echo "To start the application:"
echo "  python3 industrial_app.py"
echo ""
echo "Then open your browser to: http://localhost:7860"
echo ""
echo "============================================================"
