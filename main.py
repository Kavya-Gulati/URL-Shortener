import hashlib, argparse, json
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--shorten',help='Shortens provided URL')

args = parser.parse_args()
print(args)
print(type(args.shorten))
if args.shorten is not None:
    print('testing true')