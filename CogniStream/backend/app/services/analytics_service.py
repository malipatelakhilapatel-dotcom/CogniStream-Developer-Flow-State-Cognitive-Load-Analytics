"""
Analytics Service for CogniStream.
Coordinates repository queries, KPI calculations, and insight generation.
"""

from typing import List, Dict, Any, Optional
from backend.app.repositories.event_repository import event_repo
from backend.app.analytics.engine import FlowAnalyticsEngine
import json

class AnalyticsService:
    def __init__(self):
        self.repo = event_repo
        self.engine = FlowAnalyticsEngine()

    def get_overview_kpis(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        team_id: Optional[str] = None
    ) -> Dict[str, Any]:
        daily_metrics = self.repo.get_daily_metrics(start_date, end_date, team_id)

        if not daily_metrics:
            return {
                "active_developers": 0,
                "observed_ide_hours": 0.0,
                "qualifying_focus_hours": 0.0,
                "avg_focus_block_minutes": 0.0,
                "potential_interruptions": 0,
                "estimated_context_switching_tax_pct": 0.0,
                "total_focus_blocks": 0,
                "qualifying_focus_blocks": 0,
                "period_days": 0
            }

        # Calculate unique active developers from the events in this period
        events, _ = self.repo.get_events(start_date=start_date, end_date=end_date, team_id=team_id, limit=50000)
        unique_devs = len(set(e["actor_id"] for e in events)) if events else max(d["active_developer_count"] for d in daily_metrics)

        total_ide_mins = sum(float(d.get("observed_ide_minutes", 0.0)) for d in daily_metrics)
        total_qual_mins = sum(float(d.get("qualifying_focus_minutes", 0.0)) for d in daily_metrics)
        total_blocks = sum(int(d.get("focus_block_count", 0)) for d in daily_metrics)
        total_qual_blocks = sum(int(d.get("qualifying_block_count", 0)) for d in daily_metrics)
        total_interruptions = sum(int(d.get("interruption_count", 0)) for d in daily_metrics)
        total_loss_mins = sum(float(d.get("estimated_interruption_loss_minutes", 0.0)) for d in daily_metrics)

        avg_block = round(total_ide_mins / total_blocks, 1) if total_blocks > 0 else 0.0
        tax_pct = self.engine.compute_context_switching_tax(total_ide_mins, total_loss_mins)

        return {
            "active_developers": unique_devs,
            "observed_ide_hours": round(total_ide_mins / 60.0, 1),
            "qualifying_focus_hours": round(total_qual_mins / 60.0, 1),
            "avg_focus_block_minutes": avg_block,
            "potential_interruptions": total_interruptions,
            "estimated_context_switching_tax_pct": tax_pct,
            "total_focus_blocks": total_blocks,
            "qualifying_focus_blocks": total_qual_blocks,
            "period_days": len(daily_metrics)
        }

    def get_flow_trends(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        team_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        daily_metrics = self.repo.get_daily_metrics(start_date, end_date, team_id)

        # Aggregate across teams by date if team_id == "all"
        by_date: Dict[str, Dict[str, Any]] = {}
        for d in daily_metrics:
            date_key = str(d["date"])[:10]
            if date_key not in by_date:
                by_date[date_key] = {
                    "date": date_key,
                    "observed_ide_hours": 0.0,
                    "qualifying_focus_hours": 0.0,
                    "focus_blocks": 0,
                    "interruptions": 0,
                    "active_devs": 0
                }
            by_date[date_key]["observed_ide_hours"] += float(d.get("observed_ide_minutes", 0.0)) / 60.0
            by_date[date_key]["qualifying_focus_hours"] += float(d.get("qualifying_focus_minutes", 0.0)) / 60.0
            by_date[date_key]["focus_blocks"] += int(d.get("focus_block_count", 0))
            by_date[date_key]["interruptions"] += int(d.get("interruption_count", 0))
            by_date[date_key]["active_devs"] = max(by_date[date_key]["active_devs"], int(d.get("active_developer_count", 0)))

        trends = []
        for k in sorted(by_date.keys()):
            row = by_date[k]
            row["observed_ide_hours"] = round(row["observed_ide_hours"], 2)
            row["qualifying_focus_hours"] = round(row["qualifying_focus_hours"], 2)
            trends.append(row)

        return trends

    def get_interruption_breakdown(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        team_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        metrics = self.repo.get_interruption_metrics(start_date, end_date, team_id)

        # Aggregate counts and estimated loss by category
        by_cat: Dict[str, Dict[str, Any]] = {}
        total_events = 0

        category_labels = {
            "ci_cd_notification": "CI/CD Notifications",
            "direct_message": "Direct Slack Messages",
            "mention": "Channel Mentions (@here/@user)",
            "project_switch": "Cross-Project Switches",
            "task_switch": "Jira Task Transitions",
            "code_review": "Code Review Interventions",
            "channel_message": "Monitored Channel Messages",
            "default": "Other External Interrupts"
        }

        for m in metrics:
            cat = m["interruption_category"]
            cnt = int(m.get("event_count", 0))
            loss = float(m.get("estimated_associated_focus_loss_minutes", 0.0))
            total_events += cnt

            if cat not in by_cat:
                by_cat[cat] = {
                    "category": cat,
                    "label": category_labels.get(cat, cat.replace("_", " ").title()),
                    "count": 0,
                    "estimated_loss_hours": 0.0
                }
            by_cat[cat]["count"] += cnt
            by_cat[cat]["estimated_loss_hours"] += loss / 60.0

        result = []
        for cat, data in by_cat.items():
            pct = round((data["count"] / total_events) * 100.0, 1) if total_events > 0 else 0.0
            result.append({
                "category": cat,
                "label": data["label"],
                "count": data["count"],
                "percentage": pct,
                "estimated_loss_hours": round(data["estimated_loss_hours"], 1)
            })

        result.sort(key=lambda x: x["count"], reverse=True)
        return result

    def get_interruption_timeline(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        team_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        metrics = self.repo.get_interruption_metrics(start_date, end_date, team_id)

        by_date: Dict[str, Dict[str, Any]] = {}
        for m in metrics:
            dt = str(m["period_start"])[:10]
            cat = m["interruption_category"]
            cnt = int(m.get("event_count", 0))

            if dt not in by_date:
                by_date[dt] = {
                    "date": dt,
                    "total_interruptions": 0,
                    "ci_cd_notification": 0,
                    "direct_message": 0,
                    "mention": 0,
                    "project_switch": 0,
                    "task_switch": 0,
                    "other": 0
                }
            by_date[dt]["total_interruptions"] += cnt
            if cat in by_date[dt]:
                by_date[dt][cat] += cnt
            else:
                by_date[dt]["other"] += cnt

        timeline = [by_date[k] for k in sorted(by_date.keys())]
        return timeline

    def get_team_comparison(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        daily = self.repo.get_daily_metrics(start_date, end_date, team_id="all")

        teams_map = {
            "team-platform": {"name": "Platform Engineering", "headcount": 4},
            "team-product": {"name": "Product Engineering", "headcount": 5},
            "team-data": {"name": "Data Engineering", "headcount": 3}
        }

        by_team: Dict[str, Dict[str, Any]] = {}
        for d in daily:
            tm = d["team_id"]
            if tm not in by_team:
                by_team[tm] = {
                    "team_id": tm,
                    "team_name": teams_map.get(tm, {}).get("name", tm),
                    "headcount": teams_map.get(tm, {}).get("headcount", 4),
                    "total_ide_mins": 0.0,
                    "total_qual_mins": 0.0,
                    "focus_block_count": 0,
                    "interruption_count": 0,
                    "context_switch_count": 0,
                    "loss_mins": 0.0,
                    "days": 0
                }
            by_team[tm]["total_ide_mins"] += float(d.get("observed_ide_minutes", 0.0))
            by_team[tm]["total_qual_mins"] += float(d.get("qualifying_focus_minutes", 0.0))
            by_team[tm]["focus_block_count"] += int(d.get("focus_block_count", 0))
            by_team[tm]["interruption_count"] += int(d.get("interruption_count", 0))
            by_team[tm]["context_switch_count"] += int(d.get("context_switch_count", 0))
            by_team[tm]["loss_mins"] += float(d.get("estimated_interruption_loss_minutes", 0.0))
            by_team[tm]["days"] += 1

        result = []
        for tm, data in by_team.items():
            headcount = max(1, data["headcount"])
            total_blocks = data["focus_block_count"]
            avg_block_dur = round(data["total_ide_mins"] / total_blocks, 1) if total_blocks > 0 else 0.0
            qual_hours_per_dev = round((data["total_qual_mins"] / 60.0) / headcount, 1)
            interruptions_per_dev = round(data["interruption_count"] / headcount, 1)
            tax_pct = self.engine.compute_context_switching_tax(data["total_ide_mins"], data["loss_mins"])

            result.append({
                "team_id": tm,
                "team_name": data["team_name"],
                "headcount": headcount,
                "observed_ide_hours": round(data["total_ide_mins"] / 60.0, 1),
                "qualifying_focus_hours": round(data["total_qual_mins"] / 60.0, 1),
                "qualifying_hours_per_dev": qual_hours_per_dev,
                "interruptions_per_dev": interruptions_per_dev,
                "avg_focus_block_minutes": avg_block_dur,
                "context_switch_count": data["context_switch_count"],
                "context_switching_tax_pct": tax_pct
            })

        result.sort(key=lambda x: x["qualifying_hours_per_dev"], reverse=True)
        return result

    def get_insights(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        team_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        daily = self.repo.get_daily_metrics(start_date, end_date, team_id)
        events, _ = self.repo.get_events(start_date=start_date, end_date=end_date, team_id=team_id, limit=10000)
        blocks = self.repo.get_focus_blocks(start_date=start_date, end_date=end_date, team_id=team_id)
        return self.engine.generate_deterministic_insights(daily, events, blocks)

analytics_service = AnalyticsService()