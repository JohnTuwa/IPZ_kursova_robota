import telegram.ext

class UserInputs:
    def __init__(self, taskmanager, first, last):
        self.NEXT, self.FINISH = first, last
        self.worker = taskmanager

    def start(self, update, context):
        update.message.reply_text('''Вітаю! Дякую що обрали TaskPal!
/help - додаткова інформація по використанню''')
        self.worker.user_id = update.message.chat_id
        print(self.worker.user_id)

    def help(self, update, context):
        update.message.reply_text('Я - бот для організації завдань. Я допоможу вам з веденням обліку ваших завдань,'
                                  'розподілених на "проєкти", та відслідковуванням їх виконання')
        update.message.reply_text('''Ось наявних команд для TaskPal:
/start - Запуск бота
/help - Список команд TaskPal та загальна інформація
/create_project - Створити новий проєкт
/delete_project - Видалити проєкт
/projects_list - Список наявних проєктів
/add_task - Додати завдання в проєкт
/delete_task - Видалити завдання з проєкту
/task_list - Список завдань в проєкті
/clear_project - Видалити усі завдання з проєкту
/mark_as_done - Позначити проєкт як виконаний
/cancel - Відмінити виконання команди
''')

    def create_project_start(self, update, context):
        update.message.reply_text('Введіть назву проєкту:')
        return self.NEXT
    def create_project_finish(self, update, context):
        self.worker.user_id = update.message.chat_id
        self.worker.project_name = update.message.text
        response = self.worker.create_project()
        update.message.reply_text(response)
        return telegram.ext.ConversationHandler.END

    def delete_project_start(self, update, context):
        self.worker.user_id = update.message.chat_id
        formatted_list = '\n'.join(self.worker.projects_list())
        if len(formatted_list) == 0:
            update.message.reply_text('Ви ще не створили жодного проєкту')
            return telegram.ext.ConversationHandler.END
        temp_message = update.message.reply_text(f'''Список ваших проєктів:
{formatted_list}''')
        context.user_data['msg_to_del_id'] = temp_message.message_id
        update.message.reply_text('Введіть назву проєкту який хочете видалити:')
        return self.NEXT
    def delete_project_finish(self, update, context):
        self.worker.project_name = update.message.text
        context.bot.delete_message(chat_id=self.worker.user_id, message_id=context.user_data['msg_to_del_id'])
        response = self.worker.delete_project()
        update.message.reply_text(response)
        return telegram.ext.ConversationHandler.END

    def add_task_start(self, update, context):
        self.worker.user_id = update.message.chat_id
        formatted_list = '\n'.join(self.worker.projects_list())
        if len(formatted_list) == 0:
            update.message.reply_text('Ви ще не створили жодного проєкту')
            return telegram.ext.ConversationHandler.END
        temp_message = update.message.reply_text(f'''Список ваших проєктів:
{formatted_list}''')
        context.user_data['msg_to_del_id'] = temp_message.message_id
        update.message.reply_text('Введіть назву проєкту в який хочете додати завдання:')
        return self.NEXT
    def add_task_next(self, update, context):
        self.worker.project_name = update.message.text
        context.bot.delete_message(chat_id=self.worker.user_id, message_id=context.user_data['msg_to_del_id'])
        formatted_list = '\n'.join(self.worker.task_list())
        temp_message = update.message.reply_text(f'''Список завдань в проєкті {self.worker.project_name}:
{formatted_list}''')
        context.user_data['msg_to_del_id'] = temp_message.message_id
        update.message.reply_text('Введіть назву завдання:')
        return self.FINISH
    def add_task_finish(self, update, context):
        self.worker.task_name = update.message.text
        context.bot.delete_message(chat_id=self.worker.user_id, message_id=context.user_data['msg_to_del_id'])
        response = self.worker.add_task()
        update.message.reply_text(response)
        return telegram.ext.ConversationHandler.END

    def task_list_start(self, update, context):
        self.worker.user_id = update.message.chat_id
        formatted_list = '\n'.join(self.worker.projects_list())
        if len(formatted_list) == 0:
            update.message.reply_text('Ви ще не створили жодного проєкту')
            return telegram.ext.ConversationHandler.END
        temp_message = update.message.reply_text(f'''Список ваших проєктів:
{formatted_list}''')
        context.user_data['msg_to_del_id'] = temp_message.message_id
        update.message.reply_text('Введіть назву проєкту:')
        return self.NEXT
    def task_list_finish(self, update, context):
        self.worker.project_name = update.message.text
        context.bot.delete_message(chat_id=self.worker.user_id, message_id=context.user_data['msg_to_del_id'])
        received_list = self.worker.task_list()
        if not received_list:
            update.message.reply_text(f"Проєкт з таким ім'ям не існує")
            return telegram.ext.ConversationHandler.END
        formatted_list = '\n'.join(received_list)
        update.message.reply_text(f'''Список завдань в проєкті {self.worker.project_name}:
{formatted_list}''')
        return telegram.ext.ConversationHandler.END

    def delete_task_start(self, update, context):
        self.worker.user_id = update.message.chat_id
        formatted_list = '\n'.join(self.worker.projects_list())
        if len(formatted_list) == 0:
            update.message.reply_text('Ви ще не створили жодного проєкту')
            return telegram.ext.ConversationHandler.END
        temp_message = update.message.reply_text(f'''Список ваших проєктів:
{formatted_list}''')
        context.user_data['msg_to_del_id'] = temp_message.message_id
        update.message.reply_text('Введіть назву проєкту в якому хочете видалити завдання:')
        return self.NEXT

    def delete_task_next(self, update, context):
        self.worker.project_name = update.message.text
        context.bot.delete_message(chat_id=self.worker.user_id, message_id=context.user_data['msg_to_del_id'])
        formatted_list = '\n'.join(self.worker.task_list())
        if len(formatted_list) == 0:
            update.message.reply_text('В цьому проєкті немає завдань')
            return telegram.ext.ConversationHandler.END
        temp_message = update.message.reply_text(f'''Список завдань в проєкті {self.worker.project_name}:
{formatted_list}''')
        context.user_data['msg_to_del_id'] = temp_message.message_id
        update.message.reply_text('Введіть назву завдання:')
        return self.FINISH
    def delete_task_finish(self, update, context):
        self.worker.task_name = update.message.text
        context.bot.delete_message(chat_id=self.worker.user_id, message_id=context.user_data['msg_to_del_id'])
        response = self.worker.delete_task()
        update.message.reply_text(response)
        return telegram.ext.ConversationHandler.END

    def clear_project_start(self, update, context):
        self.worker.user_id = update.message.chat_id
        formatted_list = '\n'.join(self.worker.projects_list())
        temp_message = update.message.reply_text(f'''Список ваших проєктів:
{formatted_list}''')
        context.user_data['msg_to_del_id'] = temp_message.message_id
        update.message.reply_text('Введіть назву проєкту який хочете очистити:')
        return self.NEXT
    def clear_project_finish(self, update, context):
        self.worker.project_name = update.message.text
        context.bot.delete_message(chat_id=self.worker.user_id, message_id=context.user_data['msg_to_del_id'])
        response = self.worker.clear_project()
        update.message.reply_text(response)
        return telegram.ext.ConversationHandler.END

    def task_done_start(self, update, context):
        self.worker.user_id = update.message.chat_id
        formatted_list = '\n'.join(self.worker.projects_list())
        if len(formatted_list) == 0:
            update.message.reply_text('Ви ще не створили жодного проєкту')
            return telegram.ext.ConversationHandler.END
        temp_message = update.message.reply_text(f'''Список ваших проєктів:
{formatted_list}''')
        context.user_data['msg_to_del_id'] = temp_message.message_id
        update.message.reply_text('Введіть назву проєкту:')
        return self.NEXT
    def task_done_next(self, update, context):
        self.worker.project_name = update.message.text
        context.bot.delete_message(chat_id=self.worker.user_id, message_id=context.user_data['msg_to_del_id'])
        formatted_list = '\n'.join(self.worker.task_list())
        if len(formatted_list) == 0:
            update.message.reply_text('В цьому проєкті немає завдань')
            return telegram.ext.ConversationHandler.END
        temp_message = update.message.reply_text(f'''Список завдань в проєкті {self.worker.project_name}
{formatted_list}''')
        context.user_data['msg_to_del_id'] = temp_message.message_id
        update.message.reply_text('Введіть назву завдання:')
        return self.FINISH
    def task_done_finish(self, update, context):
        self.worker.task_name = update.message.text
        context.bot.delete_message(chat_id=self.worker.user_id, message_id=context.user_data['msg_to_del_id'])
        response, run_res = self.worker.mark_as_done()
        update.message.reply_text(response)
        if not run_res:
            return telegram.ext.ConversationHandler.END
        cheering_response = self.worker.percentage_is_done()
        update.message.reply_text(cheering_response)
        return telegram.ext.ConversationHandler.END

    def list_of_projects(self, update, context):
        self.worker.user_id = update.message.chat_id
        formatted_list = '\n'.join(self.worker.projects_list())
        if len(formatted_list) == 0:
            update.message.reply_text('Ви ще не створили жодного проєкту')
            return telegram.ext.ConversationHandler.END
        update.message.reply_text(f'''Список ваших проєктів:
{formatted_list}''')

    def cancel(self, update, context):
        update.message.reply_text('Команду скасовано')
        context.bot.delete_message(chat_id=self.worker.user_id, message_id=context.user_data['msg_to_del_id'])
        return telegram.ext.ConversationHandler.END

    def error(self, update, context):
        print(f'Update {update} caused error {context.error}')
