from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.models import SQLRequest, SQLResponse
from backend.services.sql_generator import generate_sql, extract_sql_block
from backend.db.database import get_db

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.services.sql_generator import generate_and_execute_sql
from backend.models import SQLRequest, SQLResponse

router = APIRouter()

@router.post("/execute-sql", response_model=SQLResponse)
def execute_sql(
    request: SQLRequest,
    db: Session = Depends(get_db)
):
    """Generate SQL from question and execute it on the database."""
    try:
        result = generate_and_execute_sql(
            request.db_schema,
            request.question,
            db
        )
        return {
            "sql": result["sql"],
            "results": result["results"]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/test")
def check(db: Session = Depends(get_db)):
    """Health check for database connection."""
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


@router.post("/generate-sql", response_model=SQLResponse)
def generate_sql_only(request: SQLRequest):
    """Generate SQL query from a natural language question without executing."""
    full_response = generate_sql(request.db_schema, request.question)
    sql = extract_sql_block(full_response)
    # print(full_response)
    return {"sql": sql}


@router.post("/generate-and-run")
def generate_and_run_sql(request: SQLRequest, db: Session = Depends(get_db)):
    """Generate SQL from question and run it on the database."""
    full_response = generate_sql(request.db_schema, request.question)
    sql = extract_sql_block(full_response)

    try:
        result = db.execute(text(sql)).fetchall()
        return {
            "sql": sql,
            "result": [dict(row._mapping) for row in result]
        }
    except Exception as e:
        return {
            "sql": sql,
            "error": str(e)
        }

