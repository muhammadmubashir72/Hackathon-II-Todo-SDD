"""
Conversation service module.

This module implements conversation history operations with user isolation.
"""

from typing import List, Optional
from sqlmodel import Session, select
from datetime import datetime
from ..models.conversation import Conversation, Message
from ..models.user import User


class ConversationService:
    """Service class for conversation operations with user isolation."""

    @staticmethod
    def create_conversation(session: Session, user_id: int, title: Optional[str] = None) -> Conversation:
        """
        Create a new conversation for the specified user.

        Args:
            session: Database session
            user_id: ID of the user creating the conversation
            title: Optional title for the conversation

        Returns:
            Created Conversation object
        """
        conversation = Conversation(
            user_id=user_id,
            title=title or "New Conversation"
        )

        session.add(conversation)
        session.commit()
        session.refresh(conversation)

        return conversation

    @staticmethod
    def get_conversation_by_id(session: Session, conversation_id: int, user_id: int) -> Optional[Conversation]:
        """
        Retrieve a conversation by ID for the specified user.

        Args:
            session: Database session
            conversation_id: ID of the conversation to retrieve
            user_id: ID of the user requesting the conversation

        Returns:
            Conversation object if found and owned by user, None otherwise
        """
        statement = select(Conversation).where(
            Conversation.id == conversation_id, 
            Conversation.user_id == user_id
        )
        return session.exec(statement).first()

    @staticmethod
    def get_recent_conversations(session: Session, user_id: int, limit: int = 10) -> List[Conversation]:
        """
        Retrieve recent conversations for the specified user.

        Args:
            session: Database session
            user_id: ID of the user whose conversations to retrieve
            limit: Maximum number of conversations to return

        Returns:
            List of Conversation objects
        """
        statement = select(Conversation).where(
            Conversation.user_id == user_id
        ).order_by(Conversation.updated_at.desc()).limit(limit)
        
        return session.exec(statement).all()

    @staticmethod
    def add_message_to_conversation(
        session: Session, 
        conversation_id: int, 
        user_id: int, 
        role: str, 
        content: str,
        operation_performed: Optional[str] = None
    ) -> Optional[Message]:
        """
        Add a message to a conversation.

        Args:
            session: Database session
            conversation_id: ID of the conversation to add the message to
            user_id: ID of the user (for validation)
            role: Role of the message sender ('user' or 'assistant')
            content: Content of the message
            operation_performed: Optional operation that was performed

        Returns:
            Created Message object if successful, None if conversation not found or not owned by user
        """
        # First, verify that the conversation belongs to the user
        conversation = ConversationService.get_conversation_by_id(session, conversation_id, user_id)
        if not conversation:
            return None

        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            operation_performed=operation_performed
        )

        session.add(message)
        session.commit()
        session.refresh(message)

        return message

    @staticmethod
    def get_messages_for_conversation(session: Session, conversation_id: int, user_id: int, limit: int = 50) -> List[Message]:
        """
        Retrieve messages for a specific conversation.

        Args:
            session: Database session
            conversation_id: ID of the conversation
            user_id: ID of the user (for validation)
            limit: Maximum number of messages to return

        Returns:
            List of Message objects
        """
        # First, verify that the conversation belongs to the user
        conversation = ConversationService.get_conversation_by_id(session, conversation_id, user_id)
        if not conversation:
            return []

        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.timestamp.asc()).limit(limit)
        
        return session.exec(statement).all()

    @staticmethod
    def create_or_get_recent_conversation(session: Session, user_id: int, title: Optional[str] = None) -> Conversation:
        """
        Create a new conversation or return the most recent one if it exists.

        Args:
            session: Database session
            user_id: ID of the user
            title: Optional title for the conversation

        Returns:
            Conversation object
        """
        # Try to get the most recent conversation
        recent_conv = ConversationService.get_recent_conversations(session, user_id, limit=1)
        
        if recent_conv:
            return recent_conv[0]
        else:
            # Create a new conversation
            return ConversationService.create_conversation(session, user_id, title)