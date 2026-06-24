#!/usr/bin/env python3
"""
ASANA PORTFOLIO BUILDER
Creates 5 complete portfolio projects in your Asana workspace via API.

SETUP:
1. Get your Personal Access Token: https://app.asana.com/0/developer-console
2. Paste it below where it says "YOUR_TOKEN_HERE"
3. Get your Workspace GID: https://app.asana.com/api/1.0/workspaces
4. Run: python3 asana_portfolio_builder.py
"""

import requests
import json
import sys
import time

PERSONAL_ACCESS_TOKEN = "YOUR_TOKEN_HERE"
WORKSPACE_GID = "YOUR_WORKSPACE_GID"

class AsanaPortfolioBuilder:
    def __init__(self, token, workspace_gid):
        self.token = token
        self.workspace_gid = workspace_gid
        self.base_url = "https://app.asana.com/api/1.0"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        self.created_projects = []
    
    def _request(self, method, endpoint, data=None):
        url = f"{self.base_url}{endpoint}"
        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers)
            elif method == "POST":
                response = requests.post(url, headers=self.headers, json=data)
            else:
                response = requests.request(method, url, headers=self.headers, json=data)
            if response.status_code in [200, 201]:
                return response.json()
            else:
                print(f"  ⚠ Error {response.status_code}: {response.text[:200]}")
                return None
        except Exception as e:
            print(f"  ⚠ Request failed: {e}")
            return None
    
    def list_workspaces(self):
        result = self._request("GET", "/workspaces")
        if result and "data" in result:
            print("\n📋 YOUR WORKSPACES:")
            for ws in result["data"]:
                print(f"   Name: {ws['name']}")
                print(f"   GID:  {ws['gid']}")
            return result["data"]
        return []
    
    def create_project(self, name, notes="", color="light-blue"):
        data = {"data": {"name": name, "workspace": self.workspace_gid, "notes": notes, "color": color}}
        result = self._request("POST", "/projects", data)
        if result and "data" in result:
            proj = result["data"]
            print(f"  ✅ Created project: {proj['name']} (GID: {proj['gid']})")
            self.created_projects.append(proj)
            return proj["gid"]
        return None
    
    def create_section(self, project_gid, name):
        data = {"data": {"name": name}}
        result = self._request("POST", f"/projects/{project_gid}/sections", data)
        if result and "data" in result:
            return result["data"]["gid"]
        return None
    
    def create_task(self, project_gid, name, notes=""):
        task_data = {"data": {"name": name, "projects": [project_gid], "workspace": self.workspace_gid, "notes": notes}}
        result = self._request("POST", "/tasks", task_data)
        if result and "data" in result:
            return result["data"]["gid"]
        return None
    
    def create_subtask(self, parent_task_gid, name, notes=""):
        data = {"data": {"name": name, "notes": notes, "workspace": self.workspace_gid}}
        result = self._request("POST", f"/tasks/{parent_task_gid}/subtasks", data)
        if result and "data" in result:
            return result["data"]["gid"]
        return None
    
    def add_task_to_section(self, task_gid, section_gid):
        data = {"data": {"task": task_gid}}
        self._request("POST", f"/sections/{section_gid}/addTask", data)

