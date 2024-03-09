from controller import Controller
from arest.web.home.views import HomeView, ActivateView
from arest.api.files.views import DownloadView

Controller.include("/api", "arest.api.urls")
Controller.add("/", HomeView, name="home_page", method=["GET"])
Controller.add(
    "/activate/{activate_token:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}}",
    ActivateView,
    name="activate",
    method=["GET"],
)
Controller.add(
    (
        "/{file_uuid:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}}"
        r"/{file_name:[\w\s]+}"
    ),
    DownloadView,
    name="download_view",
    method=["GET"],
)
