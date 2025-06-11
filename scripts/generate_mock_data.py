#!/usr/bin/env python3
"""
Mock Data Generator for Copilot and Coding Performance Analysis System

This script generates 6 months of mock data for:
- Commit metrics (coding activity)
- Copilot code metrics (code suggestions and acceptances)
- Copilot chat metrics (chat interactions)

The data is generated with realistic patterns and correlations between
coding intensity and Copilot usage.
"""

import os
import sys
import uuid
import random
from datetime import datetime, timedelta, timezone
from typing import List
import logging

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy.orm import Session
from src.infrastructure.database.connection.database_connection import SessionLocal
from src.infrastructure.database.raw_commit_metrics.postgre.dtos.model import RawCommitMetrics
from src.infrastructure.database.raw_copilot_code_metrics.postgre.dtos.model import RawCopilotCodeMetrics
from src.infrastructure.database.raw_copilot_chat_metrics.postgre.dtos.model import RawCopilotChatMetrics
from src.infrastructure.database.init_db import create_tables

# Import configuration
from mock_data_config import (
    MONTHS_TO_GENERATE, SKIP_WEEKEND_PROBABILITY, SKIP_RANDOM_DAY_PROBABILITY,
    TEAMS, REPOSITORIES, DEVELOPERS, LANGUAGES, TEAMS_CONFIG,
    IDES, COPILOT_MODELS,
    PRODUCTIVITY_MULTIPLIERS, COPILOT_ADOPTION_MULTIPLIERS
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_working_days(start_date: datetime, end_date: datetime) -> List[datetime]:
    """Generate list of working days with some randomness for skipping days."""
    days = []
    current = start_date
    
    while current <= end_date:
        # Skip weekends with higher probability
        if current.weekday() >= 5:  # Saturday = 5, Sunday = 6
            if random.random() > SKIP_WEEKEND_PROBABILITY:
                days.append(current)
        else:
            # Skip random weekdays occasionally
            if random.random() > SKIP_RANDOM_DAY_PROBABILITY:
                days.append(current)
        
        current += timedelta(days=1)
    
    return days


def generate_commit_id() -> str:
    """Generate a realistic Git commit hash."""
    return ''.join(random.choices('0123456789abcdef', k=40))


def generate_commit_metrics(db: Session, days: List[datetime]) -> None:
    """Generate commit metrics data."""
    logger.info("Generating commit metrics...")
    
    commit_records = []
    used_combinations = set()  # Track (hash, repo, language) combinations
    
    for day in days:
        for team in TEAMS:
            repos = REPOSITORIES[team]
            devs = DEVELOPERS[team]
            langs = LANGUAGES[team]
            
            # Get team characteristics
            team_config = TEAMS_CONFIG[team]
            productivity_mult = PRODUCTIVITY_MULTIPLIERS[team_config["productivity"]]
            
            # Number of commits per team per day (varies by team productivity)
            base_commits = 6 if team in ["backend-team", "data-team"] else 4
            daily_commits = int(random.randint(1, base_commits * 2) * productivity_mult)
            
            for _ in range(daily_commits):
                repo = random.choice(repos)
                author = random.choice(devs)
                language = random.choice(langs)
                
                # Generate unique hash for this repo/language combination
                commit_hash = None
                max_attempts = 10
                for attempt in range(max_attempts):
                    temp_hash = generate_commit_id()
                    combination = (temp_hash, repo, language)
                    if combination not in used_combinations:
                        used_combinations.add(combination)
                        commit_hash = temp_hash
                        break
                    if attempt == max_attempts - 1:
                        logger.warning(f"Could not generate unique combination after {max_attempts} attempts")
                        commit_hash = temp_hash  # Use the last generated hash anyway
                
                if commit_hash is None:
                    continue  # Skip this commit if we couldn't generate a hash
                
                # Generate realistic code changes
                # Larger commits during weekdays, smaller on weekends
                if day.weekday() < 5:  # Weekday
                    base_added = 50
                    base_removed = 20
                else:  # Weekend
                    base_added = 20
                    base_removed = 5
                
                added_lines = int(random.randint(5, base_added * 4) * productivity_mult)
                removed_lines = int(random.randint(0, base_removed * 3) * productivity_mult)
                
                commit = RawCommitMetrics(
                    id=str(uuid.uuid4()),
                    hash=commit_hash,
                    repository_name=repo,
                    repository_team=team,
                    date=day.replace(
                        hour=random.randint(9, 18),
                        minute=random.randint(0, 59),
                        second=random.randint(0, 59)
                    ),
                    author_name=author,
                    author_teams=team,
                    language=language,
                    added_lines=added_lines,
                    removed_lines=removed_lines,
                    created_at=datetime.now(timezone.utc)
                )
                commit_records.append(commit)
    
    # Batch insert for better performance
    logger.info(f"Inserting {len(commit_records)} commit records...")
    db.add_all(commit_records)
    db.commit()
    logger.info("Commit metrics inserted successfully!")


def generate_copilot_code_metrics(db: Session, days: List[datetime]) -> None:
    """Generate Copilot code metrics data."""
    logger.info("Generating Copilot code metrics...")
    
    code_records = []
    
    for day in days:
        for team in TEAMS:
            langs = LANGUAGES[team]
            team_size = len(DEVELOPERS[team])
            
            # Get team characteristics
            team_config = TEAMS_CONFIG[team]
            copilot_mult = COPILOT_ADOPTION_MULTIPLIERS[team_config["copilot_adoption"]]
            productivity_mult = PRODUCTIVITY_MULTIPLIERS[team_config["productivity"]]
            
            # Generate unique IDE/model combinations for this team/day
            # Unique constraint: team_name, date, ide, copilot_model
            num_combinations = random.randint(1, min(3, len(IDES) * len(COPILOT_MODELS)))
            
            # Create all possible IDE/model combinations and sample from them
            all_combinations = [(ide, model) for ide in IDES for model in COPILOT_MODELS]
            selected_combinations = random.sample(all_combinations, num_combinations)
            
            for ide, model in selected_combinations:
                language = random.choice(langs)
                
                # Calculate active users (subset of team, influenced by copilot adoption)
                max_users = max(1, int(team_size * copilot_mult))
                active_users = random.randint(1, max_users)
                
                # Generate suggestions and acceptances based on team characteristics
                base_suggestions = int(random.randint(30, 150) * productivity_mult * copilot_mult)
                
                # Acceptance rate varies by team experience and copilot adoption
                if team_config["copilot_adoption"] == "high":
                    acceptance_rate = random.uniform(0.45, 0.75)  # High adoption = more accepting
                elif team_config["copilot_adoption"] == "medium":
                    acceptance_rate = random.uniform(0.35, 0.65)  # Medium adoption = moderate acceptance
                else:
                    acceptance_rate = random.uniform(0.25, 0.55)  # Low adoption = more selective
                
                code_suggestions = base_suggestions * active_users
                code_acceptances = int(code_suggestions * acceptance_rate)
                
                # Lines suggested/accepted correlation
                avg_lines_per_suggestion = random.uniform(2, 8)
                lines_suggested = int(code_suggestions * avg_lines_per_suggestion)
                lines_accepted = int(code_acceptances * avg_lines_per_suggestion * random.uniform(0.8, 1.2))
                
                code_metric = RawCopilotCodeMetrics(
                    id=str(uuid.uuid4()),
                    team_name=team,
                    date=day.replace(hour=12, minute=0, second=0, microsecond=0),  # Normalized time
                    ide=ide,
                    copilot_model=model,
                    language=language,
                    total_users=active_users,
                    code_acceptances=code_acceptances,
                    code_suggestions=code_suggestions,
                    lines_accepted=lines_accepted,
                    lines_suggested=lines_suggested,
                    created_at=datetime.now(timezone.utc)
                )
                code_records.append(code_metric)
    
    logger.info(f"Inserting {len(code_records)} Copilot code metrics...")
    db.add_all(code_records)
    db.commit()
    logger.info("Copilot code metrics inserted successfully!")


def generate_copilot_chat_metrics(db: Session, days: List[datetime]) -> None:
    """Generate Copilot chat metrics data."""
    logger.info("Generating Copilot chat metrics...")
    
    chat_records = []
    
    for day in days:
        for team in TEAMS:
            team_size = len(DEVELOPERS[team])
            
            # Get team characteristics
            team_config = TEAMS_CONFIG[team]
            copilot_mult = COPILOT_ADOPTION_MULTIPLIERS[team_config["copilot_adoption"]]
            productivity_mult = PRODUCTIVITY_MULTIPLIERS[team_config["productivity"]]
            
            # Generate unique IDE/model combinations for this team/day
            # Unique constraint: team_name, date, ide, copilot_model
            num_combinations = random.randint(1, min(2, len(IDES) * len(COPILOT_MODELS)))
            
            # Create all possible IDE/model combinations and sample from them
            all_combinations = [(ide, model) for ide in IDES for model in COPILOT_MODELS]
            selected_combinations = random.sample(all_combinations, num_combinations)
            
            for ide, model in selected_combinations:
                
                # Active users for chat (usually fewer than code suggestions)
                max_users = max(1, int(team_size * copilot_mult * 0.7))  # 70% of copilot users use chat
                active_users = random.randint(1, max_users)
                
                # Chat patterns vary by team characteristics
                base_chats = int(random.randint(3, 15) * productivity_mult * copilot_mult)
                total_chats = base_chats * active_users
                
                # Copy and insertion rates based on team experience
                if team_config["productivity"] == "high":
                    # Experienced teams are more efficient with chat responses
                    copy_rate = random.uniform(0.25, 0.40)
                    insertion_rate = random.uniform(0.35, 0.50)
                else:
                    # Less experienced teams copy/insert less efficiently
                    copy_rate = random.uniform(0.15, 0.30)
                    insertion_rate = random.uniform(0.25, 0.40)
                
                copy_events = int(total_chats * copy_rate)
                insertion_events = int(total_chats * insertion_rate)
                
                chat_metric = RawCopilotChatMetrics(
                    id=str(uuid.uuid4()),
                    team_name=team,
                    date=day.replace(hour=12, minute=0, second=0, microsecond=0),  # Normalized time
                    ide=ide,
                    copilot_model=model,
                    total_users=active_users,
                    total_chats=total_chats,
                    copy_events=copy_events,
                    insertion_events=insertion_events,
                    created_at=datetime.now(timezone.utc)
                )
                chat_records.append(chat_metric)
    
    logger.info(f"Inserting {len(chat_records)} Copilot chat metrics...")
    db.add_all(chat_records)
    db.commit()
    logger.info("Copilot chat metrics inserted successfully!")


def clear_existing_data(db: Session) -> None:
    """Clear existing mock data to avoid duplicates."""
    logger.info("Clearing existing data...")
    
    db.query(RawCopilotChatMetrics).delete()
    db.query(RawCopilotCodeMetrics).delete()
    db.query(RawCommitMetrics).delete()
    db.commit()
    
    logger.info("Existing data cleared!")


def main() -> None:
    """Main function to generate all mock data."""
    logger.info("Starting mock data generation...")
    
    # Ensure database tables exist
    create_tables()
    
    # Calculate date range (6 months back from today)
    end_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    start_date = end_date - timedelta(days=30 * MONTHS_TO_GENERATE)
    
    logger.info(f"Generating data from {start_date.date()} to {end_date.date()}")
    
    # Get working days
    working_days = get_working_days(start_date, end_date)
    logger.info(f"Generated {len(working_days)} working days")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Clear existing data
        clear_existing_data(db)
        
        # Generate all types of metrics
        generate_commit_metrics(db, working_days)
        generate_copilot_code_metrics(db, working_days)
        generate_copilot_chat_metrics(db, working_days)
        
        logger.info("All mock data generated successfully!")
        
        # Print summary
        commit_count = db.query(RawCommitMetrics).count()
        code_count = db.query(RawCopilotCodeMetrics).count()
        chat_count = db.query(RawCopilotChatMetrics).count()
        
        logger.info("Summary:")
        logger.info(f"  - Commit metrics: {commit_count} records")
        logger.info(f"  - Copilot code metrics: {code_count} records")
        logger.info(f"  - Copilot chat metrics: {chat_count} records")
        logger.info(f"  - Total records: {commit_count + code_count + chat_count}")
        
    except Exception as e:
        logger.error(f"Error generating mock data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
