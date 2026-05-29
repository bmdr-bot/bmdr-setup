"""CLI commands for BMDR."""

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

from bmdr_cli.approval import ApprovalType, get_approval_gate
from bmdr_cli.config import get_config
from bmdr_cli.github_ops import get_github_ops
from bmdr_cli.opencode_ops import get_opencode_ops
from bmdr_cli.templates import TemplateEngine


def cmd_init(args: argparse.Namespace) -> int:
    """Initialize BMDR configuration."""
    config = get_config()
    
    print("🔧 Initializing BMDR CLI...")
    
    org = input(f"GitHub org/username [{config.github_org}]: ").strip()
    if org:
        config.set("github_org", org)
    
    projects_dir = input(f"Projects directory [{config.projects_dir}]: ").strip()
    if projects_dir:
        config.set("projects_base_dir", projects_dir)
        Path(projects_dir).expanduser().mkdir(parents=True, exist_ok=True)
    
    # Approval settings
    print("\n🛡️  Approval Gate Configuration")
    print("Critical operations requiring human approval:")
    
    require_prod = input("Require approval for production deployment? [Y/n]: ").strip().lower()
    if require_prod == "n":
        config.set("approvals.deploy_production", False)
    else:
        config.set("approvals.deploy_production", True)
    
    require_secret = input("Require approval for secret changes? [Y/n]: ").strip().lower()
    if require_secret == "n":
        config.set("approvals.secret_change", False)
    else:
        config.set("approvals.secret_change", True)
    
    require_infra = input("Require approval for infrastructure changes? [Y/n]: ").strip().lower()
    if require_infra == "n":
        config.set("approvals.infra_change", False)
    else:
        config.set("approvals.infra_change", True)
    
    print(f"\n✅ Config saved to {config.CONFIG_FILE}")
    return 0


def cmd_create(args: argparse.Namespace) -> int:
    """Create a new project from template."""
    config = get_config()
    project_name = args.name
    template = args.template or "default"
    
    print(f"🚀 Creating project: {project_name}")
    print(f"📋 Template: {template}")
    
    if args.dir:
        project_dir = Path(args.dir).expanduser()
    else:
        project_dir = config.projects_dir / project_name
    
    if project_dir.exists():
        print(f"❌ Directory already exists: {project_dir}")
        return 1
    
    project_dir.mkdir(parents=True)
    
    variables = {
        "project_name": project_name,
        "project_slug": project_name.lower().replace(" ", "-"),
        "github_org": config.github_org,
        "author": args.author or "BMDR",
        "description": args.description or f"{project_name} - A BMDR project",
        "python_version": config.get("project_defaults.python_version", "3.11"),
        "fastapi_version": config.get("project_defaults.fastapi_version", "0.109.0"),
        "license": config.get("project_defaults.license", "MIT"),
        "year": "2024",
    }
    
    templates_dir = Path(__file__).parent.parent / "templates"
    engine = TemplateEngine(templates_dir)
    
    try:
        engine.copy_template(template, project_dir, variables)
    except ValueError as e:
        print(f"❌ {e}")
        return 1
    
    # Initialize git
    subprocess.run(["git", "init"], cwd=project_dir, check=True, capture_output=True)
    subprocess.run(["git", "add", "."], cwd=project_dir, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", f"feat: initial {project_name} setup"],
        cwd=project_dir,
        check=True,
        capture_output=True,
    )
    
    print(f"✅ Project created: {project_dir}")
    
    # Create GitHub repo if requested
    if args.github:
        print("🌐 Creating GitHub repository...")
        try:
            gh = get_github_ops()
            repo = gh.create_repo(
                name=variables["project_slug"],
                description=variables["description"],
                private=args.private,
                org=config.github_org if args.org else None,
            )
            
            remote_url = repo["clone_url"].replace("https://", f"https://{gh.token}@")
            subprocess.run(
                ["git", "remote", "add", "origin", remote_url],
                cwd=project_dir,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "branch", "-m", "main"],
                cwd=project_dir,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "push", "-u", "origin", "main"],
                cwd=project_dir,
                check=True,
                capture_output=True,
            )
            
            print(f"✅ GitHub repo: {repo['html_url']}")
            
            if args.protect:
                gh.create_branch_protection(config.github_org, variables["project_slug"])
                print("🔒 Branch protection enabled")
                
        except Exception as e:
            print(f"⚠️ GitHub setup failed: {e}")
    
    print("")
    print("Next steps:")
    print(f"  cd {project_dir}")
    print("  cp .env.example .env")
    print("  ./scripts/run-local.sh")
    
    return 0


