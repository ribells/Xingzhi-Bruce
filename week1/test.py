import http.client

conn = http.client.HTTPSConnection("stock-ticker-security-and-company-search-database.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "4fdf7b0e21msh4e17b550c54d8d8p17665cjsn0d5ee1f96b6e",
    'X-RapidAPI-Host': "stock-ticker-security-and-company-search-database.p.rapidapi.com"
    }

conn.request("GET", "/all_search?ticker=AAPL", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
