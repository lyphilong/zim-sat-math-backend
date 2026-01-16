"""
FastAPI Backend for SAT Math Problem Solver
Root entrypoint for Vercel deployment
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import schemas
from api.backend.services.schemas import (
    SATMathSolutionOutput,
    SATEnglishSolutionOutput,
)

# Create FastAPI app instance
app = FastAPI(
    title="SAT Math Solver API",
    description="API for solving SAT Math & SAT English problems using LLM",
    version="1.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS middleware để frontend có thể gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for local/Vercel deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProblemRequest(BaseModel):
  problem: Optional[str] = None
  image_base64: Optional[str] = None
  image_mime_type: Optional[str] = None


class EnglishProblemRequest(BaseModel):
  problem: str


@app.get("/")
async def root():
    """Root endpoint - API status"""
    return {"message": "SAT Math & English Solver API", "status": "running"}


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/solve", response_model=SATMathSolutionOutput)
async def solve_problem(request: ProblemRequest):
    """
    Solve SAT Math problem using LLM (text and/or image).
    """
    # Validate that at least problem text or image is provided
    if not request.problem and not request.image_base64:
        raise HTTPException(
            status_code=400,
            detail="Either problem text or image must be provided",
        )

    try:
        from api.backend.services.llm_service import solve_sat_problem

        solution = await solve_sat_problem(
            problem=request.problem,
            image_base64=request.image_base64,
            image_mime_type=request.image_mime_type,
        )
        return solution
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error solving SAT Math problem: {str(e)}",
        )


@app.post("/solve-english", response_model=SATEnglishSolutionOutput)
async def solve_english_problem(request: EnglishProblemRequest):
    """
    Solve SAT English problem using LLM (text-only).
    """
    if not request.problem:
        raise HTTPException(
            status_code=400,
            detail="Problem text must be provided for SAT English",
        )

    try:
        from api.backend.services.llm_service import solve_sat_english_problem

        solution = await solve_sat_english_problem(problem=request.problem)
        return solution
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error solving SAT English problem: {str(e)}",
        )