def cmd_dev(args: argparse.Namespace) -> int:
    """Start development session with OpenCode."""
    project_dir = Path(args.dir) if args.dir else Path.cwd()
    
    if not (project_dir / ".git").exists():
        print(f"❌ Not a git repository: {project_dir}")
        return 1
    
    print(f"🚀 Starting OpenCode development session in {project_dir}")
    
    try:
        oc = get_opencode_ops()
        print(f"OpenCode version: {oc.version()}")
        
        if args.task:
            print(f"\n📝 Task: {args.task}")
            print("Running OpenCode... (this may take a while)")
            
            result = oc.run_task(
                prompt=args.task,
                workdir=project_dir,
                model=args.model,
                thinking=args.thinking,
                timeout=args.timeout,
            )
            
            if result["success"]:
                print("\n✅ Task completed successfully")
                print("\nOutput:")
                print(result["stdout"])
            else:
                print("\n❌ Task failed")
                print(result["stderr"])
                return 1
        else:
            print("\n💡 No task specified. Use --task 'your task here'")
            print("Starting interactive session...")
            # Would start interactive session here
            
    except RuntimeError as e:
        print(f"❌ {e}")
        return 1
    
    return 0


def cmd_review(args: argparse.Namespace) -> int:
    """Review PR with OpenCode."""
    project_dir = Path(args.dir) if args.dir else Path.cwd()
    
    if not args.pr:
        print("❌ PR number required. Use --pr <number>")
        return 1
    
    print(f"🔍 Reviewing PR #{args.pr} with OpenCode...")
    
    try:
        oc = get_opencode_ops()
        result = oc.review_pr(
            pr_number=args.pr,
            workdir=project_dir,
            model=args.model,
        )
        
        if result["success"]:
            print("\n✅ Review completed")
            print(result["stdout"])
        else:
            print("\n❌ Review failed")
            print(result["stderr"])
            return 1
            
    except RuntimeError as e:
        print(f"❌ {e}")
        return 1
    
    return 0


def cmd_template(args: argparse.Namespace) -> int:
    """List or manage templates."""
    templates_dir = Path(__file__).parent.parent / "templates"
    engine = TemplateEngine(templates_dir)
    
    if args.action == "list":
        templates = engine.list_templates()
        if templates:
            print("📋 Available templates:")
            for t in templates:
                print(f"  • {t}")
        else:
            print("No templates found")
        return 0
    
    elif args.action == "add":
        print("Use 'bmdr create <name> --template <template_name>' to use a template")
        return 0
    
    return 1


def cmd_deploy(args: argparse.Namespace) -> int:
    """Deploy project to target environment."""
    config = get_config()
    project_dir = Path(args.dir) if args.dir else Path.cwd()
    target = args.target or "docker"
    
    # Check approval requirements
    gate = get_approval_gate()
    
    if target == "production":
        approval_type = ApprovalType.DEPLOY_PRODUCTION
        if gate.requires_approval(approval_type):
            req = gate.request(
                approval_type=approval_type,
                title=f"Deploy {project_dir.name} to production",
                description=f"Production deployment requested for {project_dir.name}",
                metadata={"project": str(project_dir), "target": target},
            )
            
            if req:
                print(f"⏳ Waiting for approval: {req.id}")
                if not gate.wait_for_approval(req.id):
                    return 1
    
    print(f"🚀 Deploying to {target}...")
    
    if target == "docker":
        compose_file = project_dir / "docker-compose.prod.yml"
        if not compose_file.exists():
            print(f"❌ {compose_file} not found")
            return 1
        
        subprocess.run(
            ["docker-compose", "-f", str(compose_file), "up", "-d"],
            cwd=project_dir,
            check=True,
        )
        print("✅ Deployed with Docker Compose")
        
    elif target == "kubernetes":
        k8s_dir = project_dir / "k8s"
        if not k8s_dir.exists():
            print(f"❌ {k8s_dir} not found")
            return 1
        
        subprocess.run(
            ["kubectl", "apply", "-k", str(k8s_dir)],
            check=True,
        )
        print("✅ Deployed to Kubernetes")
        
    elif target == "cloudflare":
        print("🌐 Starting Cloudflare tunnel...")
        subprocess.run(
            ["docker-compose", "-f", "docker-compose.prod.yml", "up", "-d", "tunnel"],
            cwd=project_dir,
            check=True,
        )
        print("✅ Cloudflare tunnel started")
    
    return 0


