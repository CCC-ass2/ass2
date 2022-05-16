import requests
r = requests.get('http://localhost:8000/page3data')

if __name__ == '__main__':
    print(r.json())