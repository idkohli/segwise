from sqlalchemy import JSON, Column, Integer, String, Float
from sql_app.database import Base


class GameData(Base):
    __tablename__ = 'game_data'

    id = Column(Integer, primary_key=True, index=True)
    AppID = Column(Integer, unique=True, index=True)
    Name = Column(String)
    ReleaseDate = Column(String)
    RequiredAge = Column(Integer)
    Price = Column(Float)
    DLCCount = Column(Integer)
    AboutTheGame = Column(String)
    SupportedLanguages = Column(JSON)
    Windows = Column(String)
    Mac = Column(String)
    Linux = Column(String)
    Positive = Column(Integer)
    Negative = Column(Integer)
    ScoreRank = Column(Integer)
    Developers = Column(String)
    Publishers = Column(String)
    Categories = Column(String)
    Genres = Column(String)
    Tags = Column(String)
