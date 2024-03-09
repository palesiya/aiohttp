from controller import Controller
from src.arest.api.account import views

Controller.add("", views.Account, name="account", method=["*"])
Controller.add(
    "/token", views.Token, name="token_endpoint", method=["POST", "PUT", "DELETE"]
)
