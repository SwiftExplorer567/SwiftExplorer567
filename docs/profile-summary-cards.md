# Cached GitHub profile summary cards

The five GitHub profile statistics cards previously loaded from a shared Vercel
endpoint, which can return a **rate-limit error image**. This workflow instead
generates the upstream SVGs in GitHub Actions and stores them in this repository.

## One-time setup

1. Create a **fine-grained personal access token** at
   https://github.com/settings/personal-access-tokens/new with access to
   **Public repositories (read-only)**. Keep its permissions read-only.
2. Go to this repository's **Settings → Secrets and variables → Actions** and
   add it as a repository secret named **`SUMMARY_GITHUB_TOKEN`**.
   An existing **`GH_STATS_TOKEN`** secret is also supported as a fallback.
   Never commit a token to the repository.
3. Merge the PR adding the workflow. It will run automatically after that merge
   (if GitHub Actions is enabled), and you can also go to
   **Actions → Refresh GitHub profile cards → Run workflow** to trigger it.
4. Check the workflow run. Once **all five cards** generate successfully,
   the workflow commits them under
   `profile-summary-card-output/github_dark/` and replaces the old Vercel
   image URLs in `README.md`. Before this first successful run, the old
   URLs are intentionally left untouched to avoid broken local image links.

After initial setup, the cards refresh daily at **03:17 UTC** (06:17 Türkiye time)
and remain visible even if the upstream hosted API is temporarily unavailable.
GitHub may cache README images briefly after the first successful run.

## Implementation notes

- **Rendering:** upstream `vn7n24fzkq/github-profile-summary-cards` GitHub
  Action, pinned to a reviewed commit from its `release` branch.
- **Theme and time zone:** `github_dark`, `UTC+3`.
- **Safety:** the upstream Action cannot push (`AUTO_PUSH: false`);
  `scripts/sync_profile_cards.py` validates all five SVGs before replacing
  README URLs. Only the repository's built-in Actions token pushes generated
  files. The personal token is used only for reading GitHub API statistics.
- **Manual refresh:** use `workflow_dispatch` from the Actions tab.
- **Private stats:** a public-repositories-only token deliberately does not
  grant access to private repository activity.
