"""Display actionable YouTube authentication events without printing tokens."""

import re


class YoutubeOAuthConsole:
    def __init__(self, output=print):
        self.output = output
        self.warned = False
        self.oauth_context = 0

    def feed(self, line):
        text = line.lower()
        if "youtubeoauth2handler" in text or "oauth integration:" in text:
            self.oauth_context = 12
        else:
            self.oauth_context = max(0, self.oauth_context - 1)

        if ("youtube access token refreshed successfully" in text
                or "oauth integration: token retrieved successfully" in text):
            if self.warned:
                self.output("[YouTube / LOCAL] Autorização restabelecida.", flush=True)
            self.warned = False
            self.oauth_context = 0
            return

        needs_login = "oauth integration: to give youtube-source access" in text
        invalid_token = (
            (self.oauth_context or "refreshing access token returned error" in text)
            and any(error in text for error in (
                "invalid_grant", "invalid_token", "expired_token",
                "device token has expired", "token has been expired or revoked",
                "account linking was denied",
            ))
        )
        if not (needs_login or invalid_token):
            return

        if not self.warned:
            self.output(
                "\n" + "=" * 64 + "\n"
                "[YouTube / LOCAL] VOCÊ PRECISA RENOVAR O TOKEN\n"
                "A autorização do YouTube precisa ser feita novamente.\n"
                "Conclua o login do Google e atualize o refreshToken do Lavalink.\n"
                + "=" * 64 + "\n", flush=True,
            )
            self.warned = True

        if needs_login:
            code = re.search(r"enter code ([A-Z0-9-]+)\b", line)
            if code:
                self.output(
                    "[YouTube / LOCAL] Abra https://www.google.com/device e use o código: "
                    + code.group(1), flush=True,
                )


def watch_lavalink_output(stream):
    monitor = YoutubeOAuthConsole()
    with stream:
        for line in stream:
            monitor.feed(line)
