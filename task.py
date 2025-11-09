from datetime import datetime

from PyQt6.QtGui import QIcon
from db import get_connection
from taskcard import Ui_Form
from PyQt6.QtWidgets import QWidget, QPushButton, QProgressBar
import time

style_radiobutt = """
QRadioButton::indicator {
	width: 15px;
	height:15px;
	border:1px solid black;
	border-radius: 8px;
	background: white;
}
QRadioButton::indicator:checked{
	background: need_color;
	border: 1px solid #666666;
}"""
import sys
from PyQt6 import uic
from main import Second

class TaskCard(QWidget):
    def __init__(self, title, description='', date=None, priority='NORMAL', difficulty_level=0, important=0,
                 completed=0, id_task=None):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.id_task = id_task
        self.title = title
        self.description = description
        self.date = date
        self.priority_2 = priority
        self.difficulty_level = difficulty_level
        self.important = important
        self.completed = completed
        self.sec_win = None
    def init_card(self):
        self.ui.title.setText(self.title)
        self.ui.description.setText(self.description)
        self.ui.date.setText(self.date)

        self.ui.editButton.clicked.connect(self.prog)
        self.ui.next_button.clicked.connect(self.vison)
        self.ui.importantButton.clicked.connect(self.important_funct)

        if self.important == 1:
            self.ui.importantButton.setIcon(QIcon(r"icons\dark_theme\star-fill.png"))
        else:
            self.ui.importantButton.setIcon(QIcon(r"icons\dark_theme\star-line.png"))
        button = [self.ui.priorButton_5, self.ui.priorButton_6, self.ui.priorButton_7, self.ui.priorButton_8,
                  self.ui.priorButton_9]

        for n, radio_but in enumerate(button):
            print(n)
            radio_but.clicked.connect(lambda _, x=n: self.priority_task(x))

    def prog(self):
        # for i in range(101):
        #     time.sleep(0.03)
        #     self.ui.progressBar.setValue(i)
        self.sec_win = Second()
        self.sec_win.show()
    def important_funct(self):
        if self.important == 1:
            self.important = 0
            self.ui.importantButton.setIcon(QIcon(r"icons\dark_theme\star-line.png"))
        else:
            self.important = 1
            self.ui.importantButton.setIcon(QIcon(r"icons\dark_theme\star-fill.png"))

        conn = get_connection()
        cur = conn.cursor()
        cur.execute('UPDATE tasks SET important = NOT important WHERE title = ?', (self.title,))
        conn.commit()
        conn.close()

    def vison(self):
        vis = self.ui.extraWidget.isVisible()
        self.ui.extraWidget.setVisible(not vis)

    def priority_task(self, number):
        print(number)
        colors = ['lime', 'green', 'yellow', 'red', 'black']
        button = [self.ui.priorButton_5, self.ui.priorButton_6, self.ui.priorButton_7, self.ui.priorButton_8,
                  self.ui.priorButton_9]
        for i in button[:number + 1]:
            i.setChecked(1)
            i.setStyleSheet(style_radiobutt.replace('need_color', colors[number]))
        for i in button[number + 1:]:
            i.setChecked(0)

    def __str__(self):
        return f'{self.title, self.description, self.date, self.priority}'

    def __repr__(self):
        return str(self)


class TaskManager:
    def add_task(self, task: TaskCard):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(f"""
        INSERT INTO tasks (title, description, date, priority, completed) VALUE (?,?,?,?,?)""",
                    (task.title, task.description, task.date, int(task.priority), task.completed))
        conn.commit()
        conn.close()

    def get_all_tasks(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM tasks')
        tasks = cur.fetchall()
        conn.close()
        return [TaskCard(*x[1:], x[0]) for x in tasks]

    def get_completed_status(self, completed_status):
        conn = get_connection()
        cur = conn.cursor()
        if completed_status:
            cur.execute('SELECT * FROM tasks WHERE completed = 1')
        else:
            cur.execute('SELECT * FROM tasks WHERE completed = 0')
        tasks = cur.fetchall()
        conn.close()
        return [Task(*x[1:]) for x in tasks]

    def mark_completed(self, task_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('UPDATE tasks SET completed= NOT completed WHERE id=?', (task_id,))
        conn.commit()
        conn.close()

    def delete_task(self, task_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()


class SubTasks:
    def __init__(self, title, id_tasks, description='', priority='NORMAL', completed=0):
        self.title = title
        self.id_tasks = id_tasks
        self.description = description
        self.priority = priority
        self.completed = completed

    def __str__(self):
        return f'{self.title, self.description, self.priority, self.completed, self.id_tasks}'

    def __repr__(self):
        return str(self)


class SubTaskManager:
    def add_subtask(self, subtask: SubTasks):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO subtasks (title, description, priority, completed, id_task) VALUES (?,?,?,?,?)',
                    (subtask.title, subtask.description, subtask.priority, subtask.completed, int(subtask.id_task)))
        conn.commit()
        conn.close()
