import seed

def stream_users_in_batches(batch_size):
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) FROM user_data")
    total = cursor.fetchone()['COUNT(*)']

    for offset in range(0, total, batch_size):
        cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (batch_size, offset))
        batch = cursor.fetchall()
        for user in batch:
            yield user  

    cursor.close()
    connection.close()

def batch_processing(batch):
    for user in batch:
        if user.get('age') > 25:
            yield user  
