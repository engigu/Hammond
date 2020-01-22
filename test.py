from celery_senders.sender import test_celery

if __name__ == "__main__":
    test_celery.delay()
    