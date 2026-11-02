# CogniStream Product Demo & Evaluation Guide

This guide walks an engineering director, manager, or evaluator through exploring CogniStream to evaluate its analytics, workflow friction diagnosis, and user interface.

---

## 1. Executive Scenario: Diagnosing CI/CD Notification Friction

### The Persona:
You are an **Engineering Director** overseeing Platform, Product, and Data engineering teams. Engineers have complained about feeling fragmented and unable to complete deep focus tasks.

### Exploration Steps:

#### Step 1: Open the Overview Dashboard
- Navigate to `http://localhost:5173`.
- Observe the **6 KPI Cards**:
  - Notice that while **Observed IDE Active Hours** is ~800 hours, **Qualifying Focus** (blocks &ge; 90 minutes) is only ~544 hours.
  - Notice the **Context-Switching Tax** of ~19.4%, indicating approximately 1 out of every 5 active hours is lost to disruption recovery.
- Look at the **Deterministic Workflow Observations** panel:
  - Read the insight: *"Automated CI/CD alerts accounted for over 30% of all recorded potential interruptions."*
  - Read the peak window: *"Interruption frequency peaked between 13:00 and 14:00 UTC."*

#### Step 2: Filter by Team
- Click the **Team Selector** in the top navigation bar.
- Select **Platform Engineering**:
  - Notice how the Focus Time Trend and KPI cards automatically recalculate.
  - Platform Engineering experiences elevated CI/CD alerts due to deployment and Kubernetes infrastructure pipelines.
- Switch to **Data Engineering**:
  - Notice that Data Engineering exhibits longer uninterrupted focus blocks (averaging over 107 minutes) and lower friction tax.

#### Step 3: Deep-Dive into Interruption Analysis
- Click **Interruption Analysis** in the left navigation sidebar.
- Review the **CI/CD Automation Friction Alert**:
  - Understand the relative frequency of CI/CD alerts vs personal direct messages.
  - Notice the **Zero Overlap Guarantee**: CogniStream merges overlapping recovery windows so bursts of 5 build alerts in 10 minutes don't produce 60 minutes of artificial loss.

#### Step 4: Inspect Reconstructed Focus Blocks
- Click **Flow Analytics** in the sidebar.
- Inspect the **Session Duration Distribution**:
  - Notice the split rule: inactivity gaps &gt; 15 minutes split sessions.
  - Toggle the **Qualifying Only (&ge;90m)** filter to see the uninterrupted deep focus sessions.

#### Step 5: Explore Raw Normalized Telemetry
- Click **Activity Explorer** in the sidebar.
- Type `proj-k8s-infra` in the search input or filter by **Source: Slack**.
- View the exact event records, pseudonymized actor IDs (`dev-maya`), and categorized interruption tags.

#### Step 6: Review Methodology Transparency
- Click **Methodology & Bias** in the sidebar.
- Review the transparent documentation of assumptions, the interval union algorithm, and ethical safeguards against individual monitoring.
