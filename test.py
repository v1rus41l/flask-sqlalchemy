import datetime

from requests import get, post, delete

print(get('http://localhost:5000/api/v2/jobs').json())

print(get('http://localhost:5000/api/v2/jobs/1').json())

print(get('http://localhost:5000/api/v2/jobs/999').json())
# при условии, что работы с id = 999 нет в базе

print(get('http://localhost:5000/api/v2/jobs/q').json())

# корректный запрос
print(post('http://localhost:5000/api/v2/jobs',
           json={'team_leader': 2,
                 'job': 'engine repairing',
                 'collaborators': '2, 3',
                 'work_size': 24,
                 'is_finished': False}).json())

# некорректный: пустой запрос
print(post('http://localhost:5000/api/v2/jobs').json())

# некорректный: передано только название работы
print(post('http://localhost:5000/api/v2/jobs',
           json={'jobs': 'engine repairing'}).json())

# корректный запрос
print(delete('http://localhost:5000/api/v2/jobs/3').json())

# некорректный: новости с id = 999 нет в базе
print(delete('http://localhost:5000/api/v2/jobs/999').json())

# некорректный: неверный формат id
print(delete('http://localhost:5000/api/v2/jobs/q').json())

# некорректный: пустой запрос
print(delete('http://localhost:5000/api/v2/jobs').json())
