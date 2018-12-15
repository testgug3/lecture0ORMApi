import requests

def main():
    base = input("First Currency: ")
    other = input("Seconde Currency: ")
    res = requests.get("http://api.fixer.io/lates",
    params = {"base": base, "symbols": other})
    if res.status_code != 200:
        raise Exception("Error: API request unsucessful.")
    data = res.json()
    rate = data["rates"][other]
    print(f"1 {base} is equal to {rate} {other}")

if __name__ == "__main__":
    main()