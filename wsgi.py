"""
Connects actual application to AWS server using gunicorn
"""
from app import APP

application = APP

if __name__ == "__main__":
    application.run()
