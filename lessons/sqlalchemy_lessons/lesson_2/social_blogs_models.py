from typing import Optional

from sqlalchemy import DateTime, Float, ForeignKeyConstraint, Index, Integer, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase


class Base(DeclarativeBase):
    __abstract__ = True


class Categories(Base):
    __tablename__ = 'categories'

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(50), nullable=False)
    description = mapped_column(String(200))

    polls: Mapped[list['Polls']] = relationship('Polls', uselist=True, back_populates='category')
    products: Mapped[list['Products']] = relationship('Products', uselist=True, back_populates='category')


class Role(Base):
    __tablename__ = 'role'

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(20), nullable=False)

    user: Mapped[list['User']] = relationship('User', uselist=True, back_populates='role')


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        Index('username', 'username', unique=True),
    )

    username = mapped_column(String(80), nullable=False)
    is_active = mapped_column(TINYINT(1), nullable=False)
    is_admin = mapped_column(TINYINT(1), nullable=False)
    id = mapped_column(Integer, primary_key=True)
    created_at = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))


class Polls(Base):
    __tablename__ = 'polls'
    __table_args__ = (
        ForeignKeyConstraint(['category_id'], ['categories.id'], name='polls_category_id_fkey'),
        Index('polls_category_id_fkey', 'category_id')
    )

    title = mapped_column(String(255), nullable=False)
    start_date = mapped_column(DateTime, nullable=False)
    is_active = mapped_column(TINYINT(1), nullable=False)
    is_anonymous = mapped_column(TINYINT(1), nullable=False)
    id = mapped_column(Integer, primary_key=True)
    created_at = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    description = mapped_column(Text)
    end_date = mapped_column(DateTime)
    category_id = mapped_column(Integer)

    category: Mapped[Optional['Categories']] = relationship('Categories', back_populates='polls')
    poll_options: Mapped[list['PollOptions']] = relationship('PollOptions', uselist=True, back_populates='poll')
    poll_statistics: Mapped[list['PollStatistics']] = relationship('PollStatistics', uselist=True, back_populates='poll')


class Products(Base):
    __tablename__ = 'products'
    __table_args__ = (
        ForeignKeyConstraint(['category_id'], ['categories.id'], name='products_ibfk_1'),
        Index('category_id', 'category_id')
    )

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(100), nullable=False)
    price = mapped_column(Float, nullable=False)
    in_stock = mapped_column(TINYINT(1))
    category_id = mapped_column(Integer)

    category: Mapped[Optional['Categories']] = relationship('Categories', back_populates='products')


class User(Base):
    __tablename__ = 'user'
    __table_args__ = (
        ForeignKeyConstraint(['role_id'], ['role.id'], name='user_ibfk_1'),
        Index('role_id', 'role_id')
    )

    id = mapped_column(Integer, primary_key=True)
    first_name = mapped_column(String(25), nullable=False)
    email = mapped_column(String(75), nullable=False)
    password = mapped_column(String(255), nullable=False)
    repeat_password = mapped_column(String(255), nullable=False)
    last_name = mapped_column(String(30))
    phone = mapped_column(String(45))
    role_id = mapped_column(Integer)
    rating = mapped_column(Float, server_default=text("'0'"))
    deleted = mapped_column(TINYINT(1), server_default=text("'0'"))
    created_at = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = mapped_column(TIMESTAMP)
    deleted_at = mapped_column(TIMESTAMP)

    role: Mapped[Optional['Role']] = relationship('Role', back_populates='user')
    news: Mapped[list['News']] = relationship('News', uselist=True, back_populates='author')
    comment: Mapped[list['Comment']] = relationship('Comment', uselist=True, back_populates='author')


class News(Base):
    __tablename__ = 'news'
    __table_args__ = (
        ForeignKeyConstraint(['author_id'], ['user.id'], name='news_ibfk_1'),
        Index('author_id', 'author_id')
    )

    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String(100), nullable=False)
    content = mapped_column(Text, nullable=False)
    author_id = mapped_column(Integer)
    moderated = mapped_column(TINYINT(1), server_default=text("'0'"))
    created_at = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = mapped_column(TIMESTAMP)

    author: Mapped[Optional['User']] = relationship('User', back_populates='news')
    comment: Mapped[list['Comment']] = relationship('Comment', uselist=True, back_populates='news')


class PollOptions(Base):
    __tablename__ = 'poll_options'
    __table_args__ = (
        ForeignKeyConstraint(['poll_id'], ['polls.id'], name='poll_options_ibfk_1'),
        Index('poll_id', 'poll_id')
    )

    poll_id = mapped_column(Integer, nullable=False)
    text_ = mapped_column('text', String(255), nullable=False)
    id = mapped_column(Integer, primary_key=True)
    created_at = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))

    poll: Mapped['Polls'] = relationship('Polls', back_populates='poll_options')
    option_statistics: Mapped[list['OptionStatistics']] = relationship('OptionStatistics', uselist=True, back_populates='option')


class PollStatistics(Base):
    __tablename__ = 'poll_statistics'
    __table_args__ = (
        ForeignKeyConstraint(['poll_id'], ['polls.id'], name='poll_statistics_ibfk_1'),
        Index('poll_id', 'poll_id', unique=True)
    )

    poll_id = mapped_column(Integer, nullable=False)
    total_votes = mapped_column(Integer, nullable=False)
    unique_voters = mapped_column(Integer, nullable=False)
    id = mapped_column(Integer, primary_key=True)
    created_at = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))

    poll: Mapped['Polls'] = relationship('Polls', back_populates='poll_statistics')
    option_statistics: Mapped[list['OptionStatistics']] = relationship('OptionStatistics', uselist=True, back_populates='poll_stats')


class Comment(Base):
    __tablename__ = 'comment'
    __table_args__ = (
        ForeignKeyConstraint(['author_id'], ['user.id'], name='comment_ibfk_1'),
        ForeignKeyConstraint(['news_id'], ['news.id'], name='comment_ibfk_2'),
        Index('author_id', 'author_id'),
        Index('news_id', 'news_id')
    )

    id = mapped_column(Integer, primary_key=True)
    content = mapped_column(Text, nullable=False)
    author_id = mapped_column(Integer)
    news_id = mapped_column(Integer)
    created_at = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = mapped_column(TIMESTAMP)

    author: Mapped[Optional['User']] = relationship('User', back_populates='comment')
    news: Mapped[Optional['News']] = relationship('News', back_populates='comment')


class OptionStatistics(Base):
    __tablename__ = 'option_statistics'
    __table_args__ = (
        ForeignKeyConstraint(['option_id'], ['poll_options.id'], name='option_statistics_ibfk_1'),
        ForeignKeyConstraint(['poll_stats_id'], ['poll_statistics.id'], name='option_statistics_ibfk_2'),
        Index('option_id', 'option_id'),
        Index('poll_stats_id', 'poll_stats_id')
    )

    poll_stats_id = mapped_column(Integer, nullable=False)
    option_id = mapped_column(Integer, nullable=False)
    votes_count = mapped_column(Integer, nullable=False)
    percentage = mapped_column(Float, nullable=False)
    id = mapped_column(Integer, primary_key=True)
    created_at = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))

    option: Mapped['PollOptions'] = relationship('PollOptions', back_populates='option_statistics')
    poll_stats: Mapped['PollStatistics'] = relationship('PollStatistics', back_populates='option_statistics')
