def stream_user_ages(users):
    for user in users:
        yield user['age']  

 
def calculate_average_age(users):
    total_age = 0
    count = 0
    for age in stream_user_ages(users):
        total_age += age
        count += 1
    return total_age / count if count > 0 else 0
