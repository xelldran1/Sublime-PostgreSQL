#!/usr/bin/env python
from os.path import relpath
from platform import python_version
from sys import exc_info
from sublime import load_settings, error_message, message_dialog, packages_path, status_message
try:
    import sublime_helper
    import file
    open_file =sublime_helper.open_file
    SafeCommand =sublime_helper.SafeCommand
    pkg =sublime_helper.package(__file__)
    settings =pkg.settings
except Exception, e:
    package = relpath(__file__, packages_path())
    line = exc_info()[2].tb_lineno
    error_message("""python%s\n%s
line %s:\n
%s:\n%s""" % (
    python_version(), package, line,
    type(e), str(e)
    ))


def pgpass_tip():
    url ="www.postgresql.org/docs/9.2/static/libpq-pgpass.html"
    status_message(url)
    message_dialog("psql get password from pgpass")
    status_message(url)

if not file.exists(settings.user.file):
    file.copy(settings.file, settings.user.file)
    open_file(settings.user.file)
    message_dialog("edit PostgreSQL connection settings")
    pgpass_tip()


name ="PostgreSQL.sublime-settings"
s =load_settings(name)
error_message(s.get("database"))


class PostgresqlRunCommand(SafeCommand):
    def saferun(self):
        pass
        #psql=settings.default.psql
        #host=settings.default.host
        #port=settings.default.port
        #username=settings.default.username
        #open_file(settings.file)
        #pgpass_tip()


class PostgresqlDefaultSettingsCommand(SafeCommand):
    def saferun(self):
        open_file(settings.file)
        pgpass_tip()


class PostgresqlUserSettingsCommand(SafeCommand):
    def run(self):
        open_file(settings.user.file)
        pgpass_tip()