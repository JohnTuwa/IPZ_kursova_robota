import unittest
from task_manager import TaskManager

class TestTaskmanager(unittest.TestCase):

    def test_create_proj(self):
        proj1 = TaskManager(1234, 'not_exists', '')
        proj2 = TaskManager(1234, 'already_exists', '')

        self.assertEqual(proj1.create_project(), 'Проєкт "not_exists" створено!')
        self.assertEqual(proj2.create_project(), 'Проєкт "already_exists" вже існує!')

        proj1.delete_project()

    def test_delete_proj(self):
        proj1 = TaskManager(1234, 'not_exists', '')
        proj2 = TaskManager(1234, 'already_exists', '')

        self.assertEqual(proj1.delete_project(), 'Проєкт "not_exists" не знайдено!')
        self.assertEqual(proj2.delete_project(), 'Проєкт "already_exists" видалено!')

        with open(f'project_data\\1234\\already_exists.txt', 'a') as f:
            print('i am a line', file=f)
            print('will be done', file=f)
        with open(f'project_data\\1234\\already_exists_done.txt', 'a') as f:
            print('i am a line', file=f)

    def test_proj_list(self):
        user_test = TaskManager(1234, '', '')

        self.assertEqual(user_test.projects_list(), ['already_exists'])

    def test_task_list(self):
        proj1 = TaskManager(1234, 'not_exists', '')
        proj2 = TaskManager(1234, 'already_exists', '')

        self.assertEqual(proj1.task_list(), False)
        self.assertEqual(proj2.task_list(), ['i am a line', 'will be done'])

    def test_add_task(self):
        proj1 = TaskManager(1234, 'not_exists', '')
        proj2 = TaskManager(1234, 'already_exists', 'i am a line')
        proj3 = TaskManager(1234, 'already_exists', 'i am a new line')

        self.assertEqual(proj1.add_task(), 'Проєкт "not_exists" не знайдено!')
        self.assertEqual(proj2.add_task(), 'Завдання "i am a line" вже існує в "already_exists"!')
        self.assertEqual(proj3.add_task(), 'Завдання "i am a new line" додано до "already_exists"!')

        proj3.delete_task()

    def test_delete_task(self):
        proj1 = TaskManager(1234, 'not_exists', '')
        proj2 = TaskManager(1234, 'already_exists', 'i am a line')
        proj3 = TaskManager(1234, 'already_exists', 'i am a new line')

        self.assertEqual(proj1.delete_task(), 'Проєкт "not_exists" не знайдено!')
        self.assertEqual(proj2.delete_task(), 'Завдання "i am a line" видалено з "already_exists"!')
        self.assertEqual(proj3.delete_task(), 'Завдання "i am a new line" не знайдено в "already_exists"!')

        proj2.add_task()
        proj2.project_name = 'already_exists_done'
        proj2.add_task()

    def test_project_clear(self):
        proj1 = TaskManager(1234, 'not_exists', '')
        proj2 = TaskManager(1234, 'already_exists', 'i am a line')

        self.assertEqual(proj1.clear_project(), 'Проєкт "not_exists" не знайдено!')
        self.assertEqual(proj2.clear_project(), 'Проєкт "already_exists" очищено!')

        with open(f'project_data\\1234\\already_exists.txt', 'a') as f:
            print('i am a line', file=f)
            print('will be done', file=f)

    def test_done(self):
        proj1 = TaskManager(1234, 'not_exists', '')
        proj2 = TaskManager(1234, 'already_exists', 'i am a line')
        proj3 = TaskManager(1234, 'already_exists', 'i am a new line')
        proj4 = TaskManager(1234, 'already_exists', 'will be done')

        response1, result1 = proj1.mark_as_done()
        response2, result2 = proj2.mark_as_done()
        response3, result3 = proj3.mark_as_done()
        response4, result4 = proj4.mark_as_done()

        self.assertEqual(response1, 'Проєкт "not_exists" не знайдено!')
        self.assertEqual(response2, 'Завдання "i am a line" уже виконано!')
        self.assertEqual(response3, 'Завдання "i am a new line" не знайдено в "already_exists"!')
        self.assertEqual(response4, 'Завдання "will be done" в "already_exists" виконано, чудова робота!')

        proj4.project_name = 'already_exists_done'
        proj4.delete_task()

    def test_percent(self):
        proj1 = TaskManager(1234, 'already_exists', '')

        self.assertEqual(proj1.percentage_is_done(), 'Ви подолали 50.00% шляху! Продовжуйте в тому ж дусі!')
        
