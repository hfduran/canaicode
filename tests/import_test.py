from services.gh_copilot_services import GhCopilotServices
from tests.constants import ONE_CONSTANT


def test_gh_service():
    GhCopilotServices.summarize_metrics()
    assert True

def test_constant():
    assert ONE_CONSTANT == 1