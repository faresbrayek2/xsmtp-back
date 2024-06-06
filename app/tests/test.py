import requests
from bs4 import BeautifulSoup

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
    'cache-control': 'max-age=0',
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': 'CHECKPAGERANK_SESSION=q854ngk5qv7neph0da78rbqbh2; _gid=GA1.2.1312182781.1717627913; _ga_2GGEZX1072=GS1.1.1717660446.2.0.1717660446.0.0.0; _ga=GA1.2.2099698396.1717627912; _gat_gtag_UA_654337_1=1',
    'origin': 'https://checkpagerank.net',
    'priority': 'u=0, i',
    'referer': 'https://checkpagerank.net/',
    '^sec-ch-ua': '^\\^Google',
    'sec-ch-ua-mobile': '?0',
    '^sec-ch-ua-platform': '^\\^Windows^\\^^',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
}

data = {
  'name': 'https://checkpagerank.net/'
}

response = requests.post('https://checkpagerank.net/check-page-rank.php', headers=headers, data=data)

soup = BeautifulSoup(response.text, 'html.parser')

# Extracting the metrics
metrics = {}
for font in soup.find_all('font'):
    text = font.get_text(separator='\n').strip()
    for line in text.split('\n'):
        key_value = line.split(': ')
        if len(key_value) == 2:
            key, value = key_value
            metrics[key.strip()] = value.strip()

# Print the extracted metrics
for key, value in metrics.items():
    print(f"{key}: {value}")
