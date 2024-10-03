#imports 
import os


class Config:
    #postgresql://username:password@host:port/database_name
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/test')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
