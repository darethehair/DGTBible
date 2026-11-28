"""Exercise the recorded player in Chromium using a real Opus clip and controlled HTTP responses."""

import argparse
from collections import Counter
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
from threading import Thread

from playwright.sync_api import expect, sync_playwright


ROOT = Path(__file__).resolve().parents[1]
LIBRARY = "https://darethehair.github.io/DGTBible-Audio/dgt-audio-24k/"
JOHN = [f"slot-02/John/001/{verse:03}.opus" for verse in range(1, 52)]
CROSS_CHAPTER = "slot-02/John/002/001.opus"
ROMANS = "slot-02/Romans/001/005.opus"


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


def check(browser, url, clip):
    page = browser.new_page(viewport={"width": 390, "height": 844}, service_workers="block")
    files, responses, requests, errors = JOHN.copy(), {}, Counter(), []
    page.emulate_media(reduced_motion="reduce")
    page.on("pageerror", lambda error: errors.append(str(error)))

    def audio_route(route):
        path = route.request.url.removeprefix(LIBRARY).split("?")[0]
        headers = {"access-control-allow-origin": "*"}
        if path == "availability.json":
            route.fulfill(json={"version": 1, "files": files}, headers=headers)
            return
        requests[path] += 1
        status = responses.get(path, 200 if path in files else 404)
        route.fulfill(status=status, headers=headers, body=clip if status == 200 else b"", content_type="audio/ogg")

    page.route(LIBRARY + "**", audio_route)
    page.goto(url)
    expect(page.locator("#reference")).to_have_text("John 1:1")
    assert not requests
    page.locator("#ref").fill("Jn 1:18")
    page.get_by_role("button", name="Go", exact=True).click()
    expect(page.locator("#reference")).to_have_text("John 1:18")
    page.locator("#ref").fill("John 1:1-10, Romans 1:5")
    page.get_by_role("button", name="Go", exact=True).click()
    expect(page.locator("#reference")).to_have_text("John 1:1")
    expect(page.locator("#ref")).to_have_value("John 1:1-10, Romans 1:5")
    page.locator("#themeSelect").select_option("dark")
    page.locator("#openAudio").click()
    expect(page.locator("#audioNarrator")).to_have_value("02")
    expect(page.locator("#audioAvailability")).to_have_text("10 of 11 verses recorded")
    assert not requests
    assert page.evaluate("document.documentElement.scrollWidth === innerWidth")

    def select(text, coverage=None):
        page.locator("#audioPassage").fill(text)
        if coverage:
            expect(page.locator("#audioAvailability")).to_have_text(coverage)

    def play():
        page.locator("#audioPlay").click()

    select("John 2", "0 of 25 verses recorded")
    play()
    expect(page.locator("#audioStatus")).to_contain_text("No recordings are available")
    expect(page.locator("#audioStatus")).to_contain_text("Skipped 25 missing")
    assert not requests

    page.locator("#audioNarrator").select_option("01")
    select("John 1:1", "0 of 1 verses recorded")
    play()
    expect(page.locator("#audioStatus")).to_contain_text("No recordings are available")
    assert not requests

    page.locator("#audioNarrator").select_option("02")
    page.locator("#audioRate").select_option("1.5")
    page.locator("#audioScroll").uncheck()
    for reference, expected in [
        ("John 1", "51 of 51 verses recorded"), ("John 1-3", "51 of 112 verses recorded"),
        ("John 1:14–3:16", "38 of 79 verses recorded"),
        ("John", "51 of 878 verses recorded"), ("the entire NT", "51 of 7,939 verses recorded"),
    ]:
        select(reference, expected)
    assert not requests

    responses[JOHN[1]] = 404
    select("John 1:1–4", "4 of 4 verses recorded")
    play()
    expect(page.locator("#audioSummary")).to_contain_text("John 1:1")
    expect(page.locator("#verseCard")).to_have_class("verse-card audio-current")
    expect(page.locator("#audioProgress")).to_be_visible()
    page.wait_for_function('document.querySelector("#audioProgress").value > 0')
    assert set(requests) == {JOHN[0], JOHN[1]}
    assert page.locator("#recordedAudio").evaluate("(audio) => audio.playbackRate === 1.5 && audio.preservesPitch")
    page.locator("#english .align-token").first.hover()
    expect(page.locator("#greek .align-token.active").first).to_be_visible()
    play()
    expect(page.locator("#audioPlay")).to_have_text("Resume")
    expect(page.locator("#audioSummary")).to_contain_text("Paused")
    play()
    expect(page.locator("#audioPlay")).to_have_text("Pause")
    page.locator("#audioNext").click()
    expect(page.locator("#audioSummary")).to_contain_text("John 1:3")
    expect(page.locator("#audioStatus")).to_contain_text("Skipped 1 missing (John 1:2)")
    page.locator("#audioPrevious").click()
    expect(page.locator("#audioSummary")).to_contain_text("John 1:1")
    page.locator("#audioNext").click()
    expect(page.locator("#audioSummary")).to_contain_text("John 1:3")
    assert requests[JOHN[1]] == 1
    page.get_by_role("button", name="Chapter", exact=True).click()
    expect(page.locator("#v3")).to_have_attribute("aria-current", "true")
    page.locator("#v3 .cv-dgt .align-token").first.click()
    expect(page.locator("#v3 .cv-greek .align-token.active").first).to_be_visible()
    page.get_by_role("button", name="Compact", exact=True).click()
    expect(page.locator("#compact-v3")).to_have_attribute("aria-current", "true")
    page.locator("#audioHide").click()
    expect(page.locator("#audioPanel")).not_to_have_attribute("open", "")
    page.locator("#audioPanel summary").click()
    page.locator("#audioStop").click()
    expect(page.locator(".audio-current")).to_have_count(0)

    responses[JOHN[4]] = 503
    select("John 1:5", "1 of 1 verses recorded")
    play()
    expect(page.locator("#audioStatus")).to_contain_text("1 temporary failure (John 1:5)")
    expect(page.locator("#audioRetry")).to_be_visible()
    responses[JOHN[4]] = 200
    page.locator("#audioRetry").click()
    expect(page.locator("#audioSummary")).to_contain_text("John 1:5")
    page.locator("#audioStop").click()

    files.extend([CROSS_CHAPTER, ROMANS])
    page.evaluate("(() => { const now = Date.now.bind(Date); Date.now = () => now() + 120000; })()")
    select("John 1:51–2:1, Romans 1:5", "3 of 3 verses recorded")
    play()
    expect(page.locator("#compact-v51")).to_have_attribute("aria-current", "true")
    play()
    expect(page.locator("#audioPlay")).to_have_text("Resume")
    page.locator("#audioScroll").check()
    page.wait_for_function("""() => {
        const verse = document.querySelector("#compact-v51")?.getBoundingClientRect();
        return verse && verse.top >= 0 && verse.bottom <= innerHeight - document.querySelector("#audioDock").offsetHeight;
    }""")
    page.locator("#audioScroll").uncheck()
    play()
    # Seek to the end of the clip to exercise native automatic advancement.
    page.locator("#recordedAudio").evaluate("(audio) => { audio.currentTime = audio.duration; }")
    expect(page.locator("#compactHeading")).to_have_text("John 2")
    expect(page.locator("#compact-v1")).to_have_attribute("aria-current", "true")
    page.locator("#audioNext").click()
    expect(page.locator("#compactHeading")).to_have_text("Romans 1")
    expect(page.locator("#compact-v5")).to_have_attribute("aria-current", "true")
    page.locator("#audioStop").click()
    page.locator("#audioNarrator").select_option("04")
    page.reload()
    page.locator("#openAudio").click()
    expect(page.locator("#audioNarrator")).to_have_value("04")
    expect(page.locator("#audioRate")).to_have_value("1.5")
    expect(page.locator("#audioScroll")).not_to_be_checked()
    assert not errors, errors
    print("Recorded audio passed Chromium mobile checks, including absent passages, 404, 503 retry, and cross-book sync.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("clip", type=Path, help="Path to a real .opus verse fixture")
    args = parser.parse_args()
    with ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=ROOT)) as server:
        Thread(target=server.serve_forever, daemon=True).start()
        with sync_playwright() as playwright:
            executable = os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE")
            browser = playwright.chromium.launch(executable_path=executable)
            check(browser, f"http://127.0.0.1:{server.server_port}/", args.clip.read_bytes())
