from transitions import Machine


class UsersState:
    def __init__(self, user_id):
        self.user_id = user_id
        self.machine = Machine(
            states=[
                "start",
                "choosing_movie_name",
                "choosing_movie_genre",
                "choosing_count_movies",
                "final",
            ],
            initial="start",
        )
        self.machine.add_transition(
            trigger="choose_movie_name", source="start", dest="choosing_movie_name"
        )
        self.machine.add_transition(
            trigger="choose_movie_genre",
            source="choosing_movie_name",
            dest="choosing_movie_genre",
        )
        self.machine.add_transition(
            trigger="choose_count_movies",
            source="choosing_movie_genre",
            dest="choosing_count_movies",
        )
        self.machine.add_transition(
            trigger="final", source="choosing_count_movies", dest="starte"
        )


# Словарь для хранения машин состояний пользователей
users_state = {}


# Функция для добавления новой машины состояний пользователя
def add_user(user_id):
    users_state[user_id] = UsersState(user_id)


add_user(1)
add_user(2)

for id, state in users_state.items():
    print(id, state.machine.state)

users_state[1].machine.choose_movie_name()

for id, state in users_state.items():
    print(id, state.machine.state)
# # Работа с состояниями пользователя с ID 1
# user_machines[1].machine.login()  # Пользователь 1 зашел в систему
# print(f"User 1 state: {user_machines[1].machine.state}")  # Вывод: online
#
# user_machines[1].machine.start_work()  # Пользователь 1 начал работу
# print(f"User 1 state: {user_machines[1].machine.state}")  # Вывод: busy
#
# user_machines[1].machine.end_work()  # Пользователь 1 закончил работу
# print(f"User 1 state: {user_machines[1].machine.state}")  # Вывод: online
#
# user_machines[1].machine.logout()  # Пользователь 1 вышел из системы
# print(f"User 1 state: {user_machines[1].machine.state}")  # Вывод: offline
#
# print(f"User 2 state: {user_machines[2].machine.state}")
