import vk
import getpass
import logging

APP_ID = 6277574  # чтобы получить app_id, нужно зарегистрировать своё приложение на https://vk.com/dev


def get_user_login():
    return getpass.getpass(prompt='Username:\n\t')


def get_user_password():
    return getpass.getpass(prompt='Password:\n\t')


def get_online_friends(login, password):
    session = vk.AuthSession(
        app_id=APP_ID,
        user_login=login,
        user_password=password,
        scope=2
    )
    session.get_access_token()
    api = vk.API(session, v='5.69', lang='ru')
    ids_of_friends_online = api.friends.getOnline()
    friends_online = api.users.get(user_ids=ids_of_friends_online)
    return friends_online


def output_friends_to_console(friends_online):
    if not friends_online:
        print('You have no friends online')
    else:
        print('You have {} friends online:'.format(len(friends_online)))
        for index, friend in enumerate(friends_online, 1):
            msg = '{}. {} {} is online'.format(index,
                                               friend['last_name'],
                                               friend['first_name'])
            print(msg)


def mute_vk_logger():
    logger = logging.getLogger('vk')
    logger.disabled = True


if __name__ == '__main__':
    mute_vk_logger()
    authentification_success = False
    while not authentification_success:
        login = get_user_login()
        password = get_user_password()
        try:
            friends_online = get_online_friends(login, password)
        except vk.exceptions.VkAuthError:
            print('Invalid login or password.\nTry again!\n')
        else:
            authentification_success = True
            output_friends_to_console(friends_online)
