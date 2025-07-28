def run_dummy_prediction(restaurant_ids):
    # In real case: fetch historical orders and use ML model
    return [
        {"restaurant_id": rid, "predicted_demand": 120 + i * 5}
        for i, rid in enumerate(restaurant_ids)
    ]
