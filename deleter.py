import sys
from argparse import ArgumentParser

from gmail_deleter import GmailHandler


def run(args):
    gmail = GmailHandler(credentials_filepath=args.credentials_file, token_filepath=args.token_file)

    while True:
        print("\n1. Print authenticated user's email address and total number of messages in the mailbox."
              "\n2. Print a list of all labels associated with the authenticated user's mailbox."
              "\n3. Delete messages with a specified label."
              "\n4. Delete messages with a specified Gmail search filter (e.g. 'from:user@domain.com')"
              "\n5. Delete all messages in Trash."
              "\n6. Delete all messages in Spam."
              "\n7. Quit."
              "\n")

        try:
            choice = int(input("Choose from the listed options: "))
            if choice == 1:
                profile = gmail.get_user_profile(user_id="me")
                print(f"\n[*] You are authenticated as {profile['emailAddress']}"
                      f"\n[+] Found {profile['messagesTotal']} messages in the mailbox")
            elif choice == 2:
                labels = gmail.get_labels(user_id="me")
                print(f"\n[+] Found the following labels in the mailbox:\n"
                      f"{[i['id'] for i in labels]}\n")
            elif choice == 3:
                labels = input("\nPlease specify which label(s) you want to delete (comma separated if more than one): ")
                labels = labels.upper().split(",")
                messages = gmail.list_messages_with_label(user_id="me", label_ids=labels)
                delete_type = str(input("\nSoft (move to Trash) or Hard (permanent) Delete: "))
                try:
                    if "soft" in delete_type.lower():
                        for message in messages:
                            delete = gmail.delete_message(user_id="me", msg_id=message['id'], soft_delete=True)
                        print(f"\n[!] Soft deleted messages that were labeled with the following labels: {labels}")
                    elif "hard" in delete_type.lower():
                        message_ids = (i['id'] for i in messages)
                        batch_delete = gmail.batch_delete_messages(user_id="me", msg_ids=list(message_ids))
                        print(f"\n[!] Hard deleted messages that were labeled with the following labels: {labels}")
                except ValueError:
                    print("Invalid input! Try again.")
            elif choice == 4:
                query = input("\nPlease specify a Gmail search filter for messages you want to delete: ")
                query_messages = gmail.list_messages_matching_query(user_id="me", query=query)
                delete_type = str(input("\nSoft (move to Trash) or Hard (permanent) Delete: "))
                try:
                    if "soft" in delete_type.lower():
                        for message in query_messages:
                            delete = gmail.delete_message(user_id="me", msg_id=message['id'], soft_delete=True)
                        print(f"\n[!] Soft deleted messages that matched query: {query}")
                    elif "hard" in delete_type.lower():
                        query_msg_ids = (i['id'] for i in query_messages)
                        batch_delete = gmail.batch_delete_messages(user_id="me", msg_ids=list(query_msg_ids))
                        print(f"\n[!] Hard deleted messages that matched query: {query}")
                except ValueError:
                    print("Invalid input! Try again.")
            elif choice == 5:
                trash = gmail.list_messages_with_label(user_id="me", label_ids=["TRASH"])
                trash_ids = (i['id'] for i in trash)
                batch_delete = gmail.batch_delete_messages(user_id="me", msg_ids=list(trash_ids))
                print("\n[!] Trash has been emptied!")
            elif choice == 6:
                spam = gmail.list_messages_with_label(user_id="me", label_ids=["SPAM"])
                spam_ids = (i['id'] for i in spam)
                batch_delete = gmail.batch_delete_messages(user_id="me", msg_ids=list(spam_ids))
                print("\n[!] Spam has been emptied!")
            elif choice == 7:
                sys.exit(1)
            else:
                print("\n[*] Invalid choice! Please try again...")

        except ValueError:
            print("\n[*] Invalid input! Please select from the following options...")

def main():
    parser = ArgumentParser(
        prog="Gmail Message Deleter",
        description="No longer is there a need to manually delete your Gmail messages page by page! Programmatically clean your Gmail inbox and delete messages en masse by specific labels or Gmail search filter syntax!!"
    )
    parser.add_argument("-c", "--credentials", dest="credentials_file", help="location of credentials.json file (required for first run!)", type=str)
    parser.add_argument("-t", "--token", dest="token_file", help="location of token.json file (once obtained, can be used to authenticate without supplying credentials.json)", type=str)
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    run(args)

if __name__ == "__main__":
    main()
