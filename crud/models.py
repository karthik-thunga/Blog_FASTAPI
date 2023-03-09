from .database import Base
from sqlalchemy import Column, Boolean, String, DateTime, Integer, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class PostModel(Base):
    __tablename__ = "posts"

    title = Column(String(50), nullable=False)
    content = Column(String(250), nullable=False)
    is_published = Column(Boolean, nullable=False, server_default="false")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    id = Column(Integer, primary_key=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("UserModel", back_populates="posts")
    post_comment = relationship("Comment", back_populates="post_related")
    tags = relationship("Tag", secondary="post_tags", back_populates="posts")

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, nullable=False, primary_key=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, server_default="true")
    is_superuser = Column(Boolean, server_default="false")
    posts = relationship("PostModel", back_populates="owner")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)

class Comment(Base):
    __tablename__ = "comments"

    comment = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
    post_related = relationship("PostModel", back_populates="post_comment")

class Tag(Base):
    __tablename__ = "tags"
    name = Column(String(50), nullable=False, primary_key=True)
    posts = relationship("PostModel", secondary="post_tags", back_populates="tags")

    def __repr__(self) -> str:
        return f"{self.name}"

    def __str__(self) -> str:
        return f"{self.name}"
    
class PostTag(Base):
    __tablename__ = 'post_tags'
    post_id = Column(Integer, ForeignKey('posts.id'), primary_key=True)
    tag_name = Column(String(50), ForeignKey('tags.name'), primary_key=True)