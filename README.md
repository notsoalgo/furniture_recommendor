# AI-Powered Furniture Recommendation & Analytics App

A complete ML-driven web application that uses AI to recommend furniture products and generate creative product descriptions. Built with FastAPI (backend), React (frontend), and integrated with Pinecone vector database and Google Gemini AI.

## 🌟 Features

### Core Functionality
- **AI-Powered Recommendations**: Semantic search using sentence transformers (all-MiniLM-L6-v2) to find furniture based on natural language queries
- **Creative Product Descriptions**: Google Gemini Pro generates engaging, marketing-style descriptions for each product
- **Conversational Interface**: Chat-like UI for a natural recommendation experience
- **Analytics Dashboard**: Interactive visualizations showing product statistics, brand distribution, and pricing insights
- **Vector Database**: Pinecone for fast similarity search across thousands of products
- **Dark Mode**: Full dark mode support for comfortable viewing

### Technical Highlights
- **NLP**: Text embeddings combine title, description, brand, and material for rich semantic representations
- **ML/AI**: Sentence transformers for embeddings, LangChain for GenAI integration
- **Data Processing**: Jupyter notebooks for data analytics and model training
- **Modern Stack**: FastAPI backend, React frontend with TypeScript, Tailwind CSS for styling

## 🏗️ Tech Stack

### Backend
- **Framework**: FastAPI
- **ML/AI Libraries**:
  - `sentence-transformers` - Text embeddings (all-MiniLM-L6-v2 model)
  - `pinecone` - Vector database for similarity search
  - `langchain` - AI framework for GenAI workflows
  - `langchain-google-genai` - Google Gemini Pro integration
- **Data Processing**: pandas, numpy
- **Server**: Uvicorn (ASGI server)

### Frontend
- **Framework**: React 18 with TypeScript
- **Routing**: Wouter (lightweight React router)
- **State Management**: TanStack Query (React Query)
- **UI Components**: Shadcn/ui (Radix UI primitives)
- **Styling**: Tailwind CSS with custom design system
- **Charts**: Recharts for data visualization

### Data Science
- **Notebooks**: Jupyter for data analytics and model training
- **Visualization**: Plotly for interactive charts
- **Dataset**: Furniture product catalog with 10,000+ items

### Infrastructure
- **Vector Database**: Pinecone (serverless)
- **AI Model**: Google Gemini 1.5 Flash
- **Embeddings**: 384-dimensional vectors (all-MiniLM-L6-v2)

## 📋 Prerequisites

