import ast
import asyncio
from collections import deque
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock


class RetryTests(unittest.IsolatedAsyncioTestCase):
    async def test_reloads_exact_track_once_then_skips(self):
        tree = ast.parse(Path('utils/music/models.py').read_text(encoding='utf-8'))
        branch = next(n for n in ast.walk(tree) if isinstance(n, ast.If)
                      and ast.unparse(n.test) == "track.source_name == 'youtube'"
                      and any(isinstance(x, ast.Assign) and any(
                          isinstance(t, ast.Name) and t.id == 'retry_key' for t in x.targets
                      ) for x in n.body))

        class EndEvent(ast.NodeTransformer):
            def visit_Continue(self, node):
                return ast.copy_location(ast.Return(value=None), node)

        wrapper = ast.parse('async def handle(self, track, send_report):\n    pass').body[0]
        wrapper.body = [EndEvent().visit(n) for n in branch.body]
        module = ast.fix_missing_locations(ast.Module(body=[wrapper], type_ignores=[]))
        namespace = {'asyncio': SimpleNamespace(sleep=AsyncMock()),
                     'get_start_pos': lambda player, track: 137680}
        exec(compile(module, '<youtube-error-handler>', 'exec'), namespace)
        node = SimpleNamespace(identifier='LOCAL')
        player = SimpleNamespace(node=node, queue=deque(), failed_tracks=[],
            bot=SimpleNamespace(music=SimpleNamespace(nodes={'LOCAL': node})),
            set_command_log=lambda **kwargs: None, process_next=AsyncMock(),
            text_channel=None, locked=True)
        track = SimpleNamespace(unique_id='original-video', id='old-encoded')
        report = AsyncMock()
        await namespace['handle'](player, track, report)
        self.assertIs(player.queue.popleft(), track)
        self.assertEqual(track.id, '')
        player.process_next.assert_awaited_with(start_position=137680)
        self.assertFalse(player.locked)
        await namespace['handle'](player, track, report)
        self.assertFalse(player.queue)
        self.assertEqual(player.failed_tracks, [track])
        player.process_next.assert_awaited_with()
        self.assertEqual(report.await_count, 2)


if __name__ == '__main__':
    unittest.main()
