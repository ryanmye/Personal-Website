#!/usr/bin/env python3
"""
One-time script to obtain a Spotify refresh token for the GitHub Actions workflow.
Run this locally, then add the printed refresh token as SPOTIFY_REFRESH_TOKEN in
GitHub repo Settings → Secrets and variables → Actions.

Before running: In your Spotify app (developer.spotify.com/dashboard), add this
redirect URI: http://127.0.0.1:8888/callback
(Spotify requires 127.0.0.1, not localhost.)

Usage:
  python scripts/get-spotify-refresh-token.py
  # Or with env vars:
  SPOTIFY_CLIENT_ID=xxx SPOTIFY_CLIENT_SECRET=yyy python scripts/get-spotify-refresh-token.py
"""

import base64
import json
import os
import sys
import urllib.parse
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPE = "user-read-recently-played"
PORT = 8888


def main():
    client_id = os.environ.get("SPOTIFY_CLIENT_ID", "").strip()
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET", "").strip()

    if not client_id or not client_secret:
        print("Enter your Spotify app credentials (from developer.spotify.com/dashboard):")
        if not client_id:
            client_id = input("Client ID: ").strip()
        if not client_secret:
            client_secret = input("Client Secret: ").strip()
        if not client_id or not client_secret:
            print("Error: Client ID and Client Secret are required.", file=sys.stderr)
            sys.exit(1)

    auth_params = urllib.parse.urlencode({
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
    })
    auth_url = f"https://accounts.spotify.com/authorize?{auth_params}"

    code_received = []

    class CallbackHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            if parsed.path == "/callback":
                params = urllib.parse.parse_qs(parsed.query)
                code = params.get("code", [None])[0]
                error = params.get("error", [None])[0]
                if error:
                    code_received.append(("error", error))
                elif code:
                    code_received.append(("code", code))
                else:
                    code_received.append(("error", "No code in redirect"))
            else:
                code_received.append(("error", "Unexpected path"))

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            if code_received[0][0] == "code":
                self.wfile.write(
                    b"<html><body><p>Success! You can close this tab and return to the terminal.</p></body></html>"
                )
            else:
                self.wfile.write(
                    b"<html><body><p>Error: check the terminal for details.</p></body></html>"
                )

        def log_message(self, format, *args):
            pass

    print("\n1. Opening browser for Spotify authorization...")
    print("   If it doesn't open, visit this URL manually:\n")
    print(f"   {auth_url}\n")
    try:
        import webbrowser
        webbrowser.open(auth_url)
    except Exception:
        pass

    print("2. Log in to Spotify and approve the app.")
    print("3. Waiting for redirect on http://127.0.0.1:8888/callback ...\n")

    server = HTTPServer(("", PORT), CallbackHandler)
    server.handle_request()

    if not code_received:
        print("Error: No response received. Did you complete the authorization?", file=sys.stderr)
        sys.exit(1)

    kind, value = code_received[0]
    if kind == "error":
        print(f"Error: {value}", file=sys.stderr)
        sys.exit(1)

    code = value
    print("4. Exchanging authorization code for tokens...")

    credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    token_body = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }).encode()
    token_req = urllib.request.Request(
        "https://accounts.spotify.com/api/token",
        data=token_body,
        headers={
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(token_req) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"Error from Spotify: {e.code} {body}", file=sys.stderr)
        sys.exit(1)

    refresh_token = data.get("refresh_token")
    if not refresh_token:
        print("Error: No refresh_token in response.", file=sys.stderr)
        sys.exit(1)

    print("\n" + "=" * 60)
    print("SUCCESS! Add this as GitHub secret SPOTIFY_REFRESH_TOKEN:")
    print("=" * 60)
    print(refresh_token)
    print("=" * 60)
    print("\nGo to: GitHub repo → Settings → Secrets and variables → Actions")
    print("Create secret: SPOTIFY_REFRESH_TOKEN")
    print("Paste the value above, then add SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET too.\n")


if __name__ == "__main__":
    main()
