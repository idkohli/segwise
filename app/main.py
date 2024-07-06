from fastapi import FastAPI, Depends, HTTPException, status
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from app.sql_app.database import get_db, engine
from app.utils import download_csv, parse_csv
from app.sql_app.models import GameData, Base
from fastapi.security import HTTPBasic, HTTPBasicCredentials


# Application startup
@asynccontextmanager
async def lifespan(application: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

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
    # Auth
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
    credentials: HTTPBasicCredentials = Depends(security),
    db: Session = Depends(get_db),
    **filters,
):
    # Auth
    if credentials.username != "admin" or credentials.password != "password":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    query = db.query(GameData)

    for field, value in filters.items():
        # TODO: See if anything else needs to be done for date.
        if hasattr(GameData, field):
            if field in [
                "AppID",
                "RequiredAge",
                "Price",
                "DLCCount",
                "Positive",
                "Negative",
                "ScoreRank",
                "ReleaseDate"
            ]:
                query = query.filter(getattr(GameData, field) == value)
            else:
                query = query.filter(getattr(GameData, field).like(f"%{value}%"))

    results = query.all()
    return results


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000
    )