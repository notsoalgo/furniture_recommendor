import pathlib
"""
FastAPI Backend for AI-Powered Furniture Recommendation System

This backend provides two main endpoints:
1. POST /recommend/ - Accepts user queries and returns AI-generated product recommendations
2. GET /analytics/ - Returns statistical analytics about the product dataset

Tech Stack:
- FastAPI: Modern, fast web framework
- Sentence Transformers: Text embeddings (all-MiniLM-L6-v2)
- Pinecone: Vector database for similarity search
- LangChain + Google Gemini: Creative product description generation
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv
import pandas as pd

# ML and AI imports
try:
    from sentence_transformers import SentenceTransformer
    from pinecone import Pinecone
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain.prompts import PromptTemplate
except ImportError as e:
    print(f"Warning: Some ML libraries not installed: {e}")
    print("Please install: pip install sentence-transformers pinecone langchain-google-genai")

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Furniture Recommendation API",
    description="AI-powered furniture recommendation and analytics system",
    version="1.0.0"
)

# Configure CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for ML models (initialized on startup)
embedding_model = None
pinecone_index = None
gemini_model = None
dataset = None

# Pydantic models for request/response validation
class RecommendationRequest(BaseModel):
    query: str
    top_k: Optional[int] = 8

class Product(BaseModel):
    uniq_id: str
    title: str
    price: float
    brand: str
    images: Optional[str] = None
    creative_description: str
    similarity_score: float

class RecommendationResponse(BaseModel):
    query: str
    products: List[Product]
    count: int

class AnalyticsResponse(BaseModel):
    total_products: int
    top_brands: Dict[str, int]
    top_categories: Dict[str, int]
    price_stats: Dict[str, float]


@app.on_event("startup")
async def startup_event():
    """
    Initialize ML models and connections on server startup.
    This runs once when the FastAPI server starts.
    """
    global embedding_model, pinecone_index, gemini_model, dataset
    
    print("=" * 80)
    print("Starting Furniture Recommendation API...")
    print("=" * 80)
    
    # 1. Load sentence transformer model for embeddings
    try:
        print("\n[1/4] Loading sentence transformer model...")
        embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        print("✓ Embedding model loaded (dimension: 384)")
    except Exception as e:
        print(f"✗ Error loading embedding model: {e}")
    
    # 2. Connect to Pinecone vector database
    try:
        print("\n[2/4] Connecting to Pinecone...")
        PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
        
        if not PINECONE_API_KEY:
            print("⚠️  PINECONE_API_KEY not found in environment variables")
            print("   Set PINECONE_API_KEY to enable recommendations")
        else:
            pc = Pinecone(api_key=PINECONE_API_KEY)
            pinecone_index = pc.Index("furniture-recommender")
            
            # Verify connection
            stats = pinecone_index.describe_index_stats()
            print(f"✓ Connected to Pinecone (vectors: {stats.total_vector_count:,})")
    except Exception as e:
        print(f"✗ Error connecting to Pinecone: {e}")
    
    # 3. Initialize Google Gemini model for creative descriptions
    try:
        print("\n[3/4] Initializing Google Gemini AI...")
        GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
        
        if not GOOGLE_API_KEY:
            print("⚠️  GOOGLE_API_KEY not found in environment variables")
            print("   Set GOOGLE_API_KEY to enable AI descriptions")
        else:
            gemini_model = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=GOOGLE_API_KEY,
                temperature=0.7,
                max_tokens=150
            )
            print("✓ Gemini AI initialized")
    except Exception as e:
        print(f"✗ Error initializing Gemini: {e}")
    
# 4. Load dataset for analytics
try:
    print("\n[4/4] Loading dataset for analytics...")
   script_dir = pathlib.Path(__file__).parent.resolve()
        dataset_path = script_dir / "furniture_dataset.csv"
        dataset = pd.read_csv(dataset_path)
        print(f"✓ Dataset loaded ({len(dataset):,} products)")
    except Exception as e:
        print(f"✗ Error loading dataset: {e}")



   print("\n" + "=" * 80)
print("✅ API Server Ready!")
print("=" * 80 + "\n")
       
    

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "Furniture Recommendation API is running",
        "version": "1.0.0",
        "status": "healthy",
        "endpoints": {
            "recommendations": "POST /recommend/",
            "analytics": "GET /analytics/"
        }
    }


@app.post("/recommend/", response_model=RecommendationResponse)
async def recommend_products(request: RecommendationRequest):
    """
    Generate furniture recommendations based on user query.
    
    Process:
    1. Embed user query using sentence-transformers
    2. Search Pinecone for similar products
    3. Generate creative descriptions using Gemini AI
    4. Return top-k products with metadata
    
    Args:
        request: RecommendationRequest with query text and optional top_k
    
    Returns:
        RecommendationResponse with recommended products and AI descriptions
    """
    
    # Validate models are loaded
    if embedding_model is None:
        raise HTTPException(
            status_code=503,
            detail="Embedding model not initialized. Check server logs."
        )
    
    if pinecone_index is None:
        raise HTTPException(
            status_code=503,
            detail="Pinecone connection not established. Check PINECONE_API_KEY."
        )
    
    try:
        # Step 1: Generate embedding for user query
        query_embedding = embedding_model.encode(
            [request.query],
            normalize_embeddings=True
        )[0]
        
        # Step 2: Search Pinecone for similar products
        search_results = pinecone_index.query(
            vector=query_embedding.tolist(),
            top_k=request.top_k,
            include_metadata=True
        )
        
        if not search_results.matches:
            return RecommendationResponse(
                query=request.query,
                products=[],
                count=0
            )
        
        # Step 3: Generate creative descriptions using Gemini AI
        products = []
        
        for match in search_results.matches:
            metadata = match.metadata
            
            # Generate creative description
            creative_desc = await generate_creative_description(
                title=metadata.get('title', ''),
                brand=metadata.get('brand', ''),
                price=metadata.get('price', 0)
            )
            
            # Create product object
            product = Product(
                uniq_id=metadata.get('uniq_id', ''),
                title=metadata.get('title', 'Untitled Product'),
                price=float(metadata.get('price', 0)),
                brand=metadata.get('brand', 'Unknown'),
                images=metadata.get('images'),
                creative_description=creative_desc,
                similarity_score=float(match.score)
            )
            
            products.append(product)
        
        return RecommendationResponse(
            query=request.query,
            products=products,
            count=len(products)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating recommendations: {str(e)}"
        )


async def generate_creative_description(title: str, brand: str, price: float) -> str:
    """
    Generate a creative, marketing-style product description using Gemini AI.
    
    If Gemini is not available, returns a simple fallback description.
    
    Args:
        title: Product title
        brand: Product brand
        price: Product price
    
    Returns:
        Creative product description (1-2 sentences)
    """
    
    if gemini_model is None:
        # Fallback description if Gemini not available
        return f"Discover the {title} by {brand}, expertly crafted to enhance your living space with style and functionality."
    
    try:
        # Create prompt for Gemini
        prompt_template = PromptTemplate(
            input_variables=["title", "brand", "price"],
            template="""You are a creative furniture marketing expert. Write a compelling, concise product description (2-3 sentences max) for this furniture item. Focus on benefits, style, and emotional appeal. Be enthusiastic but professional.