PROJECTS = [
    {
        "name": "Q3 Product Launch Campaign",
        "notes": "Complete marketing campaign from pre-launch through post-launch analysis.",
        "color": "light-red",
        "sections": ["PRE-LAUNCH", "LAUNCH WEEK", "POST-LAUNCH", "CAMPAIGN CLOSEOUT"],
        "tasks": [
            ("PRE-LAUNCH", "Define campaign objectives & KPIs", ["Set SMART goals", "Identify target audience segments", "Define success metrics"]),
            ("PRE-LAUNCH", "Create campaign messaging & positioning", ["Draft key messages", "Create brand voice guidelines", "Get stakeholder approval"]),
            ("PRE-LAUNCH", "Design creative assets", ["Social media graphics (8 pieces)", "Email templates (3 variations)", "Landing page design mockups", "Video production: 30-second spot"]),
            ("PRE-LAUNCH", "Build email list & segment audience", ["Clean existing email list", "Create signup forms", "Set up audience segments"]),
            ("LAUNCH WEEK", "Launch social media campaign", ["Schedule posts (2-week calendar)", "Set up paid social ads", "Execute influencer outreach"]),
            ("LAUNCH WEEK", "Send launch email sequence", ["Day 0: Announcement email", "Day 3: Follow-up with social proof", "Day 7: Last chance email"]),
            ("LAUNCH WEEK", "Publish landing page & activate all assets"),
            ("LAUNCH WEEK", "Monitor & respond (Week 1)", ["Track social engagement daily", "Respond to comments and DMs", "Monitor ad performance"]),
            ("POST-LAUNCH", "Analyze campaign performance", ["Pull analytics from all channels", "Calculate overall ROI", "Create performance report"]),
            ("POST-LAUNCH", "Optimize based on learnings", ["A/B test email subject lines", "Adjust ad targeting", "Refine landing page"]),
            ("POST-LAUNCH", "Retarget non-converters"),
            ("POST-LAUNCH", "Document lessons learned & archive assets"),
            ("CAMPAIGN CLOSEOUT", "Final budget reconciliation"),
            ("CAMPAIGN CLOSEOUT", "Present results to stakeholders"),
        ]
    },
    {
        "name": "New Employee Onboarding",
        "notes": "Standardized onboarding template. Duplicate for each new hire.",
        "color": "light-green",
        "sections": ["BEFORE DAY 1", "DAY 1", "WEEK 1", "30-DAY CHECK", "60-DAY CHECK", "90-DAY CHECK"],
        "tasks": [
            ("BEFORE DAY 1", "Send welcome email & first-day packet"),
            ("BEFORE DAY 1", "Prepare workstation & equipment", ["Order laptop, monitor, peripherals", "Set up desk, chair, workspace", "Prepare welcome swag bag"]),
            ("BEFORE DAY 1", "IT setup & account creation", ["Create company email", "Add to Slack/Teams", "Grant Asana access", "Add to Google Groups", "Configure VPN"]),
            ("BEFORE DAY 1", "Prepare onboarding documentation", ["Employee handbook", "Org chart with contacts", "First-week agenda"]),
            ("DAY 1", "Welcome meeting with hiring manager (9:00 AM)"),
            ("DAY 1", "HR paperwork & benefits enrollment"),
            ("DAY 1", "Office tour & team introductions"),
            ("DAY 1", "IT orientation (passwords, security, tools)"),
            ("DAY 1", "Lunch with assigned buddy/mentor"),
            ("WEEK 1", "Department overview meetings", ["Marketing team intro", "Sales team intro", "Product team intro", "Operations team intro"]),
            ("WEEK 1", "Complete role-specific training modules"),
            ("WEEK 1", "Shadow team member (3 sessions)"),
            ("WEEK 1", "Set 30-60-90 day goals with manager"),
            ("WEEK 1", "Receive first project assignment"),
            ("30-DAY CHECK", "Manager 1:1 check-in"),
            ("30-DAY CHECK", "Complete required compliance training"),
            ("30-DAY CHECK", "Submit first project deliverable"),
            ("30-DAY CHECK", "New hire experience feedback survey"),
            ("60-DAY CHECK", "Progress review with manager"),
            ("60-DAY CHECK", "Take on first independent project"),
            ("60-DAY CHECK", "Cross-functional collaboration project"),
            ("90-DAY CHECK", "Formal performance review"),
            ("90-DAY CHECK", "Goal-setting for next quarter"),
            ("90-DAY CHECK", "Onboarding complete - archive project"),
        ]
    },
    {
        "name": "Sprint 14: Mobile App v2.3",
        "notes": "Agile sprint management. Use Board view for Kanban workflow.",
        "color": "light-purple",
        "sections": ["BACKLOG", "TO DO", "IN PROGRESS", "CODE REVIEW", "TESTING", "DONE", "SPRINT RETRO"],
        "tasks": [
            ("BACKLOG", "[Feature] Dark mode support for iOS & Android"),
            ("BACKLOG", "[Feature] Push notification settings screen"),
            ("BACKLOG", "[Feature] Offline document sync mode"),
            ("BACKLOG", "[Bug] Login timeout on slow 3G connections"),
            ("BACKLOG", "[Bug] Images not loading on iOS 17 devices"),
            ("BACKLOG", "[Tech Debt] Refactor authentication module"),
            ("BACKLOG", "[Tech Debt] Update all API endpoints to v3"),
            ("TO DO", "Implement dark mode UI components (Assigned: Alex)"),
            ("TO DO", "Create push notification preference screen (Assigned: Priya)"),
            ("TO DO", "Fix login timeout issue on slow connections (Assigned: James)"),
            ("IN PROGRESS", "Build offline sync engine (Assigned: Alex)"),
            ("IN PROGRESS", "Debug iOS 17 image loading failure (Assigned: Maria)"),
            ("CODE REVIEW", "Refactor auth module (Author: James, Reviewer: Priya)"),
            ("TESTING", "Update API integration tests for v3 endpoints"),
            ("DONE", "Design dark mode mockups (Completed: June 20)"),
            ("DONE", "Research push notification best practices (Completed: June 22)"),
            ("DONE", "Set up feature flag system (Completed: June 23)"),
            ("SPRINT RETRO", "Sprint review meeting (Scheduled: June 30)"),
            ("SPRINT RETRO", "Collect team feedback and velocity data"),
            ("SPRINT RETRO", "Update velocity chart and burndown"),
            ("SPRINT RETRO", "Plan Sprint 15 scope and assignments"),
        ]
    },
    {
        "name": "Grant Application Pipeline",
        "notes": "Track every grant from research through final reporting. Built for nonprofits.",
        "color": "light-yellow",
        "sections": ["RESEARCH", "APPLICATION IN PROGRESS", "SUBMITTED", "AWARDED", "DECLINED", "REPORTING DUE"],
        "tasks": [
            ("RESEARCH", "Identify 10 potential grants for Q3-Q4", ["Community Foundation ($25K)", "State Arts Council ($15K)", "Federal DOE Grant ($100K)", "TechCorp Corporate ($10K)", "Family Foundation ($20K)"]),
            ("RESEARCH", "Review eligibility criteria for each identified grant"),
            ("RESEARCH", "Prioritize grants by alignment, amount, and deadline"),
            ("APPLICATION IN PROGRESS", "Apply: Community Foundation Grant ($25K) - Due July 15", ["Gather organizational documents", "Write program narrative", "Prepare budget justification", "Collect 3 letters of support", "Complete online application"]),
            ("APPLICATION IN PROGRESS", "Apply: TechCorp Corporate Giving ($10K) - Due Aug 1", ["Research TechCorp priorities", "Draft partnership proposal", "Prepare impact metrics report"]),
            ("APPLICATION IN PROGRESS", "Apply: Federal DOE Grant ($100K) - Due Sept 15", ["Register on Grants.gov", "Download full RFP", "Form grant writing team", "Outline narrative sections", "Begin budget development"]),
            ("SUBMITTED", "Submitted: State Arts Council ($15K) - June 10 ✓"),
            ("SUBMITTED", "Submitted: Family Foundation ($20K) - June 18 ✓"),
            ("AWARDED", "Awarded: Tech Literacy Grant ($8K) - June 15 ✓", ["Sign grant agreement", "Set up quarterly reporting calendar", "Initiate program activities"]),
            ("DECLINED", "Declined: National Health Initiative ($50K)", ["Request feedback from program officer"]),
            ("REPORTING DUE", "Q2 Report: Tech Literacy Grant - Due Sept 30"),
            ("REPORTING DUE", "Mid-year Financial Statement - Due July 31"),
            ("REPORTING DUE", "Final Impact Report - Due Dec 31"),
        ]
    },
    {
        "name": "Annual Fundraising Gala 2026",
        "notes": "Complete event planning from 6 months out through post-event follow-up.",
        "color": "light-orange",
        "sections": ["6 MONTHS OUT", "3 MONTHS OUT", "1 MONTH OUT", "EVENT WEEK", "DAY OF EVENT", "POST-EVENT"],
        "tasks": [
            ("6 MONTHS OUT", "Set event date: October 15, 2026"),
            ("6 MONTHS OUT", "Establish fundraising goal: $50,000"),
            ("6 MONTHS OUT", "Form event planning committee (5-7 volunteers)"),
            ("6 MONTHS OUT", "Create detailed event budget", ["Venue & catering estimate", "Entertainment & AV budget", "Marketing & invitations", "Auction item procurement", "Contingency fund (10%)"]),
            ("6 MONTHS OUT", "Book venue: Metropolitan Event Center"),
            ("3 MONTHS OUT", "Send save-the-date announcements"),
            ("3 MONTHS OUT", "Confirm catering menu and dietary options"),
            ("3 MONTHS OUT", "Book entertainment: Jazz quartet + keynote speaker"),
            ("3 MONTHS OUT", "Launch sponsorship packages", ["Title Sponsor: $10,000", "Gold Sponsor: $5,000", "Silver Sponsor: $2,500", "Table Host: $1,000"]),
            ("3 MONTHS OUT", "Design invitation suite and event program"),
            ("1 MONTH OUT", "Send formal invitations to full list"),
            ("1 MONTH OUT", "Confirm RSVPs and track responses"),
            ("1 MONTH OUT", "Finalize seating chart and table assignments"),
            ("1 MONTH OUT", "Brief all volunteers on roles"),
            ("1 MONTH OUT", "Complete silent auction procurement (target: 25 items)"),
            ("EVENT WEEK", "Final walkthrough at venue (lighting, layout, AV)"),
            ("EVENT WEEK", "Pick up all printed materials and signage"),
            ("EVENT WEEK", "Confirm AV setup and test equipment"),
            ("EVENT WEEK", "Prepare check-in packets and name tags"),
            ("EVENT WEEK", "Finalize day-of timeline (every 15 minutes)"),
            ("DAY OF EVENT", "Setup: 8:00 AM - 12:00 PM"),
            ("DAY OF EVENT", "Guest arrival & check-in: 5:00 - 7:00 PM"),
            ("DAY OF EVENT", "Welcome reception & silent auction: 5:30 - 7:00 PM"),
            ("DAY OF EVENT", "Dinner & program: 7:00 - 9:00 PM"),
            ("DAY OF EVENT", "Live auction & closing ask: 9:00 - 10:00 PM"),
            ("DAY OF EVENT", "Breakdown & cleanup: 10:00 - 11:00 PM"),
            ("POST-EVENT", "Send thank-you emails within 48 hours"),
            ("POST-EVENT", "Collect and process all donation pledges"),
            ("POST-EVENT", "Final budget reconciliation"),
            ("POST-EVENT", "Send attendee satisfaction survey"),
            ("POST-EVENT", "Document lessons learned for next year"),
        ]
    }
]

