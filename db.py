import sqlalchemy


class BD:
    def __init__(self):
        self.connection = sqlalchemy.create_engine('postgresql://kurshakov:12345@localhost:5432/vkinder').connect()

    def insert_info_bd(self, user_id, result_dict):
        sel = self.connection.execute(f'''
        SELECT vk_id FROM vk_users
        WHERE vk_id = '{user_id}'
        ''').fetchall()
        if len(sel) == 0:
            self.connection.execute(f'''
            INSERT  INTO vk_users (vk_id,vk_age,vk_sex,vk_city,vk_relation)
            VALUES ({user_id},{result_dict.get('age')},{result_dict.get('sex')},{result_dict.get('city')},{result_dict.get('relation')})
            ''')
            return 1  # Заполнение произошло
        return 0  # Заполнение не произошло

    def update_param(self, user_id, param, data):
        param = 'vk_' + param
        self.connection.execute(f'''
        UPDATE vk_users SET {param}='{data}'
        WHERE vk_id = {user_id}
        ''')

    def check_param_bd(self, user_id, param):
        param = 'vk_' + param
        sel = self.connection.execute(f'''
            SELECT {param} FROM vk_users
            WHERE vk_id = '{user_id}'
            ''').fetchall()
        if sel[0][0] == 0 or sel[0][0] == '0':
            return 0  # Поле незаполнено
        return 1  # Поле заполнено

    def get_param_bd(self, user_id, param):
        param = 'vk_' + param
        sel = self.connection.execute(f'''
            SELECT {param} FROM vk_users
            WHERE vk_id = '{user_id}'
            ''').fetchall()
        return sel[0][0]

    def check_all_params(self, user_id):
        data = ['age', 'sex', 'city', 'relation']
        for param in data:
            if self.check_param_bd(user_id, param) == 0:
                return 0
        return 1

    def insert_search(self, user_id, search_id):
        self.connection.execute(f'''
            INSERT  INTO vk_search (vk_id_user,vk_id_search)
            VALUES ({user_id},{search_id})
            ''')
