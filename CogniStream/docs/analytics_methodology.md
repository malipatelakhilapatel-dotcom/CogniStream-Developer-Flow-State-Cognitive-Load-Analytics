# CogniStream Analytics Methodology & Theoretical Foundations

## 1. Problem Formulation: Beyond Taylorist Metrics

Traditional software engineering metrics (Lines of Code, Pull Request Count, Closed Jira Tickets) suffer from severe flaws:
1. **Misaligned Incentives:** Developers are rewarded for generating verbose code or splitting tickets unnaturally.
2. **Invisible Cognitive Load:** High-intensity engineering demands unbroken concentration. An engineer interrupted every 15 minutes by CI/CD alerts produces fragmented, error-prone code despite appearing "busy."
3. **Observer Effect:** Surveillance-oriented tracking creates developer anxiety and degrades morale.

**CogniStream's Philosophy:**
- We monitor **workflow friction triggers**, not human brains.
- We quantify **uninterrupted editor availability**, not subjective concentration.
- We identify **systemic organizational blockers** (e.g., noisy automated CI alerts) to empower engineering leadership to fix notification hygiene.

---

## 2. Mathematical Formulations

### 2.1 Reconstructed Focus Block Duration
Let $H = \{t_1, t_2, \dots, t_n\}$ be the ordered timestamps of IDE heartbeats for actor $A$.
A focus block $B_k = [t_{\text{start}}, t_{\text{end}}]$ satisfies:
$$\forall i \in [\text{start}, \text{end}-1], \quad (t_{i+1} - t_i) \le \Delta_{\text{inactivity}}$$
where $\Delta_{\text{inactivity}} = 15 \text{ minutes}$.

### 2.2 Qualifying Focus Block Condition
A focus block $B_k$ is defined as *Qualifying Focus* if:
$$\text{Duration}(B_k) \ge \Theta_{\text{qualification}} = 90 \text{ minutes}$$

### 2.3 Non-Overlapping Interruption Interval Union
For a set of $m$ potential interruption events with timestamps $T_j$ and category recovery duration $R(c_j)$, the nominal impact interval is:
$$I_j = [T_j, \min(T_j + R(c_j), \text{SessionEnd})]$$

To prevent double-counting overlapping recovery intervals:
$$\mathcal{U} = \bigcup_{j=1}^m I_j$$
where $\mathcal{U} = \sum_{k=1}^p [S_k, E_k]$ is the union of disjoint intervals.
$$\text{Total Estimated Interruption Loss} = \sum_{k=1}^p (E_k - S_k)$$

### 2.4 Estimated Context-Switching Tax
$$\text{Tax} (\%) = \begin{cases} 
\frac{\text{Total Merged Interruption Loss (mins)}}{\text{Total Observed IDE Active Time (mins)}} \times 100, & \text{if IDE Time} > 0 \\
0.0, & \text{otherwise}
\end{cases}$$

---

## 3. Assumptions & Recovery Times

| Category | Nominal Recovery | Rationale |
|---|---|---|
| `ci_cd_notification` | 12.0 min | Triage build failure logs, rerun jobs, wait for CI queue |
| `direct_message` | 15.0 min | Synchronous cognitive context shift to answer questions |
| `project_switch` | 18.0 min | Reloading IDE workspace, cognitive switch to different domain |
| `mention` | 10.0 min | Reading threaded discussions in channels |
| `task_switch` | 10.0 min | Updating Jira tickets, context shift |
| `code_review` | 15.0 min | Reading teammate's PR diff, leaving comments |
