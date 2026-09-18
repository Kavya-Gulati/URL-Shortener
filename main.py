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
            data = {}
            try:
                with open('data.json','r') as f:
                    data = json.load(f)

            except:
                data = {}

            if url in data.keys():
                print('-'*5,'This URL has already been shortened and stored.','-'*5) 
                print(url, '==>', data[url])
                return data[url]

            else:
                if alias is None: 
                    h = hashlib.new('SHAKE-256') #This algo allows us to generate variable length hashes.
                    h.update(url.encode())
                    url_hash = h.hexdigest(5)
                    data[url] = url_hash
                
                else:
                    data[url] = alias

                with open('data.json','w') as f:
                    json.dump(data,f)
            
                print('-'*15,'URL shortened successfully','-'*15)
                print(url, '==>', data[url])
                return data[url]
            
    
    
args = parser.parse_args()
print(args)

if args.command == 'shorten':
    ShortenURL(args)