def batch_processing(batch):
    for user in batch:
        if user.get('age') > 25:
            yield user
