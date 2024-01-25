from controller import Controller
from src.aihttp.api.account import views

Controller.add("", views.Account, name="account", method=["*"])