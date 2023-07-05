def use_app_context():
    from flask import current_app
    from wsgi import app
    
    

    with app.app_context():
        config = current_app.config
    return config

def sql_app_context(db):
    from wsgi import app

    with app.app_context():
        
        db.create_all()