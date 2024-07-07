import csv
import requests
import ast
from io import StringIO
from sqlalchemy.orm import Session
from app.sql_app.models import GameData
from app.sql_app.schemas import GameDataCreate


def get_google_sheet_csv_url(sheet_url: str) -> str:
    # Extract the sheet ID from the Google Sheets URL
    if "docs.google.com/spreadsheets" in sheet_url:
        sheet_id = sheet_url.split("/d/")[1].split("/")[0]
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        return csv_url
    return sheet_url

def convert_row_to_game_data(row: dict) -> GameDataCreate:
    # Convert the row data to appropriate types
    return GameDataCreate(
        AppID=int(row['AppID']),
        Name=row['Name'],
        ReleaseDate=row['Release date'],
        RequiredAge=int(row['Required age']) if row['Required age'] else None,
        Price=float(row['Price']) if row['Price'] else None,
        DLCCount=int(row['DLC count']) if row['DLC count'] else None,
        AboutTheGame=row['About the game'],
        SupportedLanguages=ast.literal_eval(row['Supported languages']),
        Windows=row['Windows'],
        Mac=row['Mac'],
        Linux=row['Linux'],
        Positive=int(row['Positive']) if row['Positive'] else None,
        Negative=int(row['Negative']) if row['Negative'] else None,
        ScoreRank=int(row['Score rank']) if row['Score rank'] else None,
        Developers=row['Developers'],
        Publishers=row['Publishers'],
        Categories=row['Categories'],
        Genres=row['Genres'],
        Tags=row['Tags']
    )

def download_csv(url: str):
    csv_url = get_google_sheet_csv_url(url)
    response = requests.get(csv_url)
    response.raise_for_status()
    return StringIO(response.text)

def parse_csv(csv_file, db: Session):
    reader = csv.DictReader(csv_file)

    for row in reader:
        game_data = convert_row_to_game_data(row)

        # Ensures that a particular game is added only once. Identified by its AppID.
        app_id = game_data.AppID
        game_exists = db.query(GameData).filter(GameData.AppID == app_id).first()
        if game_exists:
            continue

        db_game_data = GameData(**game_data.model_dump())
        db.add(db_game_data)
    db.commit()
