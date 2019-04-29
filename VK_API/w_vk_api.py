import urllib.request
import json
from datetime import datetime

access_token = "8e217ecf8e217ecf8e217ecfe98e4b45e288"
"e218e217ecfd2e5d359c66802c91b712275"
group = 'spb.live'
version = '5.92'
offsets = [0, 100]


def getPosts():
    all_posts = []
    for off in offsets:
        request = urllib.request.Request(
            'https://api.vk.com/method/wall.get?domain=%s&offset=%s&count='
            '100&v=%s&access_token=%s'
            % (group, off, version, access_token)
        )

        response = urllib.request.urlopen(request)
        result = response.read().decode('utf-8')

        data = json.loads(result)['response']['items']
        all_posts = all_posts + data
    return all_posts


def getComments(post_id, owner_id):
    comments = []
    for off in offsets:
        id = post_id
        request = urllib.request.Request(
            'https://api.vk.com/method/wall.getComments?owner_id=%s&post_id=%s'
            '&offset=%s&count=100&v=%s&access_token=%s'
            % (owner_id, id, off, version, access_token)
        )
        response = urllib.request.urlopen(request)
        result = response.read().decode('utf-8')
        data = json.loads(result)['response']['items']
        comments = comments + data
    return comments


def getUserInfo(user_id):
    user = {'sex': 'Unknown', 'age': 'Unknown', 'city': 'Unknown'}
    request = urllib.request.Request(
        'https://api.vk.com/method/users.get?v=%s&access_token=%s&user_ids=%s'
        '&fields=sex,bdate,home_town'
        % (version, access_token, user_id)
    )
    response = urllib.request.urlopen(request)
    result = response.read().decode('utf-8')
    if json.loads(result).get('response') is not None:
        data = json.loads(result)['response'][0]

        # 0 - not selected, 1 - female, 2 - male
        user['sex'] = 'Unknown' if data['sex'] == 0 else (
            'Female' if data['sex'] == 1 else 'Male')
        bdate = 'Unknown'
        htown = 'Unknown'

        if data.get('bdate') is not None:
            sdate = data['bdate']

            try:
                utc = datetime.strptime(sdate, '%d.%m.%Y')
                now = datetime.now()
                delta = now - utc
                bdate = '%s years' % (delta.days // 365)
            except ValueError:
                bdate = 'Unknown'

        if data.get('home_town') is not None and data.get('home_town') != '':
            htown = data['home_town']

        user['age'] = bdate
        user['city'] = htown

    return user
