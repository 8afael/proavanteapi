from re import search

from fastapi import FastAPI
import models
from database import engine
from brapi import Brapi
from populateDb import dataSearch

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

ticker = 'PETR4'
database = 'proavante.db'

searchData = dataSearch(ticker, database)
getActualValue = searchData.loadData()
searchData.saveJsonToClass()
searchData.saveToDB()

