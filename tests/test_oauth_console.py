import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout

import ruamel.yaml

from utils.music.oauth_console import YoutubeOAuthConsole, save_refresh_token, watch_lavalink_output


class OAuthConsoleTests(unittest.TestCase):
    def test_revoked_token_warns_once_and_recovers(self):
        output = []
        monitor = YoutubeOAuthConsole(lambda message, **kw: output.append(message))
        for _ in range(2):
            monitor.feed('YoutubeOauth2Handler : Refreshing YouTube access token failed')
            monitor.feed('Caused by: Refreshing access token returned error invalid_grant')
        self.assertEqual(len(output), 1)
        self.assertIn('VOCÊ PRECISA RENOVAR O TOKEN', output[0])
        monitor.feed('YoutubeOauth2Handler : YouTube access token refreshed successfully')
        monitor.feed('Refreshing access token returned error invalid_grant')
        self.assertEqual(len(output), 3)

    def test_normal_refresh_network_and_audio_errors_do_not_request_login(self):
        output = []
        monitor = YoutubeOAuthConsole(lambda message, **kw: output.append(message))
        for line in (
            'YoutubeOauth2Handler : Access token has expired, refreshing...',
            'YoutubeOauth2Handler : YouTube access token refreshed successfully',
            'YoutubeOauth2Handler : Refreshing YouTube access token failed',
            'java.net.SocketTimeoutException: Read timed out',
            'Client [ANDROID_VR] failed: This video requires login.',
            'Expected decoding to halt, got: 16394',
        ):
            monitor.feed(line)
        self.assertEqual(output, [])

    def test_device_login_and_token_redaction(self):
        stream = io.StringIO(
            'OAUTH INTEGRATION: To give youtube-source access to your account, '
            'go to https://www.google.com/device and enter code ABC-123-XYZ\n'
            'OAUTH INTEGRATION: Token retrieved successfully. Store your refresh token (SECRET)\n'
        )
        output = io.StringIO()
        with redirect_stdout(output):
            watch_lavalink_output(stream)
        self.assertIn('ABC-123-XYZ', output.getvalue())
        self.assertNotIn('SECRET', output.getvalue())
        self.assertIn('Autorização restabelecida', output.getvalue())
        self.assertTrue(stream.closed)

    def test_unrelated_token_is_ignored(self):
        output = []
        monitor = YoutubeOAuthConsole(lambda message, **kw: output.append(message))
        monitor.feed('Spotify: invalid_grant')
        self.assertEqual(output, [])

    def test_new_token_is_saved_without_being_printed(self):
        token = "1//AUTOMATIC_TEST_TOKEN"
        with tempfile.TemporaryDirectory() as directory:
            config_path = os.path.join(directory, "application.yml")
            with open(config_path, "w", encoding="utf-8") as stream:
                stream.write("plugins:\n  youtube:\n    oauth:\n      enabled: true\n")

            output = []
            monitor = YoutubeOAuthConsole(
                lambda message, **kw: output.append(message),
                token_handler=lambda value: save_refresh_token(value, config_path),
            )
            monitor.feed(
                "OAUTH INTEGRATION: Token retrieved successfully. "
                f"Store your refresh token as this can be reused. ({token})"
            )

            yaml = ruamel.yaml.YAML(typ="safe")
            with open(config_path, "r", encoding="utf-8") as stream:
                oauth = yaml.load(stream)["plugins"]["youtube"]["oauth"]

        self.assertEqual(oauth["refreshToken"], token)
        self.assertTrue(oauth["skipInitialization"])
        self.assertNotIn(token, "\n".join(output))
        self.assertTrue(any("salvo automaticamente" in message for message in output))


if __name__ == '__main__':
    unittest.main()
