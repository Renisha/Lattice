from Cryptography_Utilities.encode import encode
from Cryptography_Utilities.encrypt import encrypt
from Cryptography_Utilities.decode import decode
from Cryptography_Utilities.decrypt import decrypt

class Member():

    def __init__(self, id, secret_key):
        self.id = id
        self.secret_key = secret_key
        self.group_id = None
        self.message_history = []

        print("\nMember {} created.".format(self.id))

    def set_group_id(self, group_id):
        self.group_id = group_id

    def set_secret_key(self, key):
        self.secret_key = key

    def add_message_to_group(self, group, message):

        """
        This is a function that handles the sending of a message by a member to the other members of the group that he is part of.
        The function returns True if message was written successfully, and False otherwise.
        """

        if self.group_id != group.id:
            print("You are not a member of group ", group.id, "!! \nCannot add messages to the group!!\n")
            return False

        print("Message being written by member {} to group {}: {}\n".format(self.id, group.id, message))

        group_key = group.get_group_key()
        encoded_message = encode(message)
        encoded_key = str(bin(group_key)[2:])
        encrypted_message = encrypt(encoded_message, encoded_key)
        group.add_message_to_group(encrypted_message)

        print("Message has been added to the group successfully.\n")

        return True

    def read_latest_message_of_group(self, group):

        """
        This is a function for a member to read the latest message that has been sent to his group. 
        Once a message has been added to a group successfully, this function must be called for every member of that group. 
        """

        if self.group_id != group.id:
            print("You are not a member of group ", group.id, "!! \nCannot read messages of the group!!\n")
            return False

        if len(group.messages) == 0:
            print("No messages have been sent to the group.\n")
            return False

        group_key = group.get_group_key()
        encoded_key = str(bin(group_key)[2:])
        encrypted_message = group.messages[-1]
        decrypted_message = decrypt(encrypted_message, encoded_key)
        decoded_message = decode(decrypted_message)

        print("Message read by member {}: {}\n".format(self.id, decoded_message))

        self.message_history.append((decoded_message, group.id))

        return True

    def add_member_to_group(self, member, group):

        """
        This function is for an admin to add a new member to the group. 
        If a group is empty, a member must be added to the group directly and that member will become the admin.
        The subsequent members must be added to the group through the admin. 
        """

        if self.id != group.admin_id:
            print("You are not an admin of the group!! \nCannot add the member to the group!!\n")
            return False

        if not group.add_member(member):
            return False

        return True

    def remove_member_from_group(self, member, group):

        """
        This function is for an admin to remove a member from the group. 
        """

        if self.id != group.admin_id:
            print("You are not an admin of the group!! \nCannot remove the member from the group!!\n")
            return False

        if not group.remove_member(member.id):
            return False

        return True