import json
import psycopg2
from psycopg2.extras import execute_values

# -----------------------------
# PostgreSQL connection setup
# -----------------------------
conn = psycopg2.connect(
    dbname="spotlight_ai",
    user="username",
    password="password",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# -----------------------------
# Insert businesses
# -----------------------------
business_fields = [
    "business_id",
    "name",
    "address",
    "city",
    "state",
    "postal_code",
    "latitude",
    "longitude",
    "stars",
    "review_count",
    "is_open",
    "categories",
]

batch_size = 10000
batch = []

with open("yelp_academic_dataset_business.json", "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)

        # Skip closed businesses
        if data.get("is_open", 0) != 1:
            continue

        row = [
            data.get("business_id"),
            data.get("name"),
            data.get("address"),
            data.get("city"),
            data.get("state"),
            data.get("postal_code"),
            data.get("latitude"),
            data.get("longitude"),
            data.get("stars"),
            data.get("review_count"),
            data.get("is_open"),
            data.get("categories"),
        ]
        batch.append(row)

        if len(batch) >= batch_size:
            execute_values(
                cur,
                "INSERT INTO data.businesses VALUES %s ON CONFLICT DO NOTHING",
                batch
            )
            conn.commit()
            batch = []

# Insert remaining
if batch:
    execute_values(
        cur,
        "INSERT INTO data.businesses VALUES %s ON CONFLICT DO NOTHING",
        batch
    )
    conn.commit()

cur.execute("SELECT business_id FROM data.businesses;")
valid_business_ids = set(row[0] for row in cur.fetchall())
print(f"Loaded {len(valid_business_ids)} valid business_ids.")

# -----------------------------
# Insert reviews
# -----------------------------
review_fields = [
    "review_id",
    "user_id",
    "business_id",
    "stars",
    "useful",
    "funny",
    "cool",
    "text",
    "date"
]

batch = []

with open("yelp_academic_dataset_review.json", "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)

        business_id = data.get("business_id")
        if business_id not in valid_business_ids:
            continue  # skip reviews for closed/nonexistent businesses
        # Replace newlines in review text
        text = data.get("text", "")
        if text:
            text = text.replace("\n", " ").replace("\r", " ")

        row = [
            data.get("review_id"),
            data.get("user_id"),
            data.get("business_id"),
            data.get("stars"),
            data.get("useful"),
            data.get("funny"),
            data.get("cool"),
            text,
            data.get("date"),
        ]

        batch.append(row)

        if len(batch) >= batch_size:
            execute_values(
                cur,
                """
                INSERT INTO data.reviews 
                (review_id, user_id, business_id, stars, useful, funny, cool, text, date)
                VALUES %s ON CONFLICT DO NOTHING
                """,
                batch
            )
            conn.commit()
            batch = []

# Insert remaining
if batch:
    execute_values(
        cur,
        """
        INSERT INTO data.reviews 
        (review_id, user_id, business_id, stars, useful, funny, cool, text, date)
        VALUES %s ON CONFLICT DO NOTHING
        """,
        batch
    )
    conn.commit()

cur.close()
conn.close()
print("Import complete!")
