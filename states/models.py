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
                "choosing_movie_rating",
                "choosing_count_movie_rating",
                "choosing_low_budget_movie",
                "choosing_count_low_budget_movie",
                "choosing_high_budget_movie",
                "choosing_count_high_budget_movie",
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
            trigger="final", source="choosing_count_movies", dest="start"
        )
        self.machine.add_transition(trigger="cancel", source="*", dest="start")
        self.machine.add_transition(
            trigger="choose_rating", source="start", dest="choosing_movie_rating"
        )
        self.machine.add_transition(
            trigger="choose_count_movie_rating",
            source="choosing_movie_rating",
            dest="choosing_count_movie_rating",
        )
        self.machine.add_transition(
            trigger="final", source="choosing_count_movie_rating", dest="start"
        )
        self.machine.add_transition(
            trigger="choose_low_budget",
            source="start",
            dest="choosing_low_budget_movie",
        )
        self.machine.add_transition(
            trigger="choose_count_low_budget",
            source="choosing_low_budget_movie",
            dest="choosing_count_low_budget_movie",
        )
        self.machine.add_transition(
            trigger="final", source="choosing_count_low_budget_movie", dest="start"
        )
        self.machine.add_transition(
            trigger="choose_high_budget",
            source="start",
            dest="choosing_high_budget_movie",
        )
        self.machine.add_transition(
            trigger="choose_count_high_budget",
            source="choosing_high_budget_movie",
            dest="choosing_count_high_budget_movie",
        )
        self.machine.add_transition(
            trigger="final", source="choosing_count_high_budget_movie", dest="start"
        )


# Словарь для хранения машин состояний пользователей
users_state = {}


# Функция для добавления новой машины состояний пользователя
def add_user(user_id):
    users_state[user_id] = UsersState(user_id)


def get_state(user_id):
    return users_state[user_id].machine.state
