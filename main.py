import telegram.ext
from usr_input import UserInputs
from task_manager import TaskManager

class TaskBot:
    def __init__(self, token):
        self.TOKEN = token
        self.NEXT, self.FINISH = range(2)
        worker = TaskManager(458158090, 'test', 'test')
        self.viewer = UserInputs(worker, self.NEXT, self.FINISH)
        self.updater = telegram.ext.Updater(self.TOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.register_handlers()

    def register_handlers(self):
        proj_create_handler = telegram.ext.ConversationHandler(
            entry_points=[telegram.ext.CommandHandler('create_project', self.viewer.create_project_start)],
            states={
                self.NEXT: [telegram.ext.MessageHandler(telegram.ext.Filters.text & ~telegram.ext.Filters.command,
                                                        self.viewer.create_project_finish)],
            },
            fallbacks=[telegram.ext.CommandHandler('cancel', self.viewer.cancel)]
        )

        proj_delete_handler = telegram.ext.ConversationHandler(
            entry_points=[telegram.ext.CommandHandler('delete_project', self.viewer.delete_project_start)],
            states={
                self.NEXT: [telegram.ext.MessageHandler(telegram.ext.Filters.text & ~telegram.ext.Filters.command,
                                                        self.viewer.delete_project_finish)],
            },
            fallbacks=[telegram.ext.CommandHandler('cancel', self.viewer.cancel)]
        )

        task_add_handler = telegram.ext.ConversationHandler(
            entry_points=[telegram.ext.CommandHandler('add_task', self.viewer.add_task_start)],
            states={
                self.NEXT: [telegram.ext.MessageHandler(telegram.ext.Filters.text & ~telegram.ext.Filters.command,
                                                        self.viewer.add_task_next)],
                self.FINISH: [telegram.ext.MessageHandler(telegram.ext.Filters.text & ~telegram.ext.Filters.command,
                                                          self.viewer.add_task_finish)],
            },
            fallbacks=[telegram.ext.CommandHandler('cancel', self.viewer.cancel)]
        )

        task_list_handler = telegram.ext.ConversationHandler(
            entry_points=[telegram.ext.CommandHandler('task_list', self.viewer.task_list_start)],
            states={
                self.NEXT: [telegram.ext.MessageHandler(telegram.ext.Filters.text & ~telegram.ext.Filters.command,
                                                        self.viewer.task_list_finish)],
            },
            fallbacks=[telegram.ext.CommandHandler('cancel', self.viewer.cancel)]
        )

        proj_clear_handler = telegram.ext.ConversationHandler(
            entry_points=[telegram.ext.CommandHandler('clear_project', self.viewer.clear_project_start)],
            states={
                self.NEXT: [telegram.ext.MessageHandler(telegram.ext.Filters.text & ~telegram.ext.Filters.command,
                                                        self.viewer.clear_project_finish)],
            },
            fallbacks=[telegram.ext.CommandHandler('cancel', self.viewer.cancel)]
        )

        task_delete_handler = telegram.ext.ConversationHandler(
            entry_points=[telegram.ext.CommandHandler('delete_task', self.viewer.delete_task_start)],
            states={
                self.NEXT: [telegram.ext.MessageHandler(telegram.ext.Filters.text & ~telegram.ext.Filters.command,
                                                        self.viewer.delete_task_next)],
                self.FINISH: [telegram.ext.MessageHandler(telegram.ext.Filters.text & ~telegram.ext.Filters.command,
                                                          self.viewer.delete_task_finish)],
            },
            fallbacks=[telegram.ext.CommandHandler('cancel', self.viewer.cancel)]
        )

        task_done_handler = telegram.ext.ConversationHandler(
            entry_points=[telegram.ext.CommandHandler('mark_as_done', self.viewer.task_done_start)],
            states={
                self.NEXT: [telegram.ext.MessageHandler(telegram.ext.Filters.text & ~telegram.ext.Filters.command,
                                                        self.viewer.task_done_next)],
                self.FINISH: [telegram.ext.MessageHandler(telegram.ext.Filters.text & ~telegram.ext.Filters.command,
                                                          self.viewer.task_done_finish)],
            },
            fallbacks=[telegram.ext.CommandHandler('cancel', self.viewer.cancel)]
        )

        # 1 stage commands
        self.dispatcher.add_handler(telegram.ext.CommandHandler('start', self.viewer.start))
        self.dispatcher.add_handler(telegram.ext.CommandHandler('help', self.viewer.help))
        self.dispatcher.add_handler(telegram.ext.CommandHandler('projects_list', self.viewer.list_of_projects))

        # 2 stage commands
        self.dispatcher.add_handler(proj_create_handler)
        self.dispatcher.add_handler(proj_delete_handler)
        self.dispatcher.add_handler(proj_clear_handler)
        self.dispatcher.add_handler(task_list_handler)

        # 3 stage commands
        self.dispatcher.add_handler(task_add_handler)
        self.dispatcher.add_handler(task_delete_handler)
        self.dispatcher.add_handler(task_done_handler)

        # error handling
        self.dispatcher.add_error_handler(self.viewer.error)

    def start(self):
        print('Polling...')
        self.updater.start_polling()
        self.updater.idle()

if __name__ == '__main__':
    with open('bot api token.txt', 'r') as f:
        token = f.read()

    bot = TaskBot(token)
    bot.start()