def cmd_approve(args: argparse.Namespace) -> int:
    """Approve a pending request."""
    gate = get_approval_gate()
    
    if args.request_id:
        if gate.store.approve(args.request_id, args.approver or os.getenv("USER", "unknown")):
            print(f"✅ Approved request: {args.request_id}")
            return 0
        else:
            print(f"❌ Failed to approve request: {args.request_id}")
            return 1
    
    # List pending requests
    pending = gate.store.list_pending()
    if not pending:
        print("No pending approval requests")
        return 0
    
    print("\n📋 Pending Approval Requests:")
    print("-" * 60)
    for req in pending:
        print(f"ID: {req.id}")
        print(f"Type: {req.type.value}")
        print(f"Title: {req.title}")
        print(f"Requester: {req.requester}")
        print(f"Expires in: {req.expires_at - __import__('time').time():.0f}s")
        print("-" * 60)
    
    return 0


def cmd_reject(args: argparse.Namespace) -> int:
    """Reject a pending request."""
    gate = get_approval_gate()
    
    if not args.request_id:
        print("❌ Request ID required")
        return 1
    
    if gate.store.reject(
        args.request_id,
        args.approver or os.getenv("USER", "unknown"),
        args.reason or "",
    ):
        print(f"❌ Rejected request: {args.request_id}")
        return 0
    else:
        print(f"❌ Failed to reject request: {args.request_id}")
        return 1


def cmd_skill(args: argparse.Namespace) -> int:
    """Manage Hermes skills."""
    skills_dir = Path.home() / ".hermes" / "skills"
    
    if args.action == "list":
        if skills_dir.exists():
            skills = [d.name for d in skills_dir.iterdir() if d.is_dir()]
            print("📚 Installed skills:")
            for skill in sorted(skills):
                print(f"  • {skill}")
        else:
            print("No skills directory found")
        return 0
    
    elif args.action == "install":
        print(f"📥 Installing skill: {args.skill_name}")
        return 0
    
    elif args.action == "create":
        print(f"🛠️  Creating skill template: {args.skill_name}")
        return 0
    
    return 1


