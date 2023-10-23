"""
╔══════════════════════════════════════════════════════════════════════════╗
║                  FastAPI Application for Document Retrieval              ║
║  Efficiently query and manipulate documents in a datastore using API     ║
╟──────────────────────────────────────────────────────────────────────────╢
║ Script Name    : main.py                                                 ║
║ Description    : Manage CRUD operations on documents in a datastore      ║
║ Author         : [V.S./Ax2]                                              ║
║ Version        : 1.0.0                                                   ║
║ License        : MIT License                                             ║
╟──────────────────────────────────────────────────────────────────────────╢
║ Please ensure all API requests are authenticated to protect data         ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

#// region [ rgba(0, 100, 250, 0.03)] OpenAI and Weaviate Settings

#* ==============================================
#*                IMPORTS SECTION
#* ==============================================
import uvicorn
from typing import Optional
from fastapi import FastAPI, File, Form, HTTPException, Body, UploadFile
from fastapi.staticfiles import StaticFiles
from loguru import logger

# Internal dependencies
from models.api import DeleteRequest, DeleteResponse, QueryRequest, QueryResponse, UpsertRequest, UpsertResponse
from datastore.factory import get_datastore
from services.file import get_document_from_file
from models.models import DocumentMetadata, Source
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import asyncpg
import asyncio

#* ==============================================
#*             APP CONFIGURATION
#* ==============================================

app = FastAPI()
app.mount("/.well-known", StaticFiles(directory=".well-known"), name="static")

#* Sub-application Configuration
sub_app = FastAPI(
    title="Retrieval Plugin API",
    description="API for querying and filtering documents using natural language queries and metadata",
    version="1.0.0",
    servers=[{"url": "http://localhost:8080"}],
)
app.mount("/sub", sub_app)

#// endregion

#// region [ rgba(0, 250, 100, 0.03)] Default User Settings

#* ==============================================
#*               STREAMLIT MODELS 
#* ==============================================
# Pydantic model for User data validation
class User(BaseModel):
    name: str
    email: str

#// endregion

#// region [ rgba(0, 150, 100, 0.03)] Default User Settings

#* ==============================================
#*               FUNCTIONS
#* ==============================================
# Asynchronous function to create a connection to the PostgreSQL
async def create_conn():
    conn = await asyncpg.connect(
        user='xgpt',
        password='xgpt',
        database='xgpt',
        host='127.0.0.1'
    )
    return conn

#// endregion

#// region [ rgba(0, 250, 500, 0.03)] Default User Settings

#* ==============================================
#*               STARTUP EVENT
#* ==============================================

@app.on_event("startup")
async def startup():
    global datastore
    datastore = await get_datastore()  # Establishing datastore connection

#// endregion

#// region [ rgba(50, 200, 150, 0.03)] Milvus Settings
#* ==============================================
#*         MIVLUS API ROUTES (VectorDB)
#* ==============================================

@app.post("/upsert-file", response_model=UpsertResponse)
async def upsert_file(file: UploadFile = File(...), metadata: Optional[str] = Form(None)):
    #? Parse metadata or use default
    try:
        metadata_obj = DocumentMetadata.parse_raw(metadata) if metadata else DocumentMetadata(source=Source.file)
    except Exception as e:
        logger.warning(f"Metadata parse error: {str(e)}")
        metadata_obj = DocumentMetadata(source=Source.file)

    document = await get_document_from_file(file, metadata_obj)

    #? Upsert document and handle possible errors
    try:
        ids = await datastore.upsert([document])
        return UpsertResponse(ids=ids)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/upsert", response_model=UpsertResponse)
async def upsert(request: UpsertRequest = Body(...)):
    try:
        ids = await datastore.upsert(request.documents)
        return UpsertResponse(ids=ids)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Service Error")


@app.post("/query", response_model=QueryResponse)
async def query_main(request: QueryRequest = Body(...)):
    try:
        results = await datastore.query(request.queries)
        return QueryResponse(results=results)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Service Error")


@sub_app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest = Body(...)):
    try:
        results = await datastore.query(request.queries)
        return QueryResponse(results=results)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Service Error")


@app.delete("/delete", response_model=DeleteResponse)
async def delete(request: DeleteRequest = Body(...)):
    #? Ensure at least one deletion criterion is provided
    if not (request.ids or request.filter or request.delete_all):
        raise HTTPException(status_code=400, detail="One of ids, filter, or delete_all is required")
    
    #? Attempt deletion and handle possible errors
    try:
        deleted_count = await datastore.delete(ids=request.ids, filter=request.filter, delete_all=request.delete_all)
        return DeleteResponse(deleted=deleted_count)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Service Error")

#// endregion

#// region [ rgba(0, 250, 0, 0.03)] Default User Settings

#* ==============================================
#*       STREAMLIT API ROUTES (Frontend)
#* ==============================================

@app.post("/create_user/")
async def create_user(user: User):
    conn = await create_conn()
    try:
        await conn.execute('''
            INSERT INTO users(name, email) VALUES($1, $2)
        ''', user.name, user.email)
    finally:
        await conn.close()
    return {"detail": "User created successfully"}


@app.get("/get_users/", response_model=List[User])
async def get_users():
    conn = await create_conn()
    try:
        users = await conn.fetch('SELECT name, email FROM users')
    finally:
        await conn.close()
    return [{"name": user["name"], "email": user["email"]} for user in users]

#// endregion

#// region [ rgba(0, 250, 0, 0.03)] Default User Settings

#* ==============================================
#*                 MAIN ROUTINE
#* ==============================================


def start():
    uvicorn.run("server.main:app", host="0.0.0.0", port=8777, reload=True)
#// endregion

