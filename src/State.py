class State:
    """
    класс состояния автомата
    содержит в себе информацию о принимаемости self.receiving
    содердит в себе токен состояния или None в случае непринимаемости
    """

    _counter = 0
    """
    переменная, считающая количество экзепляров класса
    """

    def __init__(self, token_name=None):
        """
        :param token_name: название токена, если состояяние принимающее
        """
        if token_name is not None:
            self.receiving = True
            self.token_name = token_name
        else:
            self.receiving = False
        State._counter += 1
        self.counter = int(State._counter)

    def get_token(self):
        """
        :return: Возвращает имя токена
        """
        return self.token_name

    def assign_token(self, token_name):
        """
        :param token_name: название токена
        делает состояние принимающим, именует токен
        """
        self.receiving = True
        self.token_name = token_name

    def cancel_token(self):
        """
        делает состояние непринимающим
        """
        self.receiving = False
        self.token_name = None

    def __hash__(self):
        return self.counter

    def __eq__(self, other):
        return self.counter == other.counter