def main():
    print("=" * 60)
    print("   ASANA PORTFOLIO BUILDER - Creating 5 Demo Projects")
    print("=" * 60)
    
    if PERSONAL_ACCESS_TOKEN == "YOUR_TOKEN_HERE":
        print("\n❌ ERROR: You need to set your Personal Access Token!")
        print("   1. Go to: https://app.asana.com/0/developer-console")
        print("   2. Click 'Create New Personal Access Token'")
        print("   3. Copy the token and paste it in the script")
        return
    
    builder = AsanaPortfolioBuilder(PERSONAL_ACCESS_TOKEN, WORKSPACE_GID)
    
    if WORKSPACE_GID == "YOUR_WORKSPACE_GID":
        print("\n⚠ WORKSPACE_GID not set. Listing your workspaces...")
        builder.list_workspaces()
        return
    
    print(f"\n🔧 Connected to workspace: {WORKSPACE_GID}")
    print(f"📊 Building {len(PROJECTS)} portfolio projects...\n")
    
    for i, project_def in enumerate(PROJECTS, 1):
        print(f"\n{'─' * 50}")
        print(f"  PROJECT {i}/5: {project_def['name']}")
        print(f"{'─' * 50}")
        
        project_gid = builder.create_project(
            name=project_def["name"],
            notes=project_def["notes"],
            color=project_def["color"]
        )
        
        if not project_gid:
            continue
        
        sections = {}
        for section_name in project_def["sections"]:
            sec_gid = builder.create_section(project_gid, section_name)
            if sec_gid:
                sections[section_name] = sec_gid
            time.sleep(0.2)
        
        task_count = 0
        subtask_count = 0
        
        for task_def in project_def["tasks"]:
            section_name = task_def[0]
            task_name = task_def[1]
            subtasks = task_def[2] if len(task_def) > 2 else []
            
            task_gid = builder.create_task(project_gid=project_gid, name=task_name)
            
            if task_gid:
                task_count += 1
                if section_name in sections:
                    builder.add_task_to_section(task_gid, sections[section_name])
                
                for subtask_name in subtasks:
                    builder.create_subtask(task_gid, subtask_name)
                    subtask_count += 1
                    time.sleep(0.1)
            
            time.sleep(0.2)
        
        print(f"  ✅ Created: {len(sections)} sections, {task_count} tasks, {subtask_count} subtasks")
    
    print("\n" + "=" * 60)
    print("   ✅ PORTFOLIO BUILD COMPLETE!")
    print("=" * 60)

if __name__ == "__main__":
    main()
