from sqlalchemy import (
	Column,
	DateTime,
	Float,
	ForeignKey,
	Integer,
	String,
	Text,
)
from sqlalchemy.orm import relationship

from .db import Base


class Business(Base):
	"""
	Business table mapped to `data.businesses`.

	Update column names/types to match your actual `data.businesses` table.
	"""

	__tablename__ = "businesses"
	__table_args__ = {"schema": "data"}

	business_id = Column(String, primary_key=True, index=True)
	name = Column(String, nullable=False)
	address = Column(String, nullable=True)
	city = Column(String, nullable=True)
	state = Column(String, nullable=True)
	postal_code = Column(String, nullable=True)
	latitude = Column(Float, nullable=True)
	longitude = Column(Float, nullable=True)
	stars = Column(Float, nullable=True)
	review_count = Column(Integer, nullable=True)
	categories = Column(String, nullable=True)

	reviews = relationship("Review", back_populates="business")


class Review(Base):
	"""
	Review table mapped to `data.reviews`, linked to `data.businesses`.

	Update column names/types to match your actual `data.reviews` table.
	"""

	__tablename__ = "reviews"
	__table_args__ = {"schema": "data"}

	review_id = Column(String, primary_key=True, index=True)
	business_id = Column(
		String,
		ForeignKey("data.businesses.business_id"),
		index=True,
		nullable=False,
	)
	stars = Column(Float, nullable=True)
	text = Column(Text, nullable=True)
	date = Column(DateTime, nullable=True)
	business = relationship("Business", back_populates="reviews")
