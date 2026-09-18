import hashlib, argparse, json
from urllib.parse import urlparse #To check for valid URLS
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--shorten',help='Shortens provided URL',nargs='?') #nargs = '?' allows the argument to be blank without throwing an exception.

def CheckValidity(url):
    try:
        result = urlparse(url)
        print(result.netloc)

        if result.scheme not in ('https', 'http'):
            return False
        
        if not result.netloc:
            return False

        return True
    except:
        return False
    
args = parser.parse_args()
print(args)
if args.shorten is None:
    print('error: No URL provided')
else:
    validity = CheckValidity(args.shorten)
    if validity == False:
        print("error: Invalid URL")