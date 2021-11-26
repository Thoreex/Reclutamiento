from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # import settings module
    from . import settings
    settings.init_app(app)

    # import utilities module
    from . import utilities
    utilities.init_app(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # import database module
    from . import db
    db.init_app(app)

    # import auth module
    from . import auth
    app.register_blueprint(auth.bp)

    # import jobs module
    from . import jobs
    app.register_blueprint(jobs.bp)
    app.add_url_rule('/', endpoint='index')

    # import profile, education and experience module
    from . import profile
    from . import education
    from . import experience
    profile.bp.register_blueprint(education.bp)
    profile.bp.register_blueprint(experience.bp)
    app.register_blueprint(profile.bp)

    return app