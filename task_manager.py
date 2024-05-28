from os import remove, listdir, mkdir, path


class TaskManager:
    def __init__(self, user_id, project_name, task_name):
        self.user_id = user_id
        self.project_name = project_name
        self.task_name = task_name

    def create_project(self):
        dir_path = f'project_data\\{self.user_id}'
        if not path.exists(dir_path):
            mkdir(dir_path)
        project_path = f'project_data\\{self.user_id}\\{self.project_name}.txt'
        try:
            with open(project_path, 'x') as f:
                return f'Проєкт "{self.project_name}" створено!'
        except FileExistsError:
            return f'Проєкт "{self.project_name}" вже існує!'

    def delete_project(self):
        project_path = f'project_data\\{self.user_id}\\{self.project_name}.txt'
        project_path_done = f'project_data\\{self.user_id}\\{self.project_name}_done.txt'
        try:
            remove(project_path)
            try:
                remove(project_path_done)
            except FileNotFoundError:
                pass
            return f'Проєкт "{self.project_name}" видалено!'
        except FileNotFoundError:
            return f'Проєкт "{self.project_name}" не знайдено!'

    def projects_list(self):
        folder_path = f'project_data\\{self.user_id}'
        all_names = listdir(folder_path)
        user_projects = [name for name in all_names if not name.endswith('_done.txt')]
        user_projects_formatted = [project_name.replace('.txt', '') for project_name in user_projects]
        return user_projects_formatted

    def task_list(self, project_name=None):
        project_name = project_name or self.project_name
        project_path = f'project_data\\{self.user_id}\\{project_name}.txt'
        lines = []
        try:
            with open(project_path, 'r') as f:
                for line in f:
                    lines.append(line.strip())
            return lines
        except FileNotFoundError:
            return False

    def add_task(self):
        project_path = f'project_data\\{self.user_id}\\{self.project_name}.txt'
        all_names = listdir(f'project_data\\{self.user_id}')
        if f'{self.project_name}.txt' not in all_names:
            return f'Проєкт "{self.project_name}" не знайдено!'
        if self.task_name in self.task_list():
            return f'Завдання "{self.task_name}" вже існує в "{self.project_name}"!'
        with open(project_path, 'a') as f:
            print(self.task_name, file=f)
        return f'Завдання "{self.task_name}" додано до "{self.project_name}"!'

    def delete_task(self):
        project_path = f'project_data\\{self.user_id}\\{self.project_name}.txt'
        done_list = f'project_data\\{self.user_id}\\{self.project_name}_done.txt'
        try:
            with open(project_path, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            return f'Проєкт "{self.project_name}" не знайдено!'
        if self.task_name not in self.task_list():
            return f'Завдання "{self.task_name}" не знайдено в "{self.project_name}"!'
        lines = [line for line in lines if line.strip() != self.task_name]
        with open(project_path, 'w') as f:
            for line in lines:
                f.write(line)
        try:
            with open(done_list, 'r') as f:
                lines_done = f.readlines()
            lines_done = [line for line in lines_done if line.strip() != self.task_name]
            with open(done_list, 'w') as f:
                for line in lines_done:
                    f.write(line)
        except FileNotFoundError:
            pass
        return f'Завдання "{self.task_name}" видалено з "{self.project_name}"!'

    def clear_project(self):
        project_path = f'project_data\\{self.user_id}\\{self.project_name}.txt'
        all_names = listdir(f'project_data\\{self.user_id}')
        if f'{self.project_name}.txt' not in all_names:
            return f'Проєкт "{self.project_name}" не знайдено!'
        with open(project_path, 'w') as f:
            f.write('')
        return f'Проєкт "{self.project_name}" очищено!'

    def mark_as_done(self):
        all_names = listdir(f'project_data\\{self.user_id}')
        if f'{self.project_name}.txt' not in all_names:
            return f'Проєкт "{self.project_name}" не знайдено!', False
        if self.task_name not in self.task_list():
            return f'Завдання "{self.task_name}" не знайдено в "{self.project_name}"!', False
        done_list = f'project_data\\{self.user_id}\\{self.project_name}_done.txt'
        if self.task_name in self.task_list(f'{self.project_name}_done'):
            return f'Завдання "{self.task_name}" уже виконано!', False
        with open(done_list, 'a') as f:
            print(self.task_name, file=f)
        return f'Завдання "{self.task_name}" в "{self.project_name}" виконано, чудова робота!', True

    def percentage_is_done(self):
        project_path = f'project_data\\{self.user_id}\\{self.project_name}.txt'
        done_list = f'project_data\\{self.user_id}\\{self.project_name}_done.txt'
        with open(project_path, 'r') as f:
            tasks_amount = len(f.readlines())
        with open(done_list, 'r') as f:
            tasks_done_amount = len(f.readlines())
        percentage = (tasks_done_amount / tasks_amount) * 100
        if percentage != 100:
            return f'Ви подолали {percentage:.2f}% шляху! Продовжуйте в тому ж дусі!'
        return f'Вітаю! Проєкт {self.project_name} успішно завершено! Чудова робота!'