Product: {title}
Brand: {brand}
Price: ${price}

Creative Description:"""
        )
        
        prompt = prompt_template.format(
            title=title,
            brand=brand,
            price=f"{price:.2f}"
        )
        
        # Generate description
        response = gemini_model.invoke(prompt)
        description = response.content.strip()
        
        # Limit length
        if len(description) > 300:
            description = description[:297] + "..."
        
        return description
    
    except Exception as e:
        print(f"Error generating creative description: {e}")
        # Fallback
        return f"Elevate your space with the {title} from {brand}. Quality craftsmanship meets modern design at an exceptional value."


@app.get("/analytics/", response_model=AnalyticsResponse)
async def get_analytics():
    """
    Get statistical analytics about the furniture product dataset.
    
    Returns:
        AnalyticsResponse with:
        - Total product count
        - Top 10 brands by product count
        - Top 10 categories by product count
        - Price statistics (min, max, mean, median)
    """
    
    if dataset is None:
        raise HTTPException(
            status_code=503,
            detail="Dataset not loaded. Check server logs."
        )
    
    try:
        # Calculate top brands
        top_brands = dataset['brand'].value_counts().head(10).to_dict()
        
        # Calculate top categories
        if 'categories' in dataset.columns:
            top_categories = dataset['categories'].value_counts().head(10).to_dict()
        else:
            top_categories = {}
        
        # Calculate price statistics
        price_stats = {
            "min": float(dataset['price'].min()),
            "max": float(dataset['price'].max()),
            "mean": float(dataset['price'].mean()),
            "median": float(dataset['price'].median()),
            "std": float(dataset['price'].std())
        }
        
        return AnalyticsResponse(
            total_products=len(dataset),
            top_brands=top_brands,
            top_categories=top_categories,
            price_stats=price_stats
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating analytics: {str(e)}"
        )


# Additional utility endpoints

@app.get("/health")
async def health_check():
    """
    Detailed health check showing status of all services.
    """
    return {
        "status": "healthy",
        "services": {
            "embedding_model": embedding_model is not None,
            "pinecone": pinecone_index is not None,
            "gemini_ai": gemini_model is not None,
            "dataset": dataset is not None
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "=" * 80)
    print("Starting FastAPI Server")
    print("=" * 80)
    print("\nServer will be available at:")
    print("  - Local: http://localhost:8000")
    print("  - Docs: http://localhost:8000/docs")
    print("  - ReDoc: http://localhost:8000/redoc")
    print("\n" + "=" * 80 + "\n")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
