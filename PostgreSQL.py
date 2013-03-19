#!/usr/bin/env python
from os.path import relpath
from platform import python_version
from sys import exc_info
from subprocess import PIPE, Popen, STDOUT
from sublime import error_message, message_dialog, packages_path, run_command
try:
    import sublime_helper
    selection =sublime_helper.selection
    substr =sublime_helper.substr
    PanelCommand =sublime_helper.command.PanelCommand
    SafeCommand =sublime_helper.command.SafeCommand
    pkg =sublime_helper.package(__file__)
    settings =pkg.settings
except Exception, e:
    path =relpath(__file__,packages_path())
    line =exc_info()[2].tb_lineno
    error_message("""python%s\n%s
line %s:\n
%s:\n%s""" % (
    python_version(), path,line,
    type(e), str(e)
    ))


def open_doc():
    url ="www.postgresql.org/docs/9.2/static/libpq-pgpass.html"
    run_command("open_url", {"url":url})


if not pkg.user.settings.exists:
    pass
    #pkg.user.settings.open()
    #message_dialog("edit PostgreSQL connection settings")
    #open_doc()


class PostgresqlBuildCommand(PanelCommand):
    def saferun(self):
        f =self.window.active_view().file_name()
        self.clear()
        process = Popen(
            [
                "psql",
                "-h",
                settings.host,
                "-p",
                settings.port,
                "-U",
                settings.username,
                "-f",
                f,
                settings.database
            ],
            stdout=PIPE,
            stdin=PIPE,
            stderr=STDOUT
        )
        self.show()
        stdout,stderr =process.communicate()
        if stdout:
            self.insert(stdout)
        if stderr:
            self.insert(stderr)


class PostgresqlDefaultSettingsCommand(SafeCommand):
    def saferun(self):
        pkg.settings.open()


class PostgresqlUserSettingsCommand(SafeCommand):
    def saferun(self):
        pkg.user.settings.open()