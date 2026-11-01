"""
CogniStream Mock Developer Event Generator
Generates realistic, deterministic developer activity events across GitHub, Slack, Jira, and IDE Activity Watch.
"""

import json
import random
import uuid
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Any, Optional

TEAMS = [
    {
        "id": "team-platform",
        "name": "Platform Engineering",
        "members": [
            {"id": "dev-maya", "name": "Maya Lin", "role": "Tech Lead", "focus_profile": "interrupted"},
            {"id": "dev-chen", "name": "Chen Wei", "role": "Senior Infra Engineer", "focus_profile": "deep_focus"},
            {"id": "dev-alex", "name": "Alex Mercer", "role": "DevOps Engineer", "focus_profile": "moderate"},
            {"id": "dev-elena", "name": "Elena Rostova", "role": "Security Engineer", "focus_profile": "moderate"},
        ],
        "projects": ["proj-k8s-infra", "proj-service-mesh", "proj-auth-v2", "proj-observability"]
    },
    {
        "id": "team-product",
        "name": "Product Engineering",
        "members": [
            {"id": "dev-sarah", "name": "Sarah Jenkins", "role": "Senior Frontend", "focus_profile": "context_switcher"},
            {"id": "dev-liam", "name": "Liam Connor", "role": "Fullstack Engineer", "focus_profile": "moderate"},
            {"id": "dev-zoe", "name": "Zoe Martinez", "role": "Frontend Engineer", "focus_profile": "interrupted"},
            {"id": "dev-marcus", "name": "Marcus Vance", "role": "Backend Engineer", "focus_profile": "deep_focus"},
            {"id": "dev-priya", "name": "Priya Sharma", "role": "Product Engineer", "focus_profile": "moderate"},
        ],
        "projects": ["proj-billing-portal", "proj-customer-dashboard", "proj-checkout-flow"]
    },
    {
        "id": "team-data",
        "name": "Data Engineering",
        "members": [
            {"id": "dev-david", "name": "David Kim", "role": "Data Architect", "focus_profile": "deep_focus"},
            {"id": "dev-ananya", "name": "Ananya Patel", "role": "ETL Engineer", "focus_profile": "moderate"},
            {"id": "dev-hugo", "name": "Hugo Silva", "role": "Analytics Engineer", "focus_profile": "moderate"},
        ],
        "projects": ["proj-stream-pipeline", "proj-lakehouse-etl", "proj-dbt-models"]
    }
]

SLACK_CHANNELS = {
    "team-platform": ["#infra-deployments", "#ci-alerts", "#platform-eng", "#security-ops"],
    "team-product": ["#product-releases", "#bug-triage", "#frontend-guild", "#customer-escalations"],
    "team-data": ["#data-pipelines", "#airflow-alerts", "#analytics-eng", "#warehouse-ops"]
}

CI_CD_COMPONENTS = ["k8s-cluster", "docker-builder", "unit-test-runner", "e2e-cypress", "terraform-apply", "db-migration"]

def deterministic_uuid(seed_str: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, seed_str))

