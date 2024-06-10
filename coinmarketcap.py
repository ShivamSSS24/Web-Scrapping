import requests
from bs4 import BeautifulSoup

class CoinMarketCap:
    def __init__(self):
        self.base_url = "https://coinmarketcap.com"

    def scrape_coin(self, coin_name):
        url = f"{self.base_url}/currencies/{coin_name.lower()}"
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        price = soup.find('div', class_='priceValue').text.strip()
        price_change = soup.find('span', class_='priceChange').text.strip()
        market_cap = soup.find('div', class_='cmc-details-panel-item--market-cap').find('div', class_='cmc-details-panel-value').text.strip()
        market_cap_rank = soup.find('div', class_='cmc-details-panel-item--market-cap').find('div', class_='cmc-details-panel-value').find('span').text.strip()
        volume = soup.find('div', class_='cmc-details-panel-item--volume').find('div', class_='cmc-details-panel-value').text.strip()
        volume_rank = soup.find('div', class_='cmc-details-panel-item--volume').find('div', class_='cmc-details-panel-value').find('span').text.strip()
        volume_change = soup.find('div', class_='cmc-details-panel-item--volume').find('div', class_='cmc-details-panel-value').find('span', class_='priceChange').text.strip()
        circulating_supply = soup.find('div', class_='cmc-details-panel-item--circulating-supply').find('div', class_='cmc-details-panel-value').text.strip()
        total_supply = soup.find('div', class_='cmc-details-panel-item--total-supply').find('div', class_='cmc-details-panel-value').text.strip()
        diluted_market_cap = soup.find('div', class_='cmc-details-panel-item--fully-diluted-market-cap').find('div', class_='cmc-details-panel-value').text.strip()

        contracts = soup.find('div', class_='cmc-details-panel-item--contracts').find_all('div', class_='cmc-details-panel-value')
        contract_data = []
        for contract in contracts:
            name = contract.find('span').text.strip()
            address = contract.find('a').text.strip()
            contract_data.append({"name": name, "address": address})

        official_links = soup.find('div', class_='cmc-details-panel-item--official-links').find_all('div', class_='cmc-details-panel-value')
        official_link_data = []
        for link in official_links:
            name = link.find('span').text.strip()
            link = link.find('a').get('href')
            official_link_data.append({"name": name, "link": link})

        socials = soup.find('div', class_='cmc-details-panel-item--social').find_all('div', class_='cmc-details-panel-value')
        social_data = []
        for social in socials:
            name = social.find('span').text.strip()
            link = social.find('a').get('href')
            social_data.append({"name": name, "url": link})

        data = {
            "price": price,
            "price_change": price_change,
            "market_cap": market_cap,
            "market_cap_rank": market_cap_rank,
            "volume": volume,
            "volume_rank": volume_rank,
            "volume_change": volume_change,
            "circulating_supply": circulating_supply,
            "total_supply": total_supply,
            "diluted_market_cap": diluted_market_cap,
            "contracts": contract_data,
            "official_links": official_link_data,
            "socials": social_data
        }
        return data
