# @pytest.fixture(scope="session", autouse=True)
# def _default_session_fixture(tmpdir_factory):
#     tmp_path = tmpdir_factory.mktemp("eeauth").join("credentials.json")

#     with patch("eeauth.user_registry.REGISTRY_PATH", tmp_path):
#         yield
