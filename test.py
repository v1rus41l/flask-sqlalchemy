from requests import get, post, delete

# print(get('http://localhost:5000/api/v2/users').json())
#
# print(get('http://localhost:5000/api/v2/users/1').json())
#
# print(get('http://localhost:5000/api/v2/users/999').json())
# # при условии, что пользователя с id = 999 нет в базе
#
# print(get('http://localhost:5000/api/v2/users/q').json())

# корректный запрос
print(post('http://localhost:5000/api/v2/users',
           json={'name': 'Scott',
                 'about': 'want to be a programmer',
                 'email': 'test@mail.ru'}).json())

# # некорректный: пустой запрос
# print(post('http://localhost:5000/api/v2/users').json())

# # некорректный: передан только тимлид
# print(post('http://localhost:5000/api/v2/users',
#            json={'team_leader': 'Scott Jerard'}).json())
#
# # некорректный: переданы лишние данные
# print(post('http://localhost:5000/api/v2/users',
#            json={'title': 'Mission 1',
#                  'team_leader': 'Scott Jerard',
#                  'job': 'deployment of residential modules 1 and 2',
#                  'collaborators': '1, 2',
#                  'work_size': 5}).json())