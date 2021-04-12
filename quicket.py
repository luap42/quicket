#! /usr/bin/python3

import sys
import tabulate

IS_ADMIN = len(sys.argv) == 2 and sys.argv[1] == ".admin"

print("QUICKET ADMIN")
print("The most simple ticket management system.")
print()
print("="*50)
print()
print("Choose a session username")
username = input("Your username: ")
print()
print("What do you want to do?\nChoose help for a list of commands.")

while True:
    print()
    query = input(">>> ").strip()

    if query == "help":
        print("List of commands")
        print("- help           Show this help")
        print("- list           List all tickets")
        print("- list open      List all open tickets")
        print("- goto <id>      Go to ticket with id=<id>")
        print("- new            Open new ticket")
        print("- quit           Quit this application")

    elif query == "list":
        with open("data/ticket_list", "r") as f:
            ticket_list = f.readlines()

        ticket_list = map(lambda i: i.strip(), ticket_list)

        print("Here is a list of all tickets:")

        ticket_list = [list(map(lambda j: j.strip(), i.split("|"))) for i in ticket_list]

        print(tabulate.tabulate(ticket_list, headers=["ID", "Author", "Title", "Status"]))

    elif query == "list open":
        with open("data/ticket_list", "r") as f:
            ticket_list = f.readlines()

        ticket_list = map(lambda i: i.strip(), ticket_list)

        print("Here is a list of all open tickets:")

        ticket_list = [list(map(lambda j: j.strip(), i.split("|"))) for i in ticket_list]
        ticket_list = [_ for _ in ticket_list if _[-1] == '+open']

        print(tabulate.tabulate(ticket_list, headers=["ID", "Author", "Title", "Status"]))

    elif query.startswith("goto "):
        query_id = int(query[len("goto"):])

        with open("data/tickets/" + str(query_id), "r") as f:
            ticket = f.read()

        print("Here is your ticket:")
        print()
        print()
        print(ticket)
        print()
        print()

        print("What do you want to do with this ticket?\nChoose help for a list of commands, leave to go to the main menu.")

        while True:
            print()
            ticket_query = input("[" + str(query_id) + "]> ").strip()

            if ticket_query == "help":
                print("List of commands in ticket mode")
                print("- reply           Reply to the ticket.")
                print("- show            Show the ticket again.")
                print("- close           Mark the ticket as closed.")
                print("- open            Mark the ticket as open.")

            elif ticket_query == "show":
                print("Here is your ticket:")
                print()
                print()
                print(ticket)
                print()
                print()

            elif ticket_query == "reply":
                print("Replying to the ticket.")
                print("Please add your message; three empty lines to continue")
                nlc = 0
                message = []
                while True:
                    message.append(input("$ ").strip())
                    if message[-1] == "":
                        nlc += 1
                    else:
                        nlc = 0

                    if nlc == 3:
                        message = message[:-3]
                        break

                ticket += '\n-----\n'
                ticket += '<' + username + '>\n\n'
                ticket += '\n'.join(message).strip()
                ticket += '\n'

                with open("data/tickets/" + str(query_id), "w") as f:
                    f.write(ticket)
                
                print("Okay.")

            elif ticket_query == "close":
                ticket += '\n-----\n'
                ticket += '<' + username + '>\n'
                ticket += 'ticket marked as +closed\n'
                ticket += '\n'

                with open("data/ticket_list", "r") as f:
                    ticket_list = f.readlines()

                ticket_list = map(lambda i: i.strip(), ticket_list)
                ticket_list = [list(map(lambda j: j.strip(), i.split("|"))) for i in ticket_list]
                ticket_list = [_ for _ in ticket_list if _[-1] == '+open']

                ticket_list = [[*i[:-1], '+closed'] if i[0] == str(query_id) else i for i in ticket_list]

                ticket_list = [' | '.join(i) for i in ticket_list]
                
                with open("data/tickets/" + str(query_id), "w") as f:
                    f.write(ticket)

                with open("data/ticket_list", "w") as f:
                    f.writelines(ticket_list)
                
                print("Okay.")

            elif ticket_query == "open":
                ticket += '\n-----\n'
                ticket += '<' + username + '>\n'
                ticket += 'ticket marked as +closed\n'
                ticket += '\n'

                with open("data/ticket_list", "r") as f:
                    ticket_list = f.readlines()

                ticket_list = map(lambda i: i.strip(), ticket_list)
                ticket_list = [list(map(lambda j: j.strip(), i.split("|"))) for i in ticket_list]
                ticket_list = [_ for _ in ticket_list if _[-1] == '+open']

                ticket_list = [[*i[:-1], '+closed'] if i[0] == str(query_id) else i for i in ticket_list]

                ticket_list = [' | '.join(i) for i in ticket_list]
                
                with open("data/tickets/" + str(query_id), "w") as f:
                    f.write(ticket)

                with open("data/ticket_list", "w") as f:
                    f.writelines(ticket_list)
                
                print("Okay.")
            
            elif ticket_query == "leave": break
            else:
                print("Command not found.")


    elif query == "quit": break
    else:
        print("Command not found.")
