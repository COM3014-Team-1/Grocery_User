from app.application.user.getuser.getuservm import UserVM


def get_user_handler(user_id):
    from app import db  # Import db only when needed
    
    from app.infrastructure.models.user import User  # Now you can import your model
    
    User = create_user_model(db)
    user = User.query.get(user_id)
    if user:
        user_vm = UserVM(id=user.id, username=user.username, email=user.email)
        return user_vm.to_dict()
    return None
