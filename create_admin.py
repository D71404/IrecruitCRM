from models.auth import Auth
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_admin():
    try:
        auth = Auth()
        username = "admin"
        email = "admin@crm.com"
        password = "Admin@123"

        # First, clean up any existing admin user
        logger.info("Cleaning up existing admin user...")
        auth.db.execute_update("DELETE FROM users WHERE username = %s", (username,))
        auth.db.execute_update("DELETE FROM stored_passwords WHERE user_id IN (SELECT id FROM users WHERE username = %s)", (username,))

        logger.info("Creating new admin user...")
        # Register admin user with proper password hashing
        success = auth.register_user(username, email, password, role='admin')

        if success:
            logger.info("Admin user created successfully!")
            # Verify the user was created
            user = auth.db.execute_one("SELECT * FROM users WHERE username = %s", (username,))
            if user:
                logger.info(f"Verified admin user exists with ID: {user['id']}")
                return True
        return False

    except Exception as e:
        logger.error(f"Error creating admin user: {str(e)}")
        return False

if __name__ == "__main__":
    result = create_admin()
    if not result:
        logger.error("Failed to create admin user!")
    else:
        logger.info("Admin user creation completed successfully!")