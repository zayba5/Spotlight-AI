from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func, JSON
from sqlalchemy.orm import relationship
from .db import Base


class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True, index=True)
	external_id = Column(String(128), unique=True, index=True, nullable=False)
	display_name = Column(String(128), nullable=True)
	created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

	preferences = relationship("UserPreference", back_populates="user", cascade="all, delete-orphan")
	conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")


class UserPreference(Base):
	__tablename__ = "user_preferences"

	id = Column(Integer, primary_key=True, index=True)
	user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
	key = Column(String(64), nullable=False, index=True)
	value = Column(String(256), nullable=False)
	created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
	updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

	user = relationship("User", back_populates="preferences")


class Conversation(Base):
	__tablename__ = "conversations"

	id = Column(Integer, primary_key=True, index=True)
	user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
	title = Column(String(256), nullable=True)
	created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

	user = relationship("User", back_populates="conversations")
	messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
	__tablename__ = "messages"

	id = Column(Integer, primary_key=True, index=True)
	conversation_id = Column(Integer, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True)
	role = Column(String(16), nullable=False)  # user | assistant | system
	content = Column(Text, nullable=False)
	citations = Column(JSON, nullable=True)  # list of {id, title, url}
	created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

	conversation = relationship("Conversation", back_populates="messages")



