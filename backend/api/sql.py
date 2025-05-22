from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.models.pydantic import SQLRequest, SQLResponse
from backend.services.sql_generator import generate_sql, extract_sql_block
from backend.db.database import get_db

from fastapi import APIRouter, HTTPException
from backend.services.sql_generator import generate_sql  # your existing LLM-based generator
from backend.services.sql_generator import execute_sql_query

from backend.models.pydantic import NaturalLanguageQuery

router = APIRouter()

# @router.post("/query")
# def query_db(natural_language: str):
#     sql = generate_sql(natural_language)
#     try:
#         rows = execute_sql_query(sql)
#         return {"sql": sql, "result": rows}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

@router.post("/query")
def query_db(request: NaturalLanguageQuery, db: Session = Depends(get_db)):
    print("Received request:", request)
    full_sql = generate_sql(request.db_schema, request.question)
    print("Generated raw SQL:", full_sql)
    sql = extract_sql_block(full_sql)
    print("Cleaned SQL:", sql)
    try:
        rows = execute_sql_query(sql=sql, db=db)
        print("Query results:", rows)
        return {"sql": sql, "result": rows}
    except Exception as e:
        print("SQL execution error:", str(e))
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/generate-sql", response_model=SQLResponse)
def generate_sql_only(request: SQLRequest):
    """Generate SQL query from a natural language question without executing."""
    full_response = generate_sql(request.db_schema, request.question)
    sql = extract_sql_block(full_response)
    # print(full_response)
    return {"sql": sql}

@router.get("/test")
def check(db: Session = Depends(get_db)):
    """Health check for database connection."""
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

# @router.post("/generate-and-run")
# def generate_and_run_sql(request: SQLRequest, db: Session = Depends(get_db)):
#     """Generate SQL from question and run it on the database."""
#     full_response = generate_sql(request.db_schema, request.question)
#     sql = extract_sql_block(full_response)
#
#     try:
#         result = db.execute(text(sql)).fetchall()
#         return {
#             "sql": sql,
#             "result": [dict(row._mapping) for row in result]
#         }
#     except Exception as e:
#         return {
#             "sql": sql,
#             "error": str(e)
#         }