- **Python 3.11+** (for backend and notebooks)
- **Node.js 20+** (for frontend)
- **Pinecone Account** - [Sign up at pinecone.io](https://www.pinecone.io/)
- **Google AI Studio Account** - [Get API key at aistudio.google.com](https://aistudio.google.com/)

## 🚀 Setup and Installation

### 1. Clone the Repository

\`\`\`bash
git clone <your-repo-url>
cd furniture-recommendation-app
\`\`\`

### 2. Backend Setup (Python/FastAPI)

#### Install Python Dependencies

\`\`\`bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install required packages
pip install pandas==2.3.3
pip install plotly==6.3.1
pip install jupyter==1.1.1
pip install sentence-transformers==5.1.1
pip install pinecone==5.4.2
pip install langchain==0.3.18
pip install langchain-google-genai==2.0.7
pip install langchain-pinecone==0.2.12
pip install fastapi==0.115.7
pip install uvicorn==0.34.0
pip install python-dotenv==1.0.1
\`\`\`

#### Configure Environment Variables

Create a \`.env\` file in the project root:

\`\`\`env
# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=us-east-1  # or your Pinecone environment

# Google Gemini AI
GOOGLE_API_KEY=your_google_api_key_here
\`\`\`

**How to get API keys:**

1. **Pinecone API Key**:
   - Visit [pinecone.io](https://www.pinecone.io/)
   - Sign up for a free account
   - Navigate to API Keys section
   - Copy your API key

2. **Google Gemini API Key**:
   - Visit [Google AI Studio](https://aistudio.google.com/)
   - Sign in with your Google account
   - Click "Get API Key"
   - Create a new API key or use existing one

### 3. Frontend Setup (React)

#### Install Node.js Dependencies

\`\`\`bash
# Install all frontend dependencies
npm install
\`\`\`

### 4. Data Processing and Model Training

#### Run Data Analytics Notebook

\`\`\`bash
jupyter notebook notebooks/data_analytics.ipynb
\`\`\`

This notebook:
- Loads the furniture dataset
- Performs exploratory data analysis
- Generates visualizations (top brands, price distribution)
- Analyzes data quality

#### Run Model Training Notebook

\`\`\`bash
jupyter notebook notebooks/model_training.ipynb
\`\`\`

This notebook:
- Creates combined text representations (title + description + brand + material)
- Generates embeddings using all-MiniLM-L6-v2
- Creates Pinecone index named "furniture-recommender"
- Uploads all product embeddings with metadata

**⚠️ Important**: Run the model training notebook completely before starting the backend server. This populates the Pinecone vector database.

## 🎮 Usage

### Starting the Application

#### 1. Start the FastAPI Backend

\`\`\`bash
# Navigate to backend directory
cd backend

# Run the server
python main.py
\`\`\`

The backend will be available at:
- API: \`http://localhost:8000\`
- Interactive docs: \`http://localhost:8000/docs\`
- Alternative docs: \`http://localhost:8000/redoc\`

#### 2. Start the React Frontend

\`\`\`bash
# From project root
npm run dev
\`\`\`

The frontend will be available at:
- App: \`http://localhost:5000\`

### Using the Application

#### Recommendations Page
1. Navigate to the home page
2. Type a natural language query (e.g., "modern sofa for small living room")
3. Press Enter or click the send button
4. View AI-generated recommendations with creative descriptions

**Example queries**:
- "Comfortable office chair under $500"
- "Rustic wooden dining table for 6 people"
- "Minimalist bedroom furniture"
- "Outdoor patio furniture set"

#### Analytics Dashboard
1. Navigate to the Analytics page using the navigation bar
2. View comprehensive statistics:
   - Total product count
   - Top 10 brands by product count
   - Category distribution
   - Price statistics (min, max, mean, median)

## 📁 Project Structure

\`\`\`
furniture-recommendation-app/
├── backend/
│   └── main.py                 # FastAPI application with endpoints
├── notebooks/
│   ├── data_analytics.ipynb    # Data exploration and visualization
│   └── model_training.ipynb    # Embedding generation and Pinecone setup
├── client/
│   ├── src/
│   │   ├── components/
│   │   │   ├── product-card.tsx      # Reusable product display card
│   │   │   ├── theme-provider.tsx    # Dark mode context
│   │   │   └── theme-toggle.tsx      # Theme switcher button
│   │   ├── pages/
│   │   │   ├── recommendation-page.tsx  # Main recommendation interface
│   │   │   └── analytics-page.tsx       # Analytics dashboard
│   │   ├── App.tsx             # Main app with routing
│   │   └── index.css           # Tailwind + custom styles
│   ├── index.html              # HTML entry point
│   └── package.json            # Frontend dependencies
├── design_guidelines.md        # UI/UX design specifications
├── .env                        # Environment variables (not in git)
└── README.md                   # This file
\`\`\`

## 🔧 API Endpoints

### POST /recommend/

Generate furniture recommendations based on user query.

**Request Body**:
\`\`\`json
{
  "query": "comfortable modern sofa",
  "top_k": 8
}
\`\`\`

**Response**:
\`\`\`json
{
  "query": "comfortable modern sofa",
  "products": [
    {
      "uniq_id": "12345",
      "title": "Modern 3-Seater Sofa",
      "price": 899.99,
      "brand": "ComfortPlus",
      "images": "https://example.com/image.jpg",
      "creative_description": "Transform your living space with this...",
      "similarity_score": 0.89
    }
  ],
  "count": 8
}
\`\`\`

### GET /analytics/

Get statistical analytics about the product dataset.

**Response**:
\`\`\`json
{
  "total_products": 10000,
  "top_brands": {
    "Brand A": 1500,
    "Brand B": 1200
  },
  "top_categories": {
    "Living Room": 3000,
    "Bedroom": 2500
  },
  "price_stats": {
    "min": 29.99,
    "max": 5999.99,
    "mean": 450.00,
    "median": 299.99,
    "std": 350.00
  }
}
\`\`\`

### GET /health

Health check showing status of all services.

## 🎨 Design System

The application follows a professional e-commerce + AI product aesthetic with:

- **Color Scheme**: Teal primary (trustworthy, sophisticated) with terracotta accents
- **Typography**: Inter for body text, Outfit for headings
- **Layout**: Generous spacing, card-based design, responsive grid system
- **Interactions**: Subtle hover effects, smooth transitions, loading states
- **Dark Mode**: Full support with proper contrast ratios

See `design_guidelines.md` for complete specifications.

## 🧪 Testing

### Backend Testing

Test the API endpoints:

\`\`\`bash
# Health check
curl http://localhost:8000/health

# Get analytics
curl http://localhost:8000/analytics/

# Get recommendations
curl -X POST http://localhost:8000/recommend/ \\
  -H "Content-Type: application/json" \\
  -d '{"query": "modern sofa", "top_k": 5}'
\`\`\`

### Frontend Testing

The application includes comprehensive test IDs for automated testing. All interactive elements have \`data-testid\` attributes.

## 🔍 Model Performance

### Embedding Model (all-MiniLM-L6-v2)
- **Dimension**: 384
- **Speed**: ~14,000 sentences/second (CPU)
- **Quality**: High semantic similarity for product search
- **Size**: ~90MB model file

### Vector Database (Pinecone)
- **Index**: furniture-recommender
- **Metric**: Cosine similarity
- **Response Time**: <50ms for top-10 queries
- **Capacity**: Serverless, auto-scaling

### GenAI (Google Gemini 1.5 Flash)
- **Temperature**: 0.7 (creative but controlled)
- **Max Tokens**: 150 per description
- **Response Time**: ~500ms per product

## 🚧 Troubleshooting

### Backend won't start
- ✅ Check Python version: \`python --version\` (should be 3.11+)
- ✅ Verify all dependencies installed: \`pip list\`
- ✅ Confirm .env file exists with API keys
- ✅ Test Pinecone connection: check API key is valid

### No recommendations returned
- ✅ Run model training notebook first to populate Pinecone
- ✅ Verify Pinecone index "furniture-recommender" exists
- ✅ Check backend logs for errors
- ✅ Ensure dataset loaded correctly

### Frontend errors
- ✅ Verify backend is running on port 8000
- ✅ Check browser console for CORS errors
- ✅ Clear browser cache and reload
- ✅ Verify Node.js version: \`node --version\` (should be 20+)

### Analytics page empty
- ✅ Confirm backend /analytics/ endpoint is accessible
- ✅ Check if dataset loaded in backend startup logs
- ✅ Verify Google Drive dataset URL is accessible

## 📝 Environment Variables Reference

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| \`PINECONE_API_KEY\` | Pinecone API key from pinecone.io | Yes | \`pcsk_abc123...\` |
| \`PINECONE_ENVIRONMENT\` | Pinecone cloud region | Yes | \`us-east-1\` |
| \`GOOGLE_API_KEY\` | Google Gemini API key | Yes | \`AIza...\` |

## 🎯 Future Enhancements

Potential improvements for next phase:
- **Computer Vision**: Image-based product classification and visual similarity search
- **Conversation History**: Multi-turn context-aware recommendations
- **Advanced NLP**: Query understanding and intent classification
- **A/B Testing**: Model performance evaluation framework
- **Batch Processing**: Large-scale embedding updates

## 📄 License

This project is created for educational purposes as part of an ML engineering assignment.

## 🙏 Acknowledgments

- **Dataset**: Furniture product catalog from provided Google Drive link
- **Embeddings**: sentence-transformers library by UKP Lab
- **Vector DB**: Pinecone for managed vector search
- **GenAI**: Google Gemini Pro for creative descriptions
- **UI Components**: shadcn/ui for beautiful React components

---

**Built with ❤️ for the AI/ML Internship Assignment**
