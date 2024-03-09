from controller import Controller
from .views import FileView, FollowView


Controller.add("", FileView, name="files_view", method=["POST", "GET"])
Controller.add(
    "/follow/{file_uuid}", FollowView, name="follow_view", method=["POST", "GET"]
)
