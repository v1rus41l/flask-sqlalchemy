import datetime

from requests import get, post, delete

print(get('http://localhost:5000/api/v2/users').json())

print(get('http://localhost:5000/api/v2/users/1').json())

print(get('http://localhost:5000/api/v2/users/999').json())
# при условии, что пользователя с id = 999 нет в базе

print(get('http://localhost:5000/api/v2/users/q').json())

# корректный запрос
print(post('http://localhost:5000/api/v2/users',
           json={'name': 'Scott',
                 'about': 'want to be a programmer',
                 'email': 'test23@mail.ru'}).json())

# некорректный: пустой запрос
print(post('http://localhost:5000/api/v2/users').json())

# некорректный: передано только имя
print(post('http://localhost:5000/api/v2/users',
           json={'name': 'Scott Jerard'}).json())

# корректный запрос
print(delete('http://localhost:5000/api/v2/users/3').json())

# некорректный: новости с id = 999 нет в базе
print(delete('http://localhost:5000/api/v2/users/999').json())

# некорректный: неверный формат id
print(delete('http://localhost:5000/api/v2/users/q').json())

# некорректный: пустой запрос
print(delete('http://localhost:5000/api/v2/users/users/q').json())
