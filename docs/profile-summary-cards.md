# Cached GitHub profile summary cards

Profile cards are generated once per day by GitHub Actions and served as static
SVGs from the **`profile-assets` branch**. The public README on `master`
references them with `raw.githubusercontent.com` URLs, so its images remain
available independently of the upstream Vercel card API.

## How it works

1. The workflow on `master` starts on the daily schedule or on manual dispatch.
2. GitHub Actions checks out `master` for source code and `profile-assets` in
   a separate working directory as the only publish target.
3. The pinned upstream card generator creates five SVGs in `github_dark` using
   UTC+3. It has `AUTO_PUSH: false`.
4. `scripts/validate_profile_cards.py` checks that every card is valid SVG,
   contains no known error text, and is linked from the README.
5. Only the five SVGs are copied into the asset-branch checkout. The workflow
   commits and pushes to **`profile-assets` only if a card actually changed**.
   It never pushes to `master`.

Daily refresh is scheduled for **03:17 UTC** (06:17 Türkiye time).
The README's images may be temporarily cached by GitHub's image proxy.

## Secrets and permissions

The workflow reads statistics with `SUMMARY_GITHUB_TOKEN`, falling back to
`GH_STATS_TOKEN` if set. Store one of these as a repository Actions secret
(Settings → Secrets and variables → Actions). A fine-grained PAT with public
repository read-only access is sufficient for public statistics. Never commit a
PAT to the repository.

The workflow's built-in `GITHUB_TOKEN` has `contents: write` only to commit the
SVG assets to `profile-assets`. This bot is the author of asset commits,
not the profile owner. These commits do not add noise to the `master` history.

To refresh manually, open **Actions → Refresh GitHub profile cards → Run workflow**
and choose the `master` branch. To inspect results, check:
`https://github.com/SwiftExplorer567/SwiftExplorer567/tree/profile-assets/profile-summary-card-output/github_dark`.

## Migration and recovery

The `profile-assets` branch was seeded from the last successful static card
generation *before* the README links were changed. This prevents broken images
during the migration. If a refresh fails, the existing assets remain intact.
Deleting `profile-assets` will break the README images; preserve the branch.

To include private-repository statistics, the API token would need additional
explicit read access. The default workflow does not request it.
