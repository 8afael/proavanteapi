import json
import sqlite3
from sys import modules
import requests
from pprintpp import pprint

class allInfo:
    def __init__(self, ticker, company, actualValue, patrimonioLiquido, lucroLiquido, acoesEmitidas, precoTeto, dividendo1ano, dividendo2ano, dividendo3ano, dividendo4ano, dividendo5ano):
        self.ticker = ticker
        self.company = company
        self.actualValue = actualValue
        self.patrimonioLiquido = patrimonioLiquido
        self.lucroLiquido = lucroLiquido
        self.acoesEmitidas = acoesEmitidas
        self.precoTeto = precoTeto
        self.dividendo1Ano = dividendo1ano
        self.dividendo2Ano = dividendo2ano
        self.dividendo3Ano = dividendo3ano
        self.dividendo4Ano = dividendo4ano
        self.dividendo5Ano = dividendo5ano

class dataSearch:
    def __init__(self, ticker, database):
        self.dataDetails = []
        self.ticker = ticker
        self.database = database
        self.conn = sqlite3.connect(database)
        self.cursor = self.conn.cursor()
        self.data = self.loadData()

    def loadData(self):
        token = 'f3S9CVBqGnpWkmNHyuyY9G'
        params = {
            'modules':'incomeStatementHistory,defaultKeyStatistics',
            'token':'f3S9CVBqGnpWkmNHyuyY9G',
            'range':'1y'
        }
        #urlBrapi = f'https://brapi.dev/api/quote/{self.ticker}?token={token}'
        urlBalance = f'https://brapi.dev/api/quote/{self.ticker}'
        #print(urlBalance)
        response = requests.get(urlBalance, params=params)
        if response.status_code == 200:
            data = response.json()
            #pprint(data)
            return data
        else:
            print(f"Error code: {response.status_code}")

    def search(self, subkeys):
        #self.searchDataResults = []
        #self.searchValueResults = []
        self.searchResults = []

        def _search_recursive(data, current_key=""):
            if isinstance(data, dict):
                for key, value in data.items():
                    new_key = current_key + "/" + key if current_key else key
                    if new_key in subkeys:
                        self.searchResults.append(value)
                    _search_recursive(value, new_key)
            elif isinstance(data, list):
                for item in data:
                    _search_recursive(item, current_key)

        _search_recursive(self.data)

    def getSearchResults(self):
        return self.searchResults

    def calcActualValue(self):
        searcher = dataSearch(self.ticker, "proavante.db")
        searcher.search([f"results/regularMarketPreviousClose"])
        resultActualValue = searcher.getSearchResults()
        actualvalue = resultActualValue[0]
        self.actualValue = str(actualvalue)
        return self.actualValue

    def saveJsonToClass(self):
        searcher = dataSearch(self.ticker, "proavante.db")
        self.patrimonioLiquido = 376040000000
        self.lucroLiquido = 511994000
        self.acoesEmitidas = 13044496930
        self.dividendo1Ano = 5.022
        self.dividendo2Ano = 7.344
        self.dividendo3Ano = 16.778
        self.dividendo4Ano = 5.653
        self.dividendo5Ano = 0.000
        self.precoTeto = self.calcPrecoTeto()
        self.actualValue = self.calcActualValue()

        searcher.search([f"results/symbol"])
        resultSymbol = searcher.getSearchResults()
        symbol = resultSymbol[0]
        self.ticker = str(symbol)

        searcher.search([f"results/shortName"])
        resultCompany = searcher.getSearchResults()
        company = resultCompany[0]
        self.company = str(company)

        allInfoClass = allInfo(self.ticker, self.company, self.actualValue, self.patrimonioLiquido, self.lucroLiquido, self.acoesEmitidas, self.precoTeto, self.dividendo1Ano, self.dividendo2Ano, self.dividendo3Ano, self.dividendo4Ano, self.dividendo5Ano)
        #pprint(allInfoClass)
        return allInfoClass

    def calcPrecoTeto(self):
        self.dividendoMedio = (self.dividendo1Ano+self.dividendo2Ano+self.dividendo3Ano+self.dividendo4Ano+self.dividendo5Ano)/5
        self.lucro = 0.08
        self.precoTeto = self.dividendoMedio/self.lucro
        pprint(f'Div medio 5 anos: {self.dividendoMedio}')
        pprint(f'Percentual Lucro: {self.lucro}')
        pprint(f'Preço Teto: {self.precoTeto}')
        return self.precoTeto

    def createDic(self):
        data = [
            {"ticker":self.ticker,
             "company":self.company,
             "actualValue":self.actualValue,
             "patrimonioLiquido":self.patrimonioLiquido,
             "lucroLiquido":self.lucroLiquido,
             "acoesEmitidas":self.acoesEmitidas,
             "precoTeto":self.precoTeto,
             "dividendo1Ano":self.dividendo1Ano,
             "dividendo2Ano": self.dividendo2Ano,
             "dividendo3Ano": self.dividendo3Ano,
             "dividendo4Ano": self.dividendo4Ano,
             "dividendo5Ano": self.dividendo5Ano,
             }
        ]
        return data

    def saveToDB(self):
        savedData = self.createDic()
        for item in savedData:
            print(item)
        try:
            for item in savedData:
                ticker = item["ticker"]
                company = item["company"]
                actualValue = item["actualValue"]
                patrimonioLiquido = item["patrimonioLiquido"]
                lucroLiquido = item["lucroLiquido"]
                acoesEmitidas = item["acoesEmitidas"]
                precoTeto = item["precoTeto"]
                dividendo1Ano = item["dividendo1Ano"]
                dividendo2Ano = item["dividendo2Ano"]
                dividendo3Ano = item["dividendo3Ano"]
                dividendo4Ano = item["dividendo4Ano"]
                dividendo5Ano = item["dividendo5Ano"]
                values_to_insert = (ticker, company, actualValue, patrimonioLiquido, lucroLiquido, acoesEmitidas, precoTeto, dividendo1Ano, dividendo2Ano, dividendo3Ano, dividendo4Ano, dividendo5Ano)
                query = "INSERT INTO dashboard (ticker, company, actualValue, patrimonioLiquido, lucroLiquido, acoesEmitidas, precoTeto, dividendo1Ano, dividendo2Ano, dividendo3Ano, dividendo4Ano, dividendo5Ano) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                self.cursor.execute(query, values_to_insert)
            self.conn.commit()
            print("Data saved to database successfully!")
        except sqlite3.Error as e:
            print(f"Error saving data to database: {e}")
        finally:
            self.conn.close()
