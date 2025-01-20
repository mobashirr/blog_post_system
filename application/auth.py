
'''
AUTH class modu
'''

from application.utils import session_manger
import secrets

class AUTH:
    '''
    Authoraization logic provide two methods to make authoraization or to check for users authoraization
    '''
    @staticmethod
    def isauthorized(token):
        '''
        check if a given token is authorized by checking if its exist in the session
        @token: token that we need to authorize.
        Return: user_id if the token is valid otherwise None.
        '''
        if not token:
            return False

        redis_key = f'AUTH_{token}';
        user_id = session_manger.get_value(redis_key);
        return user_id;
    
    @staticmethod
    def authorize(user):
        '''
        create a valid token and save it in the session
        @user_id: user id
        Return valid token or None if not authorized
        '''
        # generate random token
        token = secrets.token_hex(32);
        user_id = user.id
        redis_key = f'AUTH_{token}';
        # add the token into the session database
        try:
            session_manger.set_key_val(redis_key,user_id);
        except Exception as e:
            print(e)
        return token
