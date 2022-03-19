from __future__ import annotations

from pathlib import Path
from typing import List, Dict, Union, Generator
from googleapiclient.errors import HttpError
from gmail_deleter import GoogleClient


class GmailHandler:
    def __init__(self, credentials_filepath: Union[Path, str], token_filepath: Union[Path, str]):
        """
        Constructor for GmailHandler object which calls Gmail API endpoints.

        Args:
            credentials_filepath: file path to 'credentials.json' (required for first run)
            token_filepath: file path to 'token.json'
        """
        self.client = GoogleClient(credentials_filepath, token_filepath)

    def delete_message(self, user_id: str, msg_id: str, soft_delete: bool = True) -> Dict[str, Union[str, List]] | str:
        """Immediately delete a message with the given msg_id. Defaults to move to Trash (soft delete)

        Args:
            user_id: User's email address. The special value 'me' can be used to indicate the authenticated user.
            msg_id: ID of the message to delete
            soft_delete: Move to Trash (default). Set false to permanently delete message

        Returns:
            Soft delete returns a dict with message id, thread id, and a list of labels applied to message. Hard delete returns an empty response upon successful deletion
        """
        try:
            if soft_delete:
                response = self.client.service.users().messages().trash(userId=user_id, id=msg_id).execute()
                return response
            else:
                response = self.client.service.users().messages().delete(userId=user_id, id=msg_id).execute()
                return response
        except HttpError as error:
            raise f"An unhandled error occured: {error}"

    def batch_delete_messages(self, user_id: str, msg_ids: List[str]) -> str:
        """Immediately and permanently delete many messages by message id. Provides no guarantees that messages were not already deleted or even existed at all.

        Args:
            user_id: User's email address. The special value 'me' can be used to indicated the authenticated user.
            msg_ids: A list of message ids to batch delete

        Returns:
            An empty response upon successful deletion.
        """
        try:
            response = self.client.service.users().messages().batchDelete(userId=user_id, body={"ids": msg_ids}).execute()
            return response
        except HttpError as error:
            raise f"An unhandled error occured: {error}"

    def get_user_profile(self, user_id: str) -> Dict[str, Union[str, int]]:
        """Gets the current user's Gmail profile.

        Args:
            user_id: User's email address. The special value 'me' can be used to indicate the authenticated user.

        Returns:
            Dict object of the Gmail user's profile
        """
        profile = self.client.service.users().getProfile(userId=user_id).execute()
        return profile

    def get_labels(self, user_id: str) -> List[str]:
        """Get a list of all labels in the user's mailbox.

        Args:
            user_id: User's email address. The special value 'me' can be used to indicate the authenticated user.

        Returns:
            A list of all labels in the user's mailbox
        """
        label_result = self.client.service.users().labels().list(userId=user_id).execute()
        labels = label_result.get("labels", [])
        return labels

    def list_messages_with_label(self, user_id: str, label_ids: List[str]) -> Generator[Dict[str, str], None, None]:
        """List all messages of the user's mailbox with labelIds applied.

        Args:
            user_id: User's email address. The special value 'me' can be used to indicate the authenticated user.
            label_ids: Only return messages with these labelIds applied.

        Returns:
            Generator for dict of messages that have the required label(s) applied. Note that the returned dict contains only message ids and thread ids.
        """
        try:
            response = self.client.service.users().messages().list(userId=user_id, labelIds=label_ids).execute()
            if "messages" in response:
                for message in response['messages']:
                    yield message

            while "nextPageToken" in response:
                page_token = response['nextPageToken']
                response = self.client.service.users().messages().list(userId=user_id, labelIds=label_ids, pageToken=page_token).execute()
                if "messages" in response:
                    for message in response['messages']:
                        yield message
        except HttpError as error:
            raise f"[*] An unhandled error occured: {error}"

    def list_messages_matching_query(self, user_id: str, query: str = None) -> Generator[Dict[str, str], None, None]:
        """List all messages of the user's mailbox matching the query.

        Args:
            user_id: User's email address. The special value 'me' can be used to indicate the authenticated user.
            query: String used to filter messages returned. (e.g. 'from:user@domain.com' for messages from a particular sender)

        Returns:
            Generator for dict of messages that match the criteria of the query. Note that the returned dict contains only message ids and thread ids.
        """
        try:
            response = self.client.service.users().messages().list(userId=user_id, q=query).execute()

            if "messages" in response:
                for message in response['messages']:
                    yield message

            while "nextPageToken" in response:
                page_token = response['nextPageToken']
                response = self.client.service.users().messages().list(userId=user_id, q=query, pageToken=page_token).execute()
                for message in response['messages']:
                    yield message
        except HttpError as error:
            raise f"[*] An unhandled error occured: {error}"

    def get_message(self, user_id: str, msg_id: str) -> Dict[str, Union[str, int, Dict, List]]:
        """Get a message with a given id.

        Args:
            user_id: User's email address. The special value 'me' can be used to indicate the authenticated user.
            msg_id: The id of the message required.

        Returns:
            A message.
        """
        try:
            message = self.client.service.users().messages().get(userId=user_id, id=msg_id).execute()
            return message
        except HttpError as error:
            raise f"An unhandled error occured: {error}"
