from config_data.config import SiteSettings
from site_API.utils.site_api_headlers import SiteApiInterface

site = SiteSettings()

headers = {"accept": "application/json", "X-API-KEY": site.api_key.get_secret_value()}

url = site.host_api.get_secret_value()

site_api = SiteApiInterface()

if __name__ == "__main__":
    site_api()
