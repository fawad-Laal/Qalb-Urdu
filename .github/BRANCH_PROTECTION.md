# Branch Protection Rules

This document outlines the recommended branch protection rules for the Qalb-Urdu repository to prevent accidental or malicious deletions and maintain code quality.

## Recommended Protection Rules

### For the `main` branch:

1. **Require pull request reviews before merging**
   - At least 1 approval required
   - Dismiss stale pull request approvals when new commits are pushed
   - Require review from Code Owners (see CODEOWNERS file)

2. **Require status checks to pass before merging**
   - Require branches to be up to date before merging
   - Status checks required: (configure based on your CI/CD setup)
     - Code quality checks
     - Security scans
     - Tests (if applicable)

3. **Require conversation resolution before merging**
   - All PR comments must be resolved

4. **Require signed commits** (recommended for high-security projects)
   - Ensures commits are verified

5. **Include administrators**
   - Apply these rules to repository administrators as well

6. **Restrict deletions**
   - ✅ **Block force pushes**
   - ✅ **Block branch deletions**

7. **Allow force pushes** - DISABLED
   - Do not allow force pushes to this branch

8. **Allow deletions** - DISABLED
   - Do not allow this branch to be deleted

## How to Apply These Rules

### Via GitHub Web Interface:

1. Go to your repository on GitHub
2. Click on **Settings** → **Branches**
3. Under "Branch protection rules", click **Add rule**
4. Enter `main` as the branch name pattern
5. Enable the following options:
   - ☑ Require a pull request before merging
     - ☑ Require approvals (1+)
     - ☑ Dismiss stale pull request approvals when new commits are pushed
     - ☑ Require review from Code Owners
   - ☑ Require status checks to pass before merging
     - ☑ Require branches to be up to date before merging
   - ☑ Require conversation resolution before merging
   - ☑ Do not allow bypassing the above settings
   - ☑ Restrict deletions
   - ☑ Block force pushes
6. Click **Create** or **Save changes**

### Via GitHub API or Terraform:

You can also configure these rules programmatically. See the `settings.yml` file for a configuration template.

## Additional Protection Measures

1. **CODEOWNERS File**: Define code ownership to ensure critical files are reviewed
2. **GitHub Actions**: Automated checks for code quality and security
3. **Protected Tags**: Protect release tags from deletion
4. **Repository Settings**: 
   - Disable force pushes at the repository level
   - Limit who can push to matching branches
   - Require linear history (optional)

## Verification

After applying these rules, verify they're working by:
1. Attempting to force push to main (should be blocked)
2. Attempting to delete the main branch (should be blocked)
3. Creating a PR and verifying review requirements

## Emergency Override

In case of emergency, repository administrators can temporarily disable branch protection rules via:
- Repository Settings → Branches → Edit rule → Temporarily disable

**Important**: Re-enable protection rules immediately after the emergency is resolved.

## References

- [GitHub Branch Protection Documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub Code Owners Documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
