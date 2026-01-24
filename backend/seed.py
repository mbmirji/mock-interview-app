from app.database import SessionLocal
from app.models import User

def seed_anonymous_user():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == 1).first()
        if not user:
            print("Creating anonymous user...")
            anon_user = User(
                id=1,
                email="anonymous@mock-interview.app",
                username="anonymous",
                full_name="Anonymous User",
                hashed_password="not-used",
                is_active=True
            )
            db.add(anon_user)
            db.commit()
            print("Anonymous user created.")
        else:
            print("Anonymous user already exists.")
    except Exception as e:
        print(f"Error seeding user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_anonymous_user()
