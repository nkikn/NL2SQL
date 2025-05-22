from pydantic import BaseModel

class SQLRequest(BaseModel):
    db_schema: str
    question: str

class SQLResponse(BaseModel):
    sql: str

class NaturalLanguageQuery(BaseModel):
    db_schema: str
    question: str
