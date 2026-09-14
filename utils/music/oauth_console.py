"""Handle actionable YouTube authentication events without printing tokens."""

import os
import re
from typing import Callable, Optional

import ruamel.yaml


REFRESH_TOKEN_RE = re.compile(
    r"oauth integration: token retrieved successfully.*\((1//[^)\s]+)\)",
    flags=re.IGNORECASE,
)


def save_refresh_token(refresh_token: str, config_path="./application.yml") -> bool:
    """Persist a token emitted by youtube-source without exposing it in logs."""
    if not refresh_token or not os.path.isfile(config_path):
        return False

    yaml = ruamel.yaml.YAML()
    yaml.preserve_quotes = True
    with open(config_path, "r", encoding="utf-8") as stream:
        data = yaml.load(stream) or {}

    plugins = data.setdefault("plugins", {})
    youtube = plugins.setdefault("youtube", {})
    oauth = youtube.setdefault("oauth", {})
    oauth.update({
        "enabled": True,
        "skipInitialization": True,
        "refreshToken": refresh_token,
    })

    temporary_path = config_path + ".tmp"
    try:
        with open(temporary_path, "w", encoding="utf-8") as stream:
            yaml.dump(data, stream)
        os.replace(temporary_path, config_path)
    finally:
        if os.path.exists(temporary_path):
            os.remove(temporary_path)
    return True


class YoutubeOAuthConsole:
    def __init__(
        self,
        output=print,
        token_handler: Optional[Callable[[str], bool]] = None,
    ):
        self.output = output
        self.token_handler = token_handler
        self.warned = False
        self.oauth_context = 0

    def feed(self, line):
        text = line.lower()
        if "youtubeoauth2handler" in text or "oauth integration:" in text:
            self.oauth_context = 12
        else:
            self.oauth_context = max(0, self.oauth_context - 1)

        token_match = REFRESH_TOKEN_RE.search(line)
        token_retrieved = "oauth integration: token retrieved successfully" in text

        if "youtube access token refreshed successfully" in text or token_retrieved:
            if token_match and self.token_handler:
                try:
                    if self.token_handler(token_match.group(1)):
                        self.output(
                            "[YouTube / LOCAL] Novo refreshToken salvo automaticamente no application.yml.",
                            flush=True,
                        )
                    else:
                        self.output(
                            "[YouTube / LOCAL] Login concluído, mas o application.yml não foi encontrado para salvar o token.",
                            flush=True,
                        )
                except Exception as exc:
                    self.output(
                        f"[YouTube / LOCAL] Login concluído, mas não foi possível salvar o token: {exc}",
                        flush=True,
                    )
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
                "Conclua o login do Google; o novo refreshToken será salvo automaticamente.\n"
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


def watch_lavalink_output(stream, config_path="./application.yml"):
    monitor = YoutubeOAuthConsole(
        token_handler=lambda token: save_refresh_token(token, config_path),
    )
    with stream:
        for line in stream:
            monitor.feed(line)
