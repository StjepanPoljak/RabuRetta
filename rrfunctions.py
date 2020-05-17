from rrserver import *

class RabuRettaFunctions():

    def __init__(self):
        self.f_table = {
            "set_name" : (self.set_name, ()),
            "set_age" : (self.set_age, ()),
            "help" : (self.help, ()),
            "quit" : (self.quit, ()),
#            "kick_user" : (self.kick_user, ()),
            "set_admin" : (self.set_admin, ())
#            "kill_server": (self.kill_server, ()),
#            "start_game" : (self.start_game, ())
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

    def set_name(self, rrs, addr, msg):

        if addr not in rrs.users:

            return True

        else:

            rrs.users[addr].name = msg.data
            print("Set %s name to %s" % (addr, rrs.users[addr].name))
            rrs.send_request(
                    addr,
                    "input",
                    "Type in your age: ",
                    "set_age"
                    )

        return True

    def set_age(self, rrs, addr, msg):

        if addr not in rrs.users:

            return True

        else:

            rrs.users[addr].age = msg.data
            print("Set %s to age %s" % (rrs.users[addr].name, msg.data))

            if rrs.users[addr].priv == RabuRettaUserPrivilege.Admin:
                self.set_admin(rrs, addr, msg)

        return True

    def set_admin(self, rrs, addr, msg):

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

        return True

    def help(self, rrs, addr, msg):

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

    def quit(self, rrs, addr, msg):

        return False
