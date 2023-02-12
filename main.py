import Server
import App_store

if __name__ == '__main__':
    app_store = App_store.ServerAppStore('127.0.0.1', '127.0.0.1', 5050)
    server1 = Server.Server('127.0.0.1', '127.0.0.1', 5051, app_store)

    my_app = App_store.Application('main.py', 'main.py')

    server1.install(my_app)
#
