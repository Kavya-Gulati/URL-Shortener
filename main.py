import hashlib, argparse, json
from urllib.parse import urlparse #To check for valid URLS

parser = argparse.ArgumentParser(description='URL Shortener')
subparsers = parser.add_subparsers(dest='command', required=True)

parser_shorten = subparsers.add_parser('shorten', help = 'shortens a URL')
parser_shorten.add_argument('URL', help = 'URL to be shortened', nargs = "?")
parser_shorten.add_argument('--alias', help = 'provide an alias(optional)', default= None)

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

def ShortenURL(args):
    url = args.URL
    alias = args.alias

    if url is None:
        print('error: No URL provided')
        return

    else:
        validity = CheckValidity(url)

        if validity == False:
            print("error: Invalid URL")
            return

        else:
            print('Valid URL')

            data = {}
            try:
                with open('data.json','r') as f:
                    data = json.load(f)

            except:
                data = {}

            if alias is None: 
                h = hashlib.new('md5') #It generates the shortest hash(though it's not as secure as other algorithms)
                h.update(url.encode())
                url_hash = h.hexdigest()
                data[url] = url_hash
            
            else:
                data[url] = alias

            with open('data.json','w') as f:
                json.dump(data,f)
            
    
    
args = parser.parse_args()
print(args)

if args.command == 'shorten':
    ShortenURL(args)