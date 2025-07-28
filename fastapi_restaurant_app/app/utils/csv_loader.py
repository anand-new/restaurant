import pandas as pd
from app.models.restaurant import Restaurant
from sqlalchemy.orm import Session

def parse_and_create_restaurants(file, db: Session, created_by, tenant_id):
    df = pd.read_csv(file)
    restaurants = []
    
    for _, row in df.iterrows():
        restaurant = Restaurant(
            name=row['name'],
            address=row['address'],
            created_by=created_by,
            tenant_id=tenant_id  # ✅ assign tenant_id
        )
        db.add(restaurant)
        restaurants.append(restaurant)
    
    db.commit()
    return restaurants
