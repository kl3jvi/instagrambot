from InstagramAPI import InstagramAPI
import time

def ask_for_info():

    username = input('INSTAGRAM USERNAME: ')
    password = input('INSTAGRAM PASSWORD: ')
    num_to_follow = input('How many people should we follow per day? ')
    tags_to_use = [input('What tag should I use? (No #) ')]
    while True:
        more = input('Any more? (Y/N) ')
        if more == 'n'or'N':
            break
        tags_to_use.append(more)

    # This does not validate the username or password, so make sure you enter in the right one!

    return {
            'username': username,
            'password': password,
            'num_to_follow': int(num_to_follow),
            'tags_to_use': tags_to_use
        }

def login(username, password):
     api = InstagramAPI(username, password)
     api.login()
     return api


def find_targets(api, tag):
    """
    Search for users who have posted a picture with tag, and return a list of user IDs.
    """

    ok = api.tagFeed(tag) # Automatically prints an error
    if not ok:
        raise Exception # Error the script

    resp = api.LastJson
    images = resp['items']

    users = []
    for image in images:
        users.append(
            # We use .get so we can filter out invalid data.
            # Invalid data is rare, but in this case we are prepared
            # pk is ID
            image.get('user', {}).get('pk', '')
        )

    # a list of users from the list of users which id isn't an empty string
    return [u for u in users if u != '']


def follow_all(api, targets, time_to_wait):
    total_targets = len(targets)
    num = 0
    for t in targets:

        ok = api.follow(t)
        if not ok:
            print('Error while trying to follow ID: %s', t)

        num += 1
        print('Followed %d/%d' % (num, total_targets))
        time.sleep(time_to_wait)



if __name__ == '__main__':
    answers = ask_for_info()
    print('Thanks!')

    username = answers['username']
    password = answers['password']
    num_to_follow = answers['num_to_follow']
    tags_to_use = answers['tags_to_use']

    api = login(username, password)

    targets = []

for tag in tags_to_use:
        targets += find_targets(api, tag)
print('%d Targets Acquired!' % len(targets))
secs_in_a_day = 86400
time_to_wait = secs_in_a_day / num_to_follow
print('Beginning to follow!', 'Make sure you keep an eye on your following count.')
follow_all(api, targets, time_to_wait)
print('All Done!')
