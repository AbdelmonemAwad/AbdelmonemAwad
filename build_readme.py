"""Refresh the "Recently merged" block in README.md.

Lists the newest merged pull requests this account wrote in public
repositories, leaving out housekeeping. Run by
.github/workflows/update-readme.yml on a schedule.
"""
import json
import os
import pathlib
import re
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

AUTHOR = "AbdelmonemAwad"
COUNT = 6
# titles that describe upkeep rather than a finding
SKIP = ("docs:", "doc:", "chore:", "ci:", "build:", "style:", "test:", "bump ", "merge ")
# a pull request that changes only these is the repository's upkeep, whatever its title
UPKEEP = re.compile(r"\.github/|(SECURITY|CODE_OF_CONDUCT|CONTRIBUTING)\.md$|LICENSE|\.gitignore$")

README = pathlib.Path(__file__).parent / "README.md"
START, END = "<!-- merged starts -->", "<!-- merged ends -->"


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


def upkeep_only(row):
    files = get(f"{row['api']}/files?per_page=100")
    return bool(files) and all(UPKEEP.match(f["filename"]) for f in files)


def merged():
    query = urllib.parse.quote(f"is:pr is:merged is:public author:{AUTHOR}")
    found = get("https://api.github.com/search/issues"
                f"?q={query}&sort=updated&order=desc&per_page=50")
    rows = []
    for item in found.get("items", []):
        title = " ".join(item["title"].split())
        if title.lower().startswith(SKIP):
            continue
        rows.append({
            "title": title,
            "url": item["html_url"],
            "repo": item["repository_url"].rsplit("/", 1)[-1],
            "merged": item["pull_request"]["merged_at"],
            "api": item["pull_request"]["url"],
        })
    # the search orders by last update, which is not always the merge
    rows.sort(key=lambda row: row["merged"], reverse=True)
    picked = []
    for row in rows:
        if len(picked) == COUNT:
            break
        if not upkeep_only(row):
            picked.append(row)
    return picked


def escape(text):
    backslash = chr(92)
    for char in "[]":
        text = text.replace(char, backslash + char)
    return text.replace("<", "&lt;").replace(">", "&gt;")


def main():
    try:
        rows = merged()
    except urllib.error.HTTPError as error:
        # a rate limit should leave yesterday's list standing, not fail the run
        print(f"search unavailable ({error.code}), README left as it is")
        return
    if not rows:
        print("nothing found, README left as it is")
        return

    lines = []
    for row in rows:
        day = datetime.strptime(row["merged"][:10], "%Y-%m-%d").strftime("%d %b")
        lines.append(f"- [{escape(row['title'])}]({row['url']}) — **{row['repo']}**, {day}")

    block = f"{START}\n" + "\n".join(lines) + f"\n{END}"
    text = README.read_text(encoding="utf-8")
    updated = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, text, flags=re.S)

    if updated != text:
        README.write_text(updated, encoding="utf-8")
        print(f"updated {len(lines)} entries")
    else:
        print("no change")


if __name__ == "__main__":
    main()
