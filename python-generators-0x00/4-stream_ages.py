users_data = []  

def stream_user_ages():
    for user in users_data:
        yield user['age']
def calculate_average_age():
    total_age = 0
    count = 0
    for age in stream_user_ages():
        total_age += age
        count += 1
    return total_age / count if count > 0 else 0
