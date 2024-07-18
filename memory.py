from datetime import datetime
from typing import Any

from langchain_community.chat_message_histories.sql import BaseMessageConverter
from langchain.schema import AIMessage, BaseMessage, HumanMessage, SystemMessage
from sqlalchemy import Column, DateTime, Integer, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class CustomMessage(Base):
    """
    SQLAlchemy model representing custom messages in the UMM search memory.
    """
    __tablename__ = "limebot_memory"  # instances of the `CustomMessage` class will be mapped to rows in the `limebot_memory` table
    id = Column(Integer, primary_key=True)    # unique identifier for each row in the table, and it must be unique and not null.
    session_id = Column(Text)  # It will store the session identifier for each message, which is typically a string.
    type = Column(Text)  # This column will store the type of message (e.g., "human", "ai", "system").
    content = Column(Text)  # This column will store the actual content of the message.
    created_at = Column(DateTime)  # This column will store the timestamp of when the message was created.
    author_email = Column(Text)  #  This column will store the email address of the message author.

class CustomMessageConverter(BaseMessageConverter):
    """
    Converter class for custom messages between SQL model and language model representations.
    """
    def __init__(self, author_email: str):
        """
        The CustomMessageConverter class is designed to handle the conversion of custom messages between SQL model 
        representations and language model representations. The constructor (__init__) initializes the class with the email 
        of the message author, storing this information in an instance variable for use in the class's methods.
        By initializing the author_email, the class can use this information when creating or converting messages, 
        ensuring that the author's email is consistently included in the message data. This setup is crucial for 
        applications that need to track the source of messages and maintain accurate records of message metadata.
        Args:
            author_email (str): Email of the message author.
        """
        self.author_email = author_email # This means that each instance of CustomMessageConverter will store the 
                                         # email of the author, which can be used in other methods of the class.

    def from_sql_model(self, sql_message: Any) -> BaseMessage:
        """
        Convert a SQL message model to a language model representation.

        Args:
            sql_message (Any): SQL message model.

        Returns:
            BaseMessage: Language model representation of the message.
        """
        if sql_message.type == "human":
            """
            `HumanMessage` is presumably a class representing messages from human users.
            """
            return HumanMessage(
                content=sql_message.content,
            )
        elif sql_message.type == "ai":
            """
            `AIMessage` is presumably a class representing messages generated by an AI.
            """
            return AIMessage(
                content=sql_message.content,
            )
        elif sql_message.type == "system":
            """
            `SystemMessage` is presumably a class representing system-generated messages.
            """
            return SystemMessage(
                content=sql_message.content,
            )
        else:
            # print the unknown message type
            raise ValueError(f"Unknown message type: {sql_message.type}")
        
    def to_sql_model(self, message: BaseMessage, session_id: str) -> Any:
        """
        this method converts a language model message into a SQL model representation, with message being the input language 
        model message and session_id being the associated session ID.
        Args:
            message (BaseMessage): Language model representation of the message.
            session_id (str): Session ID associated with the message.

        Returns:
            Any: SQL model representation of the message.
        """
        now = datetime.now() # This timestamp will be used to set the created_at field in the SQL model.

        # The to_sql_model method in the CustomMessageConverter class converts a language model message into a 
        # SQL model representation suitable for storage in a database.
        return CustomMessage(
            session_id=session_id,
            type=message.type,
            content=message.content,
            created_at=now,
            author_email=self.author_email,
        )

    def get_sql_model_class(self) -> Any:
        """
        This method allows other parts of the application to access the CustomMessage class definition, which can be 
        useful for tasks such as querying the database, creating new instances of the model, or performing database schema 
        operations.
        This method encapsulates the knowledge of which SQL model class is used for custom messages, providing a clear 
        and consistent way to retrieve this information throughout the application.
        
        Returns:
            Any: SQL model class for custom messages.
        """
        return CustomMessage
