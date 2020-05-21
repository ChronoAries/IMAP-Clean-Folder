import imap_tools
from datetime import datetime, timedelta, timezone


# User imap information
user = "Insert Username"
password = "Insert Password"
imap_url = "Insert IMAP server name"
clean_folder = "Insert name of folder that the program will run in"
trash = "Insert name of trash folder"

# List of all emails groups
newsletters = ["abercrombie@e.abercrombie.com", "kfc@em.kfc.ca"]

# Specific cases where those emails should not be deleted
exception_subject = ["receipts", "coupons"]

# The max date of which everything that follows the arguments above will be deleted
max_date = datetime.now(tz=timezone.utc) - timedelta(days=7)

with imap_tools.MailBox(imap_url).login(user, password, clean_folder) as mailbox:
    def clean_inbox():
        deleted = 0
        try:
            for msg in mailbox.fetch():
                move = False
                msg_date = msg.date.astimezone(tz=timezone.utc)
                if msg_date <= max_date:
                    for emails in newsletters:
                        if move:
                            break
                        if msg.from_.lower() == emails:
                            for subject in exception_subject:
                                if msg.subject.lower() not in subject:
                                    mailbox.move(msg.uid, trash)
                                    move = True
                                    deleted += 1
                                    break
        except imap_tools.utils.UnexpectedCommandStatusError:
            print("Complete! Deleted" + str(deleted) + " emails")
