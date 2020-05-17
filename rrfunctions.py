from rrserver import *
import re

class RabuRettaFunctions():

    def __init__(self):
        self.f_table = {
            "set_name" : self.set_name,
            "set_age" : self.set_age,
            "help" : self.help,
            "quit" : self.quit,
            "kick" : self.kick,
            "set_admin" : self.set_admin,
            "list": self.list
#            "start" : self.start
                }

    def new_conn(self, rrs, addr):

        if addr not in rrs.users:

            return True

        rrs.users[addr].priv = \
                RabuRettaUserPrivilege.Admin if len(rrs.users) == 1 \
                else RabuRettaUserPrivilege.Unassigned

        rrs.send_request(
                addr,
                "input",
                "Type in your name: ",
                "set_name"
                )

        return True

    def set_name(self, rrs, addr, name):

        if addr not in rrs.users:

            return True

        else:
            rrs.users[addr].name = name
            print("Set %s name to %s" % (addr, rrs.users[addr].name))
            rrs.send_request(
                    addr,
                    "input",
                    "Type in your age: ",
                    "set_age"
                    )

        return True

    def set_age(self, rrs, addr, age):

        if addr not in rrs.users:

            return True

        if re.search("^[0-9]+$", age) is None:

            self.minor_error(rrs, addr, "Please provide numerical value.")

            return True

        rrs.users[addr].age = int(age)
        print(
                "Set %s to age %d" %
                (rrs.users[addr].name, rrs.users[addr].age)
                )

        if rrs.users[addr].priv == RabuRettaUserPrivilege.Admin:
            self.set_admin(rrs, addr)

        return True

    def set_admin(self, rrs, addr):

        if addr not in rrs.users:

            return True

        self.admin_console(rrs, addr)

        return True

    def admin_console(self, rrs, addr):
        rrs.send_request(
                addr,
                "input",
                "[admin]#: ",
                ""
                )

    def minor_error(self, rrs, addr, msg):

        rrs.send_request(
                addr,
                "error",
                msg,
                "retry"
                )

    def help(self, rrs, addr):
        help_string = """
        list\t\tlist users
        kick <user>\tkick user
        start\t\tstart game
        quit\t\tshut down server
        """

        rrs.send_request(
                addr,
                "output",
                help_string,
                "help"
                )

        self.admin_console(rrs, addr)

        return True

    def quit(self, rrs, addr):

        return False

    def kick(self, rrs, addr, user):
        to_kick=None

        for uaddr, userobj in rrs.users.items():

            if userobj.name == user:

                if addr == uaddr:
                    self.minor_error(
                            rrs,
                            addr,
                            "Cannot kick yourself from the server."
                            )
                    break

                rrs.send_request(
                        uaddr,
                        "kick",
                        "You have been kicked from server.",
                        ""
                        )
                to_kick = "User %s: %s has been " % uaddr, user
                to_kick += "kicked from the server."

                break

            if to_kick is not None:
                self.send_request(
                        addr,
                        "output",
                        to_kick,
                        "kick"
                        )
            else:
                self.minor_error(rrs, addr, "Invalid user name: %s" % user)

        self.admin_console(rrs, addr)

    def list(self, rrs, addr):
        list_string="User list:\n\n"

        for uaddr, user in rrs.users.items():
            list_string += "\t%s: %s (%d)\n" % (uaddr, user.name, user.age)

        rrs.send_request(
                addr,
                "output",
                list_string,
                "list"
                )

        self.admin_console(rrs, addr)
