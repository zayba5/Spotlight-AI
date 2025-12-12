# test_db.py
from backend.database.db import SessionLocal
from backend.database import models

db = SessionLocal()

# Query first restaurant
restaurant = db.query(models.Restaurant).first()
if restaurant:
    print(f"Restaurant ID: {restaurant.id}, Name: {restaurant.name}, Address: {restaurant.address}")
else:
    print("No restaurants found in DB.")

db.close()
