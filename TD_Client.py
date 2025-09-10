import requests

class TD_Client:
    def __init__(self, access_token, account_id, consumer_key, first_token_info):
        self.access_token = access_token
        self.account_id = account_id
        self.consumer_key = consumer_key
        self.first_token_info = first_token_info

    def get_account(self, new_access_token):
        header = {"authorization": f"Bearer {new_access_token}"}
        account_endpoint = f'https://api.tdameritrade.com/v1/accounts/{self.account_id}'
        account_payload = {"fields":"positions,orders"}
        account_res = requests.get(url = account_endpoint, params = account_payload, headers= header)
        return account_res

    def get_refreshed_access_token(self):
        url = "https://api.tdameritrade.com/v1/oauth2/token"
        header = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = {"grant_type":"refresh_token",
                "refresh_token": self.first_token_info["refresh_token"],
                "client_id": self.consumer_key
                }
        response = requests.post(url, headers= header, data= payload)
        refreshed_access_token_info = response.json()
        return refreshed_access_token_info["access_token"]

    
    def get_qty_all_out(self, ticker, get_account_res):
        account_info = get_account_res.json()
        positions_list = []
        for i in range(len(account_info["securitiesAccount"]["positions"])):
            position = account_info["securitiesAccount"]["positions"][i]["instrument"]["symbol"]
            positions_list.append(position.upper())
        position_index = positions_list.index(ticker)
        quantity = account_info["securitiesAccount"]["positions"][position_index]["longQuantity"]
        return quantity

            
    def place_option_order(self, new_access_token, orderType, price, instruction, symbol, quantity):
        header = {"authorization": f"Bearer {new_access_token}", "Content-Type": "application/json"}
        endpoint = f'https://api.tdameritrade.com/v1/accounts/{self.account_id}/orders'
        single_option_payload = {
                              "complexOrderStrategyType": "NONE",
                              "orderType": orderType, #'MARKET' or 'LIMIT' or 'STOP' or 'STOP_LIMIT' or 'TRAILING_STOP' or 'MARKET_ON_CLOSE' or 'EXERCISE' or 'TRAILING_STOP_LIMIT' or 'NET_DEBIT' or 'NET_CREDIT' or 'NET_ZERO'
                              "session": "NORMAL",
                              "price": price,
                              "duration": "DAY",
                              "orderStrategyType": "SINGLE",
                              "orderLegCollection": [
                                {
                                  "instruction": instruction, #BUY_TO_OPEN OR BUY_TO_CLOSE OR SELL_TO_OPEN OR SELL_TO_CLOSE
                                  "quantity": quantity,
                                  "instrument": {
                                    "symbol": symbol, # AMC_021221C24
                                    "assetType": "OPTION"
                                    }
                                }
                              ]
                            }
        res = requests.post(url= endpoint, json= single_option_payload, headers= header)
        return res
    
    def get_netliq(self, get_account_res):
        account_info = get_account_res.json()
        net_liq = account_info["securitiesAccount"]["currentBalances"]["liquidationValue"]
        return net_liq

    def get_quote(self, symbol, new_access_token):
        endpoint = f"https://api.tdameritrade.com/v1/marketdata/{symbol}/quotes"
        header = {"authorization": f"Bearer {new_access_token}"}
        response = requests.get(url = endpoint, headers= header)
        return response
