import hashlib, argparse, json
from urllib.parse import urlparse #To check for valid URLS
parser = argparse.ArgumentParser(description='URL Shortener')

parser.add_argument('-s', '--shorten',help='Shortens provided URL',nargs='?') #nargs = '?' allows the argument to be blank without throwing an exception.

def CheckValidity(url):
    try:
        result = urlparse(url)

        if result.scheme not in ('https', 'http'):
            return False
        
        if not result.netloc:
            return False

        return True
    
    except:
        return False

def ShortenURL(url):
    h = hashlib.new('md5') #It generates the shortest hash(though it's not as secure as other algorithms)
    h.update(url.encode())
    url_hash = h.hexdigest()
    
    data = {url:url_hash}
    
    with open('data.json','a') as f:
        json.dump(data,f)
    
args = parser.parse_args()
print(args)

if args.shorten is None:
    print('error: No URL provided')

else:
    validity = CheckValidity(args.shorten)

    if validity == False:
        print("error: Invalid URL")

    else:
        ShortenURL(args.shorten)
