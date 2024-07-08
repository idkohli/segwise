import json
import logging
from fastapi import FastAPI, Depends, HTTPException, status, Query
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from sql_app.database import get_db, engine
from utils import download_csv, parse_csv
from sql_app.models import GameData, Base
from fastapi.security import HTTPBasic, HTTPBasicCredentials


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Application startup initializes the db.
Base.metadata.create_all(bind=engine)


security = HTTPBasic()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/upload")
def upload_csv(
    file_url: str,
    credentials: HTTPBasicCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    # Baisc auth
    if credentials.username != "admin" or credentials.password != "password":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    csv_file = download_csv(file_url)
    parse_csv(csv_file, db)
    return {"status": "success", "message": "CSV data uploaded successfully"}


@app.get("/query")
def query_data(
    filters: str = Query({}),
    credentials: HTTPBasicCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    # Basic auth
    if credentials.username != "admin" or credentials.password != "password":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    query = db.query(GameData)

    # Convert json str into a useable dictionary
    filters_dict = json.loads(filters)

    # Goes through each filter item and updates db query.
    for field, value in filters_dict.items():
        if hasattr(GameData, field):
            # Query all games that exactly match the filter value.
            if field in [
                "AppID",
                "RequiredAge",
                "Price",
                "DLCCount",
                "Windows",
                "Mac",
                "Linux",
                "Positive",
                "Negative",
                "ScoreRank",
                "ReleaseDate",
            ]:
                query = query.filter(getattr(GameData, field) == value)
            
            # Query all games that support the language filtered by.
            elif field == "SupportedLanguages":
                query = query.filter(GameData.SupportedLanguages.contains(value))

            # Query all games that have a substring of the filter value.
            else:
                query = query.filter(getattr(GameData, field).like(f"%{value}%"))

    results = query.all()
    return results


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
