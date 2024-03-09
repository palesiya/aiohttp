from controller import Controller

Controller.include("/account", "arest.api.account.urls")
Controller.include("/file", "arest.api.files.urls")
