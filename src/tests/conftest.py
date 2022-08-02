
import pytest
from src.app import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SOURCES_URL": "https://api1.com?member_id={member_id} https://api2.com?member_id={member_id}"
                       " https://api3.com?member_id={member_id}",
        "SOURCES_URL_TIMEOUT": 1,
        "DEFAULT_AGGREGATION_STRATEGY": "AVG"
    })

    # other setup can go here
    yield app
    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
