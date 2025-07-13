import seed

def stream_users_in_batches(batch_size):
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) FROM user_data")
    total = cursor.fetchone()['COUNT(*)']
    
    for offset in range(0, total, batch_size):
        cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (batch_size, offset))
        yield cursor.fetchall()
    
    cursor.close()
    connection.close()

def batch_process(data, batch_size):
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]
