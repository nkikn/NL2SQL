from langchain.chains import LLMChain
from langchain_huggingface import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from requests import Session
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
import os
import re
from huggingface_hub import login
from langchain_core.runnables import RunnableSequence
import time
from functools import lru_cache

from sqlalchemy import text
from backend.db.database import SessionLocal


# def execute_sql_query(sql: str):
#     db = SessionLocal()
#     try:
#         result = db.execute(text(sql))
#         rows = result.fetchall()
#         columns = result.keys()
#         return [dict(zip(columns, row)) for row in rows]
#     finally:
#         db.close()

def execute_sql_query(sql: str, db: Session):
    result = db.execute(text(sql))
    rows = result.fetchall()
    columns = result.keys()
    return [dict(zip(columns, row)) for row in rows]


def generate_and_execute_sql(schema: str, question: str, db: Session):
    sql = generate_sql(schema, question)
    cleaned_sql = extract_sql_block(sql)
    # results = execute_sql_query(db, cleaned_sql)
    results = execute_sql_query(sql=cleaned_sql, db=db)
    return {
        "sql": cleaned_sql,
        "results": results
    }

def load_gemma_llm():
    model_id = os.getenv("MODEL_ID", "google/gemma-3-1b-it")  # fallback default
    token = os.getenv("HUGGINGFACE_HUB_TOKEN")

    if not token:
        raise EnvironmentError("HUGGINGFACE_HUB_TOKEN not set in environment.")

    start = time.time()
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_id, token=token)
    print(f"Tokenizer loaded in {time.time() - start:.2f}s")

    start = time.time()
    print("Loading model...")
    model = AutoModelForCausalLM.from_pretrained(model_id, token=token)
    print(f"Model loaded in {time.time() - start:.2f}s")

    device = 0 if torch.cuda.is_available() else -1
    text_gen_pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        device=device,
        max_new_tokens=256,
        do_sample=True,
        temperature=0.3,
        top_k=50,
        top_p=0.95
    )

    return HuggingFacePipeline(pipeline=text_gen_pipeline)

@lru_cache(maxsize=1)
def load_gemma_llm_cached():
    return load_gemma_llm()

def get_sql_chain():
    llm = load_gemma_llm_cached()
    prompt = PromptTemplate(
        input_variables=["schema", "question"],
        template=(
            "Given this PostgreSQL schema:\n{schema}\n\n"
            "Write a SQL query to answer this question:\n{question}"
        ),
    )
    return prompt | llm  # This is the new recommended syntax

def generate_sql(schema: str, question: str) -> str:
    chain = get_sql_chain()
    return chain.invoke({"schema": schema, "question": question})


def extract_sql_block(text: str) -> str:
    """
    Extract SQL query from the LLM response.
    Prioritizes code block, falls back to SELECT-like statement or full response.
    """
    # First, try to extract from ```sql ... ``` block
    match = re.search(r"```sql\s*(.*?)\s*```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip().replace("\n", " ")

    # Fallback: search for first SELECT statement
    fallback = re.search(r"(SELECT\s.*?;)", text, re.IGNORECASE | re.DOTALL)
    if fallback:
        return fallback.group(1).strip().replace("\n", " ")

    # Final fallback: use full text, cleaned
    return text.strip().replace("\n", " ")