def cmd_pr(args: argparse.Namespace) -> int:
    """Create a pull request from template."""
    config = get_config()
    
    templates_dir = Path(__file__).parent.parent / "templates" / "pr"
    template_file = templates_dir / f"{args.template}.md" if args.template else templates_dir / "default.md"
    
    if not template_file.exists():
        template_file = templates_dir / "default.md"
    
    with open(template_file) as f:
        body = f.read()
    
    body = body.replace("{{title}}", args.title)
    body = body.replace("{{description}}", args.description or "")
    body = body.replace("{{author}}", args.author or "BMDR")
    
    print(f"📝 PR Title: {args.title}")
    print(f"📋 Body:\n{body[:200]}...")
    
    if args.create:
        try:
            gh = get_github_ops()
            repo = args.repo or Path.cwd().name
            pr = gh.create_pr(
                owner=config.github_org,
                repo=repo,
                title=args.title,
                body=body,
                head=args.head,
                base=args.base or "main",
            )
            print(f"✅ PR created: {pr['html_url']}")
        except Exception as e:
            print(f"❌ Failed to create PR: {e}")
            return 1
    
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="bmdr",
        description="BMDR CLI - Project scaffolding and management",
    )
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # init
    init_parser = subparsers.add_parser("init", help="Initialize BMDR configuration")
    init_parser.set_defaults(func=cmd_init)
    
    # create
    create_parser = subparsers.add_parser("create", help="Create a new project")
    create_parser.add_argument("name", help="Project name")
    create_parser.add_argument("--template", "-t", help="Template to use")
    create_parser.add_argument("--dir", "-d", help="Target directory")
    create_parser.add_argument("--author", "-a", help="Project author")
    create_parser.add_argument("--description", help="Project description")
    create_parser.add_argument("--github", "-g", action="store_true", help="Create GitHub repo")
    create_parser.add_argument("--private", action="store_true", help="Private repository")
    create_parser.add_argument("--org", action="store_true", help="Use organization")
    create_parser.add_argument("--protect", action="store_true", help="Enable branch protection")
    create_parser.set_defaults(func=cmd_create)
    
    # dev (OpenCode)
    dev_parser = subparsers.add_parser("dev", help="Start OpenCode development session")
    dev_parser.add_argument("--dir", "-d", help="Project directory")
    dev_parser.add_argument("--task", help="Task for OpenCode")
    dev_parser.add_argument("--model", help="Model override")
    dev_parser.add_argument("--thinking", action="store_true", help="Show thinking")
    dev_parser.add_argument("--timeout", type=int, default=300, help="Timeout in seconds")
    dev_parser.set_defaults(func=cmd_dev)
    
    # review (OpenCode)
    review_parser = subparsers.add_parser("review", help="Review PR with OpenCode")
    review_parser.add_argument("--pr", type=int, required=True, help="PR number")
    review_parser.add_argument("--dir", "-d", help="Project directory")
    review_parser.add_argument("--model", help="Model override")
    review_parser.set_defaults(func=cmd_review)
    
    # template
    template_parser = subparsers.add_parser("template", help="Manage templates")
    template_parser.add_argument("action", choices=["list", "add"], help="Action")
    template_parser.set_defaults(func=cmd_template)
    
    # deploy
    deploy_parser = subparsers.add_parser("deploy", help="Deploy project")
    deploy_parser.add_argument("--target", "-t", choices=["docker", "kubernetes", "cloudflare", "production"], help="Deployment target")
    deploy_parser.add_argument("--dir", "-d", help="Project directory")
    deploy_parser.set_defaults(func=cmd_deploy)
    
    # approve
    approve_parser = subparsers.add_parser("approve", help="Approve pending request")
    approve_parser.add_argument("request_id", nargs="?", help="Request ID to approve")
    approve_parser.add_argument("--approver", help="Approver name")
    approve_parser.set_defaults(func=cmd_approve)
    
    # reject
    reject_parser = subparsers.add_parser("reject", help="Reject pending request")
    reject_parser.add_argument("request_id", help="Request ID to reject")
    reject_parser.add_argument("--approver", help="Approver name")
    reject_parser.add_argument("--reason", help="Rejection reason")
    reject_parser.set_defaults(func=cmd_reject)
    
    # skill
    skill_parser = subparsers.add_parser("skill", help="Manage Hermes skills")
    skill_parser.add_argument("action", choices=["list", "install", "create"], help="Action")
    skill_parser.add_argument("skill_name", nargs="?", help="Skill name")
    skill_parser.set_defaults(func=cmd_skill)
    
    # pr
    pr_parser = subparsers.add_parser("pr", help="Create pull request")
    pr_parser.add_argument("title", help="PR title")
    pr_parser.add_argument("--head", required=True, help="Head branch")
    pr_parser.add_argument("--base", default="main", help="Base branch")
    pr_parser.add_argument("--description", "-d", help="PR description")
    pr_parser.add_argument("--template", "-t", help="PR template")
    pr_parser.add_argument("--author", "-a", help="Author")
    pr_parser.add_argument("--repo", "-r", help="Repository name")
    pr_parser.add_argument("--create", "-c", action="store_true", help="Create on GitHub")
    pr_parser.set_defaults(func=cmd_pr)
    
    args = parser.parse_args(argv)
    
    if not args.command:
        parser.print_help()
        return 1
    
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
