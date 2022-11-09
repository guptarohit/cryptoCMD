from cryptocmd.utils import get_url_data


def get_trending_cryptos_json():
    api_url = 'https://web-api.coinmarketcap.com/v1/cryptocurrency/trending/latest'

    try:
        json_data = get_url_data(api_url).json()
        error_code = json_data["status"]["error_code"]
        if error_code == 0:
            return json_data["data"]
        else:
            raise Exception(json_data["status"]["error_message"])
    except Exception as e:
        print("Error fetching trending cryptos {}", error_code)

        if hasattr(e, "message"):
            print("Error message:", e.message)
        else:
            print("Error message:", e)
