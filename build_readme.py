"""Refresh the "Recently shipped" block in README.md.

Takes the newest release from each repository below, keeps the six most recent
across all of them, and rewrites the marked block. Run by
.github/workflows/update-readme.yml on a schedule.
"""
import json
import os
import pathlib
import re
import urllib.error
import urllib.request
from datetime import datetime

REPOS = [
    "AbdelmonemAwad/cadenza",
    "AbdelmonemAwad/os-linkhealth",
    "AbdelmonemAwad/os-netreport",
    "AbdelmonemAwad/os-frontpanel",
    "AbdelmonemAwad/opnsense-arabic",
    "AbdelmonemAwad/opnsense-rtl",
    "filamind-app/filamind-core",
    "filamind-app/filamind-flow",
    "filamind-app/filamind-screen",
    "filamind-app/filamind-3d",
    "filamind-app/filamind-ai",
    "filamind-app/filamind-setup",
    "deltafabs/filamind-iot",
    "deltafabs/filamind-iotbox",
    "deltafabs/filamind-iot-proxy",
]

COUNT = 6
README = pathlib.Path(__file__).parent / "README.md"
START, END = "<!-- releases starts -->", "<!-- releases ends -->"


def get(url):
    request = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "profile-readme-updater",
    })
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def latest_release(repo):
    try:
        releases = get(f"https://api.github.com/repos/{repo}/releases?per_page=20")
    except urllib.error.HTTPError as error:
        if error.code in (403, 404):
            return None
        raise
    # the API returns releases in creation order and includes drafts, so filter
    # to published, non-prerelease entries and pick the newest by date
    published = [r for r in releases
                 if not r.get("draft") and not r.get("prerelease") and r.get("published_at")]
    if not published:
        return None
    release = max(published, key=lambda r: r["published_at"])
    return {
        "name": repo.split("/")[1],
        "tag": release["tag_name"],
        "url": release["html_url"],
        "published": release["published_at"],
    }


def main():
    found = [release for release in map(latest_release, REPOS) if release]
    found.sort(key=lambda release: release["published"], reverse=True)

    lines = []
    for release in found[:COUNT]:
        day = datetime.strptime(release["published"][:10], "%Y-%m-%d").strftime("%d %b %Y")
        lines.append(f"- [**{release['name']}** {release['tag']}]({release['url']}) — {day}")

    block = f"{START}\n" + "\n".join(lines) + f"\n{END}"
    text = README.read_text(encoding="utf-8")
    updated = re.sub(re.escape(START) + r".*?" + re.escape(END), block, text, flags=re.S)

    if updated != text:
        README.write_text(updated, encoding="utf-8")
        print(f"updated {len(lines)} releases")
    else:
        print("no change")


if __name__ == "__main__":
    main()
