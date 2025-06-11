# Mock Data Generation Configuration
from typing import Dict, List, Any

# Time period
MONTHS_TO_GENERATE = 6
SKIP_WEEKEND_PROBABILITY = 0.7  # 70% chance to skip weekends
SKIP_RANDOM_DAY_PROBABILITY = 0.15  # 15% chance to skip any random day

# Teams and their characteristics
TEAMS_CONFIG: Dict[str, Dict[str, Any]] = {
    "frontend-team": {
        "productivity": "medium",  # low, medium, high
        "copilot_adoption": "high",  # low, medium, high
        "repositories": ["web-app", "admin-dashboard", "mobile-web"],
        "developers": ["alice.smith", "bob.jones", "carol.wilson", "david.brown"],
        "languages": ["TypeScript", "JavaScript", "CSS", "HTML"]
    },
    "backend-team": {
        "productivity": "high",
        "copilot_adoption": "medium",
        "repositories": ["api-gateway", "user-service", "payment-service", "notification-service"],
        "developers": ["eve.davis", "frank.miller", "grace.taylor", "henry.anderson"],
        "languages": ["Python", "Java", "Go", "SQL"]
    },
    "data-team": {
        "productivity": "high",
        "copilot_adoption": "medium",
        "repositories": ["data-pipeline", "analytics-engine", "ml-models"],
        "developers": ["ivy.thomas", "jack.jackson", "karen.white", "leo.harris"],
        "languages": ["Python", "R", "SQL", "Scala"]
    },
    "devops-team": {
        "productivity": "medium",
        "copilot_adoption": "low",
        "repositories": ["infrastructure", "monitoring", "ci-cd-tools"],
        "developers": ["maya.martin", "noah.thompson", "olivia.garcia", "paul.martinez"],
        "languages": ["Python", "Bash", "YAML", "Terraform"]
    },
    "mobile-team": {
        "productivity": "medium",
        "copilot_adoption": "high",
        "repositories": ["ios-app", "android-app", "react-native-app"],
        "developers": ["quinn.robinson", "rachel.clark", "steve.rodriguez", "tina.lewis"],
        "languages": ["Swift", "Kotlin", "TypeScript", "Dart"]
    }
}

# Extract simple lists for backward compatibility
TEAMS: List[str] = list(TEAMS_CONFIG.keys())
REPOSITORIES: Dict[str, List[str]] = {team: config["repositories"] for team, config in TEAMS_CONFIG.items()}
DEVELOPERS: Dict[str, List[str]] = {team: config["developers"] for team, config in TEAMS_CONFIG.items()}
LANGUAGES: Dict[str, List[str]] = {team: config["languages"] for team, config in TEAMS_CONFIG.items()}

# Development tools
IDES: List[str] = ["VSCode", "IntelliJ", "PyCharm", "Xcode", "Android Studio"]
COPILOT_MODELS: List[str] = ["gpt-3.5-turbo", "gpt-4", "code-davinci-002"]

# Productivity multipliers based on team characteristics
PRODUCTIVITY_MULTIPLIERS: Dict[str, float] = {
    "low": 0.7,
    "medium": 1.0,
    "high": 1.4
}

COPILOT_ADOPTION_MULTIPLIERS: Dict[str, float] = {
    "low": 0.3,
    "medium": 0.65,
    "high": 0.85
}
