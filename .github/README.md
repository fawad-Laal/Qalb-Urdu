# GitHub Configuration

This directory contains configuration files and documentation for protecting and maintaining the Qalb-Urdu repository.

## Files Overview

### 🛡️ Protection and Ownership

- **`CODEOWNERS`** - Defines code ownership for automatic review requests
  - Ensures critical files require approval from repository owner
  - Automatically requests reviews from designated code owners on PRs
  
- **`BRANCH_PROTECTION.md`** - Documentation for branch protection rules
  - Step-by-step guide to configure GitHub branch protection
  - Recommended settings to prevent force pushes and branch deletion
  - Instructions for applying protection via GitHub UI or API

- **`settings.yml`** - Repository settings template
  - YAML configuration for repository settings and branch protection
  - Can be used with Probot Settings app or as reference
  - Documents desired repository configuration

### 🔄 Automation

- **`workflows/repository-protection.yml`** - GitHub Actions workflow
  - Automatically validates protection mechanisms on PRs
  - Checks for CODEOWNERS file and critical file protection
  - Provides reminders about branch protection settings
  - Runs on all PRs to main branch

## Quick Start: Protecting Your Repository

To fully protect this repository from forced deletion and maintain code quality:

### 1. Apply Branch Protection Rules

Go to **GitHub Repository Settings → Branches** and apply the rules documented in `BRANCH_PROTECTION.md`:

```
☑ Require pull request reviews before merging (1+ approvals)
☑ Require review from Code Owners
☑ Block force pushes
☑ Block branch deletions
☑ Require status checks to pass before merging
☑ Require conversation resolution
☑ Do not allow bypassing the above settings
```

### 2. Verify CODEOWNERS

The `CODEOWNERS` file is already configured to protect:
- Configuration files (pyproject.toml, requirements.txt)
- Documentation (README.md, /docs/)
- GitHub configuration (/.github/)
- License file
- Test data and scripts

### 3. Enable GitHub Actions

Ensure GitHub Actions is enabled in **Settings → Actions** to run the repository-protection workflow.

### 4. Test Protection

Verify protection is working by:
1. Creating a test PR to main branch
2. Checking that reviews are required
3. Attempting to force push (should be blocked)

## What These Files Protect Against

✅ **Accidental branch deletion** - Branch protection prevents deletion of protected branches  
✅ **Force pushes** - Prevents rewriting commit history  
✅ **Unauthorized changes** - CODEOWNERS requires approval from designated reviewers  
✅ **Bypassing reviews** - Enforces PR review process even for administrators  
✅ **Lost work** - Requires conversation resolution before merging

## Maintenance

- Review and update `CODEOWNERS` when team structure changes
- Keep `BRANCH_PROTECTION.md` updated with current best practices
- Monitor `repository-protection.yml` workflow results in Actions tab

## Additional Resources

- [GitHub Branch Protection Documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [About Code Owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## Support

For questions or issues with repository protection:
- Review the documentation in this directory
- Check GitHub's official documentation
- Contact repository administrator: @fawad-Laal
