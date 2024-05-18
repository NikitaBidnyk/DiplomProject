import random
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from datetime import datetime
from random import randint, choice  # добавляем импорт randint и choice

kivy.require('2.0.0')


class MathGame(App):
    def build(self):
        self.operators = ['+', '-', '*', '/', '^']
        self.main_layout = BoxLayout(orientation='vertical')

        # Показать главное меню при первом старте приложения
        self.show_main_menu()

        return self.main_layout

    def show_main_menu(self, instance=None):
        self.main_layout.clear_widgets()

        title_label = Label(text="MathDo", font_size='70sp')
        title_label.font_name = 'Danfo-Regular-VariableFont_ELSH.ttf'
        title_label.color = '#fff6db'
        self.main_layout.add_widget(title_label)

        easy_button = Button(text="Easy mode", font_size='40sp', on_press=self.start_easy_mode)
        easy_button.size_hint_y = 0.5
        easy_button.size_hint_x = 0.5
        easy_button.pos_hint = {'center_x': 0.5, 'center_y': 0.5}  # Размещаем кнопку по центру родительского контейнера
        easy_button.background_color = (0,0,0,0)
        easy_button.color = '#59f23a'
        easy_button.font_name = 'PoetsenOne-Regular.ttf'
        self.main_layout.add_widget(easy_button)

        normal_button = Button(text="Normal mode", font_size='40sp', on_press=self.start_normal_mode)
        normal_button.size_hint_y = 0.5
        normal_button.size_hint_x = 0.5
        normal_button.pos_hint = {'center_x': 0.5, 'center_y': 0.5}  # Размещаем кнопку по центру родительского контейнера
        normal_button.background_color = (0, 0, 0, 0)
        normal_button.color = '#f7bd40'
        normal_button.font_name = 'PoetsenOne-Regular.ttf'
        self.main_layout.add_widget(normal_button)

        hard_button = Button(text="Hard mode", font_size='40sp', on_press=self.start_hard_mode)
        hard_button.size_hint_y = 0.5
        hard_button.size_hint_x = 0.5
        hard_button.pos_hint = {'center_x': 0.5,'center_y': 0.5}  # Размещаем кнопку по центру родительского контейнера
        hard_button.background_color = (0, 0, 0, 0)
        hard_button.color = '#f00c36'
        hard_button.font_name = 'PoetsenOne-Regular.ttf'
        self.main_layout.add_widget(hard_button)

    def start_easy_mode(self, instance):
        self.roundF = 7
        self.lives = 4
        self.difficulty = 'easy'
        self.start_game()

    def start_normal_mode(self, instance):
        self.roundF = 15
        self.lives = 3
        self.difficulty = 'normal'
        self.start_game()

    def start_hard_mode(self, instance):
        self.roundF = 24
        self.lives = 2
        self.difficulty = 'hard'
        self.start_game()

    def start_game(self):
        self.layout = BoxLayout(orientation='vertical')

        # Верхняя часть интерфейса с отображением текущего уровня и таймера
        self.top_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp')
        self.level_label = Label(text=f"Rounds:1/{self.roundF}", font_size='50sp')
        self.level_label.font_name = 'Honk-Regular-VariableFont_MORF,SHLN.ttf'
        self.top_layout.add_widget(self.level_label)

        self.time_label = Label(text="Timer:00:00", font_size='57sp', halign='right')
        self.time_label.font_name = 'Jacquard12-Regular.ttf'
        self.top_layout.add_widget(self.time_label)

        self.lives_label = Label(text=f"Lives: {self.lives}", font_size='50sp')
        self.lives_label.font_name = 'Jaini-Regular.ttf'
        self.top_layout.add_widget(self.lives_label)

        self.layout.add_widget(self.top_layout)

        # Часть интерфейса с вопросом и кнопками
        self.question_label = Label(text='', font_size='45sp')
        self.question_label.font_name = 'PoetsenOne-Regular.ttf'
        self.layout.add_widget(self.question_label)

        self.buttons_layout = BoxLayout(orientation='horizontal')
        self.buttons_layout.size_hint_y = 0.7
        self.buttons_layout.size_hint_x = 0.7
        self.buttons_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.buttons = []
        for _ in range(3):
            button = Button(font_size='40sp', on_press=self.check_answer)
            button.color = '#3de048'
            button.font_name = 'PoetsenOne-Regular.ttf'
            button.background_color= '#c369cf'
            self.buttons.append(button)
            self.buttons_layout.add_widget(button)
        self.layout.add_widget(self.buttons_layout)

        # Нижняя часть интерфейса с кнопкой "Next question"
        self.next_button = Button(text='Next question', font_size='50sp', on_press=self.next_question)
        self.next_button.size_hint_y = 0.5
        self.next_button.size_hint_x = 0.5
        self.next_button.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.next_button.height = '50dp'
        self.next_button.opacity = 0
        self.next_button.disabled = True
        self.next_button.background_color = (0, 0, 0, 0)
        self.next_button.color = 'orange'
        self.next_button.font_name = 'Honk-Regular-VariableFont_MORF,SHLN.ttf'
        self.layout.add_widget(self.next_button)

        # Переменные для отслеживания текущего уровня
        self.roundT = 1  # Начальное количество пройденных уровней

        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.layout)

        # Генерация первого вопроса
        self.generate_question()

        # Запускаем таймер
        self.start_timer()

    def start_timer(self):
        self.start_time = datetime.now()  # Запоминаем время начала игры
        Clock.schedule_interval(self.update_timer, 1)  # Обновляем таймер каждую секунду

    def update_timer(self, dt):
        current_time = datetime.now()
        elapsed_time = current_time - self.start_time
        minutes = int(elapsed_time.total_seconds() // 60)
        seconds = int(elapsed_time.total_seconds() % 60)
        self.time_label.text = f"Timer:{minutes:02d}:{seconds:02d}"  # Форматируем время в виде "MM:SS"

    def generate_question(self):
        if self.roundT <= self.roundF and self.lives > 0:  # Проверяем, не завершилась ли игра
            num1 = randint(1, 100)
            num2 = randint(1, 12)  # avoiding division by zero
            operator = choice(self.operators)

            correct_answer = None  # Инициализируем переменную перед началом условий проверки оператора '^'

            if operator == '+':
                correct_answer = num1 + num2
            elif operator == '-':
                correct_answer = num1 - num2
            elif operator == '*':
                correct_answer = num1 * num2
            elif operator == '/':
                while num1 % num2 != 0:  # Повторяем генерацию, пока результат деления не будет целым
                    num1 = randint(1, 100)
                    num2 = randint(1, 12)  # avoiding division by zero
                    if num1 % num2 == 0:  # Check if division results in an integer
                        correct_answer = num1 // num2
                        break
            elif operator == '^':
                num1 = randint(1, 10)  # keeping base small for simplicity
                num2 = randint(1, 3)  # exponent should be <= 3
                correct_answer = num1 ** num2

            if correct_answer is not None:  # Проверяем, было ли установлено значение для correct_answer
                self.correct_answer = correct_answer
                self.question_label.text = f'{num1} {operator} {num2} = ?'

                answers = [correct_answer]
                for _ in range(2):
                    wrong_answer = correct_answer + randint(-10, 10)
                    while wrong_answer in answers:  # Avoid duplicates
                        wrong_answer = correct_answer + randint(-10, 10)
                    answers.append(wrong_answer)

                random.shuffle(answers)  # Перемешать список с ответами

                for i, button in enumerate(self.buttons):
                    button.text = str(answers[i])

                self.next_button.opacity = 0
                self.next_button.disabled = True
        else:
            self.end_game()

    def end_game(self):
        # При завершении игры меняем интерфейс на экран с результатами
        elapsed_time = datetime.now() - self.start_time
        minutes = int(elapsed_time.total_seconds() // 60)
        seconds = int(elapsed_time.total_seconds() % 60)
        time_text = f"Time left: {minutes:02d}:{seconds:02d}"

        self.layout.clear_widgets()
        if self.lives > 0:
            win_text1 = f"You win!"
            win_text2 = f"\nNumber of questions passed: {self.roundT - 1} / {self.roundF} \n{time_text}"
        else:
            win_text1 = f"You lose!"
            win_text2 = f"\nNumber of questions passed: {self.roundT - 1} / {self.roundF} \n{time_text}"

        rate_label = Label(text=win_text1,font_size='80sp', halign='center')
        rate_label.font_name = 'Jacquard12-Regular.ttf'
        rate_label.size_hint_y = 0.7
        rate_label.size_hint_x = 0.7
        rate_label.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        rate_label.color = 'red'

        combined_label = Label(text=win_text2, font_size='50sp', halign='center')
        combined_label.font_name = 'Jacquard12-Regular.ttf'
        combined_label.size_hint_y = 0.7
        combined_label.size_hint_x = 0.7
        combined_label.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        combined_label.color = 'yellow'
        self.layout.add_widget(rate_label)
        self.layout.add_widget(combined_label)

        play_again_button = Button(text='Play again', font_size='60sp', on_press=self.reset_game)
        play_again_button.font_name = 'Honk-Regular-VariableFont_MORF,SHLN.ttf'
        play_again_button.size_hint_y = 0.7
        play_again_button.size_hint_x = 0.7
        play_again_button.pos_hint = {'center_x': 0.5,'center_y': 0.5}  # Размещаем кнопку по центру родительского контейнера
        play_again_button.color = 'orange'
        play_again_button.background_color = (0,0,0,0)

        self.layout.add_widget(play_again_button)

        home_menu_button = Button(text='Home menu', font_size='60sp', on_press=self.show_main_menu)
        home_menu_button.font_name = 'Honk-Regular-VariableFont_MORF,SHLN.ttf'
        home_menu_button.size_hint_y = 0.7
        home_menu_button.size_hint_x = 0.7
        home_menu_button.pos_hint = {'center_x': 0.5,'center_y': 0.5}  # Размещаем кнопку по центру родительского контейнера
        home_menu_button.color = 'orange'
        home_menu_button.background_color = (0, 0, 0, 0)
        self.layout.add_widget(home_menu_button)

    def reset_game(self, instance):
        if self.difficulty == 'easy':
            self.roundF = 7
            self.lives = 4
        elif self.difficulty == 'normal':
            self.roundF = 15
            self.lives = 3
        elif self.difficulty == 'hard':
            self.roundF = 24
            self.lives = 2

        # Reset game variables
        self.roundT = 1
        self.layout.clear_widgets()

        # Rebuild the interface
        self.build_interface()
        self.generate_question()
        self.start_timer()

    def build_interface(self):
        # Верхняя часть интерфейса с отображением текущего уровня и таймера
        self.top_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp')
        self.level_label = Label(text=f"Rounds:1/{self.roundF}", font_size='50sp')
        self.level_label.font_name = 'Honk-Regular-VariableFont_MORF,SHLN.ttf'
        self.top_layout.add_widget(self.level_label)

        self.time_label = Label(text="Timer:00:00", font_size='57sp', halign='right')
        self.time_label.font_name = 'Jacquard12-Regular.ttf'
        self.top_layout.add_widget(self.time_label)

        self.lives_label = Label(text=f"Lives: {self.lives}", font_size='50sp')
        self.lives_label.font_name = 'Jaini-Regular.ttf'
        self.top_layout.add_widget(self.lives_label)

        self.layout.add_widget(self.top_layout)

        # Часть интерфейса с вопросом и кнопками
        self.question_label = Label(text='', font_size='60sp')
        self.question_label.font_name = 'PoetsenOne-Regular.ttf'
        self.layout.add_widget(self.question_label)

        self.buttons_layout = BoxLayout(orientation='horizontal')
        self.buttons_layout.size_hint_y = 0.7
        self.buttons_layout.size_hint_x = 0.7
        self.buttons_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        self.buttons = []
        for _ in range(3):
            button = Button(font_size='40sp', on_press=self.check_answer)
            button.color = '#3de048'
            button.font_name = 'PoetsenOne-Regular.ttf'
            button.background_color = '#c369cf'
            self.buttons.append(button)
            self.buttons_layout.add_widget(button)
        self.layout.add_widget(self.buttons_layout)

        # Нижняя часть интерфейса с кнопкой "Next question"
        self.next_button = Button(text='Next question', font_size='50sp', on_press=self.next_question)
        self.next_button.size_hint_y = 0.5
        self.next_button.size_hint_x = 0.5
        self.next_button.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.next_button.height = '50dp'
        self.next_button.opacity = 0
        self.next_button.disabled = True
        self.next_button.background_color = (0, 0, 0, 0)
        self.next_button.color = 'orange'
        self.next_button.font_name = 'Honk-Regular-VariableFont_MORF,SHLN.ttf'
        self.layout.add_widget(self.next_button)

    def check_answer(self, instance):
        if instance.text == str(self.correct_answer):
            self.question_label.text = "Your answer is correct! Good job!"
            self.question_label.font_size = 60
            self.next_button.opacity = 1
            self.next_button.disabled = False
        else:
            self.lives -= 1
            self.lives_label.text = f"Lives: {self.lives}"
            self.question_label.text = "Incorrect answer! Try better next time!"
            self.question_label.font_size = 60

            if self.lives == 0:
                self.end_game()

    def next_question(self, instance):
        self.roundT += 1  # Увеличиваем количество пройденных уровней
        self.level_label.text = f"Rounds:{self.roundT}/{self.roundF}"  # Обновляем отображение текущего уровня
        self.generate_question()


if __name__ == '__main__':
    MathGame().run()
