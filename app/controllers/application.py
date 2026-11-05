from bottle import template, redirect, request
from app.controllers.datarecord import DataRecord


class Application:
    def __init__(self):
        self.pages = {
            "helper": self.helper,
            "portal": self.portal,
            "banco": self.banco,
        }
        # Composição: Application administra os dados por meio de DataRecord.
        self.models = DataRecord()

    def render(self, page):
        content = self.pages.get(page, self.helper)
        return content()

    def get_session_id(self):
        return request.get_cookie("session_id")

    def current_user(self):
        return self.models.get_current_user(self.get_session_id())

    def is_authenticated(self):
        return self.current_user() is not None

    def authenticate_user(self, username, password):
        return self.models.check_user(username, password)

    def logout_user(self):
        self.models.logout(self.get_session_id())

    def helper(self):
        return template("app/views/html/helper")

    def portal(self, error=None):
        return template("app/views/html/portal", error=error)

    def banco(self):
        if not self.is_authenticated():
            redirect("/portal")
        return template("app/views/html/banco",
                        current_user=self.current_user(),
                        produtos=self.models.list_products())
