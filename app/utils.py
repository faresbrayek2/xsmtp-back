import platform
import re
import subprocess
from bs4 import BeautifulSoup
import tldextract
import requests
import nmap
import socket


def extract_tld(url: str) -> str:
    """
    Extracts the TLD (top-level domain) from the given URL.
    
    Args:
        url (str): The URL from which to extract the TLD.
    
    Returns:
        str: The extracted TLD.
    """
    extracted = tldextract.extract(url)
    return f".{extracted.suffix}"

def check_ssl(url: str) -> bool:
    """
    Checks if the given URL has SSL enabled.

    Args:
        url (str): The URL to check for SSL.

    Returns:
        bool: True if SSL is enabled, False otherwise.
    """
    if not url.startswith('http'):
        url = 'https://' + url  # Ensure the URL is prefixed with https
    try:
        response = requests.get(url, timeout=10)
        # If the request was successful and used HTTPS, SSL is enabled
        return response.url.startswith('https')
    except requests.exceptions.SSLError:
        return False
    except requests.exceptions.RequestException as e:
        # Handle other request exceptions if necessary
        return False
    
def lookup_ip(url) -> str:
    """
    Looks up the IP address of the given URL and returns the country code.
    """
    url = url.split('/')[2]
    if ':' in url:
        url = url.split(':')[0]
    ip = socket.gethostbyname(url)
    url = f"https://geo.proxyspace.pro/ip/{ip}"
    response = requests.get(url, timeout=10)
    data = response.json()
    if 'ip' in data:
        country_code = data.get('country_code')
        return country_code
    else:
        return "Unknown"
    
def get_hosting(url: str) -> str:
    """
    Determines the hosting provider of the given URL.
    """
    url = url.split('/')[2]
    if ':' in url:
        url = url.split(':')[0]
    ip = socket.gethostbyname(url)
    url = f"https://geo.proxyspace.pro/ip/{ip}"
    response = requests.get(url, timeout=10)
    data = response.json()
    if data:
        asn_organization = data.get('asn_organization')
        return asn_organization
    else:
        return "Unknown"
    
def get_os_info() -> str:
    """
    Retrieves the operating system information.

    Returns:
        str: The operating system information.
    """
    try:
        os_info = platform.system()
        if os_info == 'Windows':
            os_version = platform.version()
            return f"{os_info} {os_version}"
        else:
            uname = subprocess.check_output('uname -a', shell=True).decode('utf-8').strip()
            return uname
    except subprocess.CalledProcessError as e:
        return f"Error retrieving OS info: {e}"

def get_php_version() -> str:
    """
    Retrieves the PHP version.

    Returns:
        str: The PHP version.
    """
    try:
        php_version_output = subprocess.check_output('php -v', shell=True).decode('utf-8').strip()
        match = re.search(r'PHP (\d+\.\d+\.\d+)', php_version_output)
        if match:
            return match.group(1)
        else:
            return "Unknown PHP version"
    except subprocess.CalledProcessError as e:
        return f"Error retrieving PHP version: {e}"

def get_host_info(url: str) -> str:
    """
    Retrieves the host information including OS and PHP version.

    Args:
        url (str): The URL to get the host information for.

    Returns:
        str: The host information including OS and PHP version.
    """
    os_info = get_os_info()
    php_version = get_php_version()
    return f"{os_info} - PHP {php_version}"

def get_seo_data(url: str) -> dict:
    """
    Retrieves the SEO information including Domain Authority (DA) of the given URL.

    Args:
        url (str): The URL to get the SEO information for.

    Returns:
        dict: A dictionary containing the SEO information and Domain Authority.
    """
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
        'name': url
    }

    seo_data = {
        'seo_rank_da': 0,
        'seo_info': {}
    }

    try:
        with requests.Session() as session:
            response = session.post('https://checkpagerank.net/check-page-rank.php', headers=headers, data=data, timeout=60)
            soup = BeautifulSoup(response.text, 'html.parser')
            for font in soup.find_all('font'):
                text = font.get_text(separator='\n').strip()
                for line in text.split('\n'):
                    key_value = line.split(': ')
                    if len(key_value) == 2:
                        key, value = key_value
                        if key.strip() == "Domain Authority":
                            seo_data['seo_rank_da'] = int(value.strip())
                        else:
                            seo_data['seo_info'][key.strip()] = value.strip()
        return seo_data
    except requests.RequestException as e:
        print(f"Error retrieving SEO data for {url}: {e}")
        return seo_data
