from pydantic import BaseModel
from typing import Optional

class GameDataCreate(BaseModel):
    AppID: int
    Name: str
    ReleaseDate: Optional[str] = None
    RequiredAge: Optional[int] = None
    Price: Optional[float] = None
    DLCCount: Optional[int] = None
    AboutTheGame: Optional[str] = None
    SupportedLanguages: Optional[str] = None
    Windows: Optional[str] = None
    Mac: Optional[str] = None
    Linux: Optional[str] = None
    Positive: Optional[int] = None
    Negative: Optional[int] = None
    ScoreRank: Optional[int] = None
    Developers: Optional[str] = None
    Publishers: Optional[str] = None
    Categories: Optional[str] = None
    Genres: Optional[str] = None
    Tags: Optional[str] = None
