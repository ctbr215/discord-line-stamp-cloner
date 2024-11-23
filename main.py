import requests
from bs4 import BeautifulSoup
import re
from io import BytesIO
import tls_client
from requests_toolbelt import MultipartEncoder
import random
import string

session = tls_client.Session(

    client_identifier="chrome112",

    random_tls_extension_order=True

)
def keisan(number):
    return True if number % 5 == 0 else False

def create_server(headers, stamp_name, count):
    json_data = {
        'name': stamp_name + str(count),
        'icon': None,
        'channels': [],
        'system_channel_id': None,
        'guild_template_code': '2TffvPucqHkN',
    }
    response = session.post('https://discord.com/api/v9/guilds', headers=headers, json=json_data)
    server_id = response.json()['id']
    json_data = {
        'validate': None,
        'max_age': 604800,
        'max_uses': 0,
        'target_type': None,
        'temporary': False,
    }
    json_data = {
        'type': 0,
        'name': 'a',
        'permission_overwrites': [],
    }
    response = session.post(
        f'https://discord.com/api/v9/guilds/{server_id}/channels',
        headers=headers,
        json=json_data,
    )
    channel_id = response.json()['id']
    response = session.post(
        f'https://discord.com/api/v9/channels/{channel_id}/invites',
        headers=headers,
        json=json_data,
    )
    return {"id": server_id, "code": response.json()['code']}
        
print('line stamp cloner')
user_input = input("1: Userモード\n2: Botモード\n")

if user_input == '1':
    mode = 'user'
    token = input('token: ')
elif user_input == '2':
    mode = 'bot'
    print('作ってないです')
else:
    print('無効な入力です')

headers = {
    "Authorization": token,
    "Content-Type": "application/json",
    "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDIwIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDUiLCJvc19hcmNoIjoieDY0IiwiYXBwX2FyY2giOiJpYTMyIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIGRpc2NvcmQvMS4wLjkwMjAgQ2hyb21lLzEwOC4wLjUzNTkuMjE1IEVsZWN0cm9uLzIyLjMuMjYgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjIyLjMuMjYiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyNDAyMzcsIm5hdGl2ZV9idWlsZF9udW1iZXIiOjM4NTE3LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsLCJkZXNpZ25faWQiOjB9",
    }

stamp_url = input('ラインスタンプのurlを入力してください: ')
response = requests.get(stamp_url)
soup = BeautifulSoup(response.text, 'html.parser')
sticker_name = soup.find('p', class_='mdCMN38Item01Ttl').text
sticker_author = soup.find('a', class_='mdCMN38Item01Author').text
sticker_description = soup.find('p', class_='mdCMN38Item01Txt').text
sticker_ids = []
li_elements = soup.find_all('li', class_='mdCMN09Li')
for li in li_elements:
    data_preview = li.get('data-preview')
    if data_preview:
        match = re.search(r'"id"\s*:\s*"(\d+)"', data_preview)
        if match:
            sticker_id = match.group(1)
            sticker_ids.append(sticker_id)

print(sticker_name, '\n', sticker_author, '\n', sticker_description, '\n', "スタンプ数: " + str(len(sticker_ids)))
counter = 1
sticker_counter = 1
sticker_add_counter = 1
now_server_id = None
for sticker_id in sticker_ids:
    if counter==6: 
        counter = 1
    if counter==1:
        result = create_server(headers, sticker_name, sticker_counter)
        now_server_id = result['id']
        print('discord.gg/' + result['code'])
        sticker_counter += 1
    response = requests.get(f"https://stickershop.line-scdn.net/stickershop/v1/sticker/{sticker_id}/android/sticker.png")
    image_data = BytesIO(response.content)
    filename = "sticker.png"

    data = {
        'name': (None, sticker_name + ' ' + str(sticker_add_counter)),
        'tags': (None, '😀'),
        'description': (None, ''),
        'file': (filename, image_data, "image/png"),
    }
    boundary = '----WebKitFormBoundary' + ''.join(random.sample(string.ascii_letters + string.digits, 16))
    multipart = MultipartEncoder(fields=data, boundary=boundary)

    sticker_headers = {
        "Authorization": token,
        "Content-Type": multipart.content_type,
        "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDIwIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDUiLCJvc19hcmNoIjoieDY0IiwiYXBwX2FyY2giOiJpYTMyIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIGRpc2NvcmQvMS4wLjkwMjAgQ2hyb21lLzEwOC4wLjUzNTkuMjE1IEVsZWN0cm9uLzIyLjMuMjYgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjIyLjMuMjYiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyNDAyMzcsIm5hdGl2ZV9idWlsZF9udW1iZXIiOjM4NTE3LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsLCJkZXNpZ25faWQiOjB9",
    }
    
    response = requests.post(
        f'https://discord.com/api/v9/guilds/{now_server_id}/stickers',
        headers=sticker_headers,
        data=multipart
    )
    print(sticker_name + ' ' + str(sticker_add_counter), '完了')
    sticker_add_counter += 1
    counter += 1

