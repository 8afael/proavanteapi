import requests
import json
from pprintpp import pprint 

class AuthBase:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_auth(self):
        # This method can be overridden or extended in child classes if needed
        raise NotImplementedError("Subclasses should implement this method.")

class QuandlAuth(AuthBase):
    def get_auth(self):
        # Implement specific authorization details
        # For instance, if using API key as a query parameter
        return {'api_key': self.api_key}

class Brapi:
    def __init__(self, ticker):
        self.data = self.loadJson(ticker)

    def loadJson(self, ticker):
        key = '19551e80c49c486b2e0cc25ef58e291d'
        url = f'https://api.marketstack.com/v1/eod?access_key={key}&symbols={ticker}&limit=1'
        #print(url)
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            pprint(data)
            return data
        else:
            print(f"Error code: {response.status_code}")

    def getActualPrice(self):
        try:
            data = self.loadJson(self.data)
            closeValue = self.search(['data'])
            #closeValue = data['data']
            print(closeValue)
            return closeValue
        except KeyError as e:
            print(e)

    def search(self, subkeys):
        self.search_results = []

        def _search_recursive(data, current_key=""):
            if isinstance(data, dict):
                for key, value in data.items():
                    new_key = current_key + "/" + key if current_key else key
                    if new_key in subkeys:
                        self.search_results.append(value)
                    _search_recursive(value, new_key)
            elif isinstance(data, list):
                for item in data:
                    _search_recursive(item, current_key)

        _search_recursive(self.data)

    def getSearchResults(self):
        return self.search_results

    def buscar_patrimonio(self, ticker):
        ticker = 'PETR3'

        #base_url = f"https://brapi.dev/api/quote/{ticker}?token={token}"

        params = {
            #'range': '1y',
            #'interval': '1mo',
            'fundamental': 'true',
            'dividends': 'true',
            'modules': 'incomeStatementHistoryQuarterly defaultKeyStatistics',
            'modules': 'balanceSheetHistory',
            'token': 'f3S9CVBqGnpWkmNHyuyY9G',
        }

        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            print("Conectado, buscando informações..")
            pprint(data)
            return data
        else:
            print("Erro ao obter dados")
            return None

        print("result" + data)

        patrimonio_liquido = data['patrimonio_liquido']
        ativos_totais = data['ativos_totais']
        passivos_totais = data['passivos_totais']

        df = pd.DataFrame({'Patrimônio Líquido': [patrimonio_liquido],
                        'Ativos Totais': [ativos_totais],
                        'Passivos Totais': [passivos_totais]})

        print(df)
        return df
    
    def execute(self, ticker):
        ticker = 'PETR3'
        print(self.buscar_patrimonio(ticker))


    
# Exemplo de uso

# Visualização
# plt.plot(df_petr4.index, df_petr4['Patrimônio Líquido'])
# plt.show()

# # Exemplo de uso
# df_petr4 = buscar_patrimonio('PETR4')
# print(df_petr4)

# # Visualização
