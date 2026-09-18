import hashlib, argparse, json
from urllib.parse import urlparse #To check for valid URLS

parser = argparse.ArgumentParser(description='URL Shortener')
subparsers = parser.add_subparsers(dest='command', required=True)

parser_shorten = subparsers.add_parser('shorten', help = 'shortens a URL')
parser_shorten.add_argument('URL', help = 'URL to be shortened', nargs = "?") #nargs='?' allows us to pass 0 arguments to this command without getting an error.
parser_shorten.add_argument('--alias', help = 'provide an alias(optional)', default= None)

parser_resolve = subparsers.add_parser('resolve', help='resolves code back into URL')
parser_resolve.add_argument('code', help='Code to be resolved back into a URL')

parser_list = subparsers.add_parser('list', help='shows all generated URL-code pairs')

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
                print(url, '==>', data[url]['code'])
                return data[url]['code']

            else:
                val = {}
                if alias is None: 
                    h = hashlib.new('SHAKE-256') #This algo allows us to generate variable length hashes.
                    h.update(url.encode())
                    url_hash = h.hexdigest(5)
                    val['code'] = url_hash
                    val['count'] = 0
                    data[url] = val
                
                else:
                    data[url]['code'] = alias

                with open('data.json','w') as f:
                    json.dump(data,f)
            
                print('-'*15,'URL shortened successfully','-'*15)
                print(url, '==>', data[url]['code'])
                return data[url]['code']
            
def ResolveCode(args):
    code = args.code
    data = {}

    try:
        with open('data.json', 'r') as f:
            data = json.load(f)

            found = False
            for value in data.values():
                print(value)
                if code in value.values():
                    found = True
                    break
                else:
                    found = False
            
            if found == False:
                print('error: The given code is invalid')
                return
            
            else:
                url = None
                for key in data.keys():
                    if data[key]['code'] == code:
                        data[key]['count']+=1
                        url = key

                        with open('data.json','w') as f:
                            json.dump(data,f)

                        break

                print('-'*9,'The code has been resolved into the URL','-'*9) 
                print(code, '==>', url)
                print(f'This Code has been resolved {data[url]['count']} times')
                return url
    
    except FileNotFoundError:
        print("error: The given file doesn't exist")
    
    except:
        print('Unexpected Error')

def ShowList():
    try:
        data = {}
        with open('data.json', 'r') as f:
            data = json.load(f)

            print('-'*15,'List of shortened URLs','-'*15)
            i = 1

            for key, value in data.items():
                print(f'{i}. ',key,'===>',value['code'])
                print(f'(It has been resolved {value['count']} times)')
                print()
                i += 1

    except FileNotFoundError:
        print("No URls have been shortened yet.")
        return
    
args = parser.parse_args()

if args.command == 'shorten':
    ShortenURL(args)

if args.command == 'resolve':
    ResolveCode(args)

if args.command == 'list':
    ShowList()