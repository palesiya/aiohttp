from controller import Controller
from src.aihttp.web.home.views import HomeView


Controller.include("/api", "src.aihttp.api.urls")
Controller.add("/", HomeView, name="home_page", method=["GET"])