class MockEventGenerator:
    def __init__(self, seed: int = 42, days: int = 30, end_date: Optional[datetime] = None):
        self.seed = seed
        self.days = days
        self.rng = random.Random(seed)
        if end_date is None:
            self.end_date = datetime(2026, 10, 25, 18, 0, 0, tzinfo=timezone.utc)
        else:
            self.end_date = end_date
        self.start_date = self.end_date - timedelta(days=days)

    def generate_events(self) -> List[Dict[str, Any]]:
        events: List[Dict[str, Any]] = []
        event_counter = 0

        # Iterate day by day
        current_day = self.start_date
        while current_day < self.end_date:
            is_weekend = current_day.weekday() >= 5
            
            for team in TEAMS:
                team_id = team["id"]
                projects = team["projects"]
                channels = SLACK_CHANNELS[team_id]

                for dev in team["members"]:
                    dev_id = dev["id"]
                    profile = dev["focus_profile"]

                    # Weekends have only rare 10% chance of small on-call or weekend hobby activity
                    if is_weekend:
                        if self.rng.random() > 0.12:
                            continue
                        work_start_hour = self.rng.randint(11, 14)
                        work_duration_hours = self.rng.uniform(1.0, 3.0)
                    else:
                        # Weekday work schedule variation
                        if profile == "deep_focus":
                            work_start_hour = self.rng.choice([8, 9, 10])
                            work_duration_hours = self.rng.uniform(6.5, 8.5)
                        elif profile == "interrupted":
                            work_start_hour = self.rng.choice([9, 10])
                            work_duration_hours = self.rng.uniform(7.0, 9.0)
                        else:
                            work_start_hour = self.rng.choice([9, 10])
                            work_duration_hours = self.rng.uniform(6.5, 8.0)

                    work_start = current_day.replace(hour=work_start_hour, minute=self.rng.randint(0, 45), second=0)
                    work_end = work_start + timedelta(hours=work_duration_hours)

                    # Generate IDE Sessions and heartbeats
                    dev_events = self._generate_developer_day(
                        dev_id=dev_id,
                        team_id=team_id,
                        projects=projects,
                        channels=channels,
                        profile=profile,
                        work_start=work_start,
                        work_end=work_end,
                        event_counter_start=event_counter
                    )
                    events.extend(dev_events)
                    event_counter += len(dev_events)

            current_day += timedelta(days=1)

        # Sort all events chronologically
        events.sort(key=lambda e: e["timestamp"])
        return events

    def _generate_developer_day(
        self,
        dev_id: str,
        team_id: str,
        projects: List[str],
        channels: List[str],
        profile: str,
        work_start: datetime,
        work_end: datetime,
        event_counter_start: int
    ) -> List[Dict[str, Any]]:
        events: List[Dict[str, Any]] = []
        counter = event_counter_start

        # Determine number and pattern of coding blocks
        current_time = work_start
        primary_project = self.rng.choice(projects)
        active_project = primary_project

        # Morning block
        morning_block_duration = self._sample_block_duration(profile)
        morning_end = min(current_time + timedelta(minutes=morning_block_duration), work_end)
        session_id_1 = deterministic_uuid(f"session-{dev_id}-{current_time.isoformat()}")

        block_events, counter = self._generate_ide_block(
            dev_id, team_id, active_project, session_id_1, current_time, morning_end, counter
        )
        events.extend(block_events)

        # Generate external interrupts / activity during morning
        ext_events, counter = self._generate_external_events(
            dev_id, team_id, projects, channels, profile, current_time, morning_end, counter
        )
        events.extend(ext_events)

        # Lunch / break gap (30 to 75 minutes)
        lunch_duration = self.rng.randint(35, 70)
        current_time = morning_end + timedelta(minutes=lunch_duration)

        if current_time < work_end:
            # Afternoon block
            if profile == "context_switcher" and len(projects) > 1:
                # Switch project in afternoon
                other_projects = [p for p in projects if p != primary_project]
                active_project = self.rng.choice(other_projects)
                # Emit project switch event
                events.append({
                    "event_id": f"evt-{counter}",
                    "timestamp": current_time.isoformat(),
                    "source": "ide",
                    "event_type": "project_switch",
                    "actor_id": dev_id,
                    "team_id": team_id,
                    "session_id": session_id_1,
                    "project_id": active_project,
                    "metadata": {
                        "previous_project": primary_project,
                        "new_project": active_project,
                        "reason": "afternoon_task_priority"
                    },
                    "ingestion_timestamp": datetime.now(timezone.utc).isoformat()
                })
                counter += 1

            afternoon_block_duration = self._sample_block_duration(profile)
            afternoon_end = min(current_time + timedelta(minutes=afternoon_block_duration), work_end)
            session_id_2 = deterministic_uuid(f"session-{dev_id}-{current_time.isoformat()}")

            block_events, counter = self._generate_ide_block(
                dev_id, team_id, active_project, session_id_2, current_time, afternoon_end, counter
            )
            events.extend(block_events)

            ext_events, counter = self._generate_external_events(
                dev_id, team_id, projects, channels, profile, current_time, afternoon_end, counter
            )
            events.extend(ext_events)

            # Maybe late afternoon quick review / git commit block
            current_time = afternoon_end + timedelta(minutes=self.rng.randint(15, 30))
            if current_time < work_end:
                git_events, counter = self._generate_git_jira_activity(
                    dev_id, team_id, active_project, current_time, work_end, counter
                )
                events.extend(git_events)

        return events

    def _sample_block_duration(self, profile: str) -> float:
        if profile == "deep_focus":
            # 90 - 180 minutes of continuous flow
            return self.rng.uniform(100.0, 190.0)
        elif profile == "interrupted":
            # 25 - 65 minutes before breaking
            return self.rng.uniform(25.0, 65.0)
        elif profile == "context_switcher":
            # 35 - 80 minutes
            return self.rng.uniform(35.0, 80.0)
        else:
            # moderate: 60 - 130 minutes
            return self.rng.uniform(55.0, 125.0)

    def _generate_ide_block(
        self,
        dev_id: str,
        team_id: str,
        project_id: str,
        session_id: str,
        start_time: datetime,
        end_time: datetime,
        counter: int
    ) -> (List[Dict[str, Any]], int):
        events = []
        cur = start_time

        # IDE session started
        events.append({
            "event_id": f"evt-{counter}",
            "timestamp": cur.isoformat(),
            "source": "ide",
            "event_type": "ide_session_started",
            "actor_id": dev_id,
            "team_id": team_id,
            "session_id": session_id,
            "project_id": project_id,
            "metadata": {"editor": "VSCode", "workspace": project_id},
            "ingestion_timestamp": datetime.now(timezone.utc).isoformat()
        })
        counter += 1

        # Emit heartbeats every 2 to 4 minutes
        while cur < end_time:
            step_minutes = self.rng.uniform(2.0, 4.0)
            cur += timedelta(minutes=step_minutes)
            if cur > end_time:
                break

            # Occasionally file switch (15% chance)
            if self.rng.random() < 0.15:
                events.append({
                    "event_id": f"evt-{counter}",
                    "timestamp": cur.isoformat(),
                    "source": "ide",
                    "event_type": "file_switch",
                    "actor_id": dev_id,
                    "team_id": team_id,
                    "session_id": session_id,
                    "project_id": project_id,
                    "metadata": {"file_extension": self.rng.choice([".py", ".tsx", ".sql", ".go", ".json"])},
                    "ingestion_timestamp": datetime.now(timezone.utc).isoformat()
                })
                counter += 1

            # Heartbeat
            events.append({
                "event_id": f"evt-{counter}",
                "timestamp": cur.isoformat(),
                "source": "ide",
                "event_type": "ide_heartbeat",
                "actor_id": dev_id,
                "team_id": team_id,
                "session_id": session_id,
                "project_id": project_id,
                "metadata": {"active_window": True, "keystrokes_est": self.rng.randint(40, 180)},
                "ingestion_timestamp": datetime.now(timezone.utc).isoformat()
            })
            counter += 1

        # Session ended
        events.append({
            "event_id": f"evt-{counter}",
            "timestamp": end_time.isoformat(),
            "source": "ide",
            "event_type": "ide_session_ended",
            "actor_id": dev_id,
            "team_id": team_id,
            "session_id": session_id,
            "project_id": project_id,
            "metadata": {"duration_minutes": round((end_time - start_time).total_seconds() / 60.0, 2)},
            "ingestion_timestamp": datetime.now(timezone.utc).isoformat()
        })
        counter += 1

        return events, counter

    def _generate_external_events(
        self,
        dev_id: str,
        team_id: str,
        projects: List[str],
        channels: List[str],
        profile: str,
        start_time: datetime,
        end_time: datetime,
        counter: int
    ) -> (List[Dict[str, Any]], int):
        events = []
        cur = start_time

        # Interruption frequency based on profile and team
        # Platform team has heavier CI/CD notifications
        ci_cd_rate = 0.35 if team_id == "team-platform" else 0.18
        if profile == "interrupted":
            interruption_interval_min = 15
            interruption_interval_max = 35
        elif profile == "deep_focus":
            interruption_interval_min = 45
            interruption_interval_max = 90
        else:
            interruption_interval_min = 25
            interruption_interval_max = 60

        while cur < end_time:
            interval = self.rng.randint(interruption_interval_min, interruption_interval_max)
            cur += timedelta(minutes=interval)
            if cur >= end_time:
                break

            # Determine event type: CI/CD notification vs Direct Message vs Mention vs Channel msg
            roll = self.rng.random()
            if roll < ci_cd_rate:
                # CI/CD notification burst
                component = self.rng.choice(CI_CD_COMPONENTS)
                status = self.rng.choice(["FAILED", "PASSED", "WARNING", "DEPLOYED", "TIMEOUT"])
                events.append({
                    "event_id": f"evt-{counter}",
                    "timestamp": cur.isoformat(),
                    "source": "slack",
                    "event_type": "ci_cd_notification",
                    "actor_id": dev_id,
                    "team_id": team_id,
                    "session_id": None,
                    "project_id": self.rng.choice(projects),
                    "metadata": {
                        "channel": channels[0],
                        "build_target": component,
                        "build_status": status,
                        "is_automated": True
                    },
                    "ingestion_timestamp": datetime.now(timezone.utc).isoformat()
                })
                counter += 1
            elif roll < 0.65:
                # Direct message received
                sender = f"user-{self.rng.randint(101, 109)}"
                events.append({
                    "event_id": f"evt-{counter}",
                    "timestamp": cur.isoformat(),
                    "source": "slack",
                    "event_type": "direct_message_received",
                    "actor_id": dev_id,
                    "team_id": team_id,
                    "session_id": None,
                    "project_id": None,
                    "metadata": {
                        "sender_id": sender,
                        "has_action_item": self.rng.choice([True, False]),
                        "urgency": self.rng.choice(["low", "medium", "high"])
                    },
                    "ingestion_timestamp": datetime.now(timezone.utc).isoformat()
                })
                counter += 1
            elif roll < 0.85:
                # Mention in channel
                events.append({
                    "event_id": f"evt-{counter}",
                    "timestamp": cur.isoformat(),
                    "source": "slack",
                    "event_type": "mention_received",
                    "actor_id": dev_id,
                    "team_id": team_id,
                    "session_id": None,
                    "project_id": None,
                    "metadata": {
                        "channel": self.rng.choice(channels),
                        "mention_type": "@here" if self.rng.random() < 0.2 else "@user"
                    },
                    "ingestion_timestamp": datetime.now(timezone.utc).isoformat()
                })
                counter += 1
            else:
                # General message received in monitored channel
                events.append({
                    "event_id": f"evt-{counter}",
                    "timestamp": cur.isoformat(),
                    "source": "slack",
                    "event_type": "message_received",
                    "actor_id": dev_id,
                    "team_id": team_id,
                    "session_id": None,
                    "project_id": None,
                    "metadata": {
                        "channel": self.rng.choice(channels),
                        "thread_reply": self.rng.choice([True, False])
                    },
                    "ingestion_timestamp": datetime.now(timezone.utc).isoformat()
                })
                counter += 1

        return events, counter

    def _generate_git_jira_activity(
        self,
        dev_id: str,
        team_id: str,
        project_id: str,
        start_time: datetime,
        end_time: datetime,
        counter: int
    ) -> (List[Dict[str, Any]], int):
        events = []
        cur = start_time

        # Jira update
        jira_id = f"ENG-{self.rng.randint(1000, 9999)}"
        events.append({
            "event_id": f"evt-{counter}",
            "timestamp": cur.isoformat(),
            "source": "jira",
            "event_type": self.rng.choice(["issue_updated", "issue_completed", "issue_started"]),
            "actor_id": dev_id,
            "team_id": team_id,
            "session_id": None,
            "project_id": project_id,
            "metadata": {
                "issue_key": jira_id,
                "status": "In Review",
                "priority": self.rng.choice(["P1", "P2", "P3"])
            },
            "ingestion_timestamp": datetime.now(timezone.utc).isoformat()
        })
        counter += 1

        cur += timedelta(minutes=self.rng.randint(5, 20))
        if cur < end_time:
            # GitHub Commit
            commit_hash = deterministic_uuid(f"commit-{dev_id}-{cur.isoformat()}")[:8]
            events.append({
                "event_id": f"evt-{counter}",
                "timestamp": cur.isoformat(),
                "source": "github",
                "event_type": "commit",
                "actor_id": dev_id,
                "team_id": team_id,
                "session_id": None,
                "project_id": project_id,
                "metadata": {
                    "commit_hash": commit_hash,
                    "files_changed": self.rng.randint(1, 8),
                    "insertions": self.rng.randint(10, 240),
                    "deletions": self.rng.randint(2, 60),
                    "branch": "feature/" + jira_id
                },
                "ingestion_timestamp": datetime.now(timezone.utc).isoformat()
            })
            counter += 1

        cur += timedelta(minutes=self.rng.randint(5, 15))
        if cur < end_time and self.rng.random() < 0.4:
            # Pull request review
            pr_num = self.rng.randint(100, 999)
            events.append({
                "event_id": f"evt-{counter}",
                "timestamp": cur.isoformat(),
                "source": "github",
                "event_type": "pull_request_reviewed",
                "actor_id": dev_id,
                "team_id": team_id,
                "session_id": None,
                "project_id": project_id,
                "metadata": {
                    "pr_number": pr_num,
                    "review_state": self.rng.choice(["APPROVED", "CHANGES_REQUESTED", "COMMENTED"]),
                    "comments_count": self.rng.randint(1, 5)
                },
                "ingestion_timestamp": datetime.now(timezone.utc).isoformat()
            })
            counter += 1

        return events, counter

if __name__ == "__main__":
    generator = MockEventGenerator(seed=42, days=30)
    evts = generator.generate_events()
    print(f"Generated {len(evts)} deterministic mock events across 30 days.")
    print("Sample event:", json.dumps(evts[0], indent=2))
