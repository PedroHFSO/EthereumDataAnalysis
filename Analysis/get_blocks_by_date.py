from datetime import datetime
import requests
from datetime import timezone

day_start = int(input('Insert starting day:\n'))
month_start = int(input('Insert starting month:\n'))
year_start = int(input('Insert starting year:\n'))

day_end = int(input('Insert end day:\n'))
month_end = int(input('Insert end month:\n'))
year_end = int(input('Insert end year:\n'))

start_date = datetime(year_start, month_start, day_start)
end_date = datetime(year_end, month_end, day_end)

start_timestamp = int(start_date.replace(tzinfo=timezone.utc).timestamp())
end_timestamp = int(end_date.replace(tzinfo=timezone.utc).timestamp())

api_key = 'DH1IHX1N6XZD5STWKPM9SFV5WJCF9PXMGD'
start_url = 'https://api.etherscan.io/api?module=block&action=getblocknobytime&timestamp='+str(start_timestamp)+'&closest=after&apikey='+api_key

end_url = 'https://api.etherscan.io/api?module=block&action=getblocknobytime&timestamp='+str(end_timestamp)+'&closest=before&apikey='+api_key


print('Start collection at: '+requests.get(start_url).json()['result'])
print('End collection at: '+requests.get(end_url).json()['result'])

