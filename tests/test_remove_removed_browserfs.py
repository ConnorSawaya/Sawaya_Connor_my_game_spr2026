import unittest

from scripts.remove_removed_browserfs import remove_removed_browserfs_script


class RemoveRemovedBrowserfsTests(unittest.TestCase):
    def test_removes_only_the_dead_loader_and_keeps_runtime_and_game_scripts(self):
        html = (
            '<!doctype html><head>'
            '<script src="https://pygame-web.github.io/cdn/0.9.3/pythons.js"></script>'
            '<script src="https://pygame-web.github.io/cdn/0.9.3//browserfs.min.js"></script>'
            '<script>window.gameReady = true;</script>'
            '</head>'
        )

        patched = remove_removed_browserfs_script(html)

        self.assertNotIn("browserfs.min.js", patched)
        self.assertIn("pythons.js", patched)
        self.assertIn("window.gameReady = true", patched)

    def test_fails_closed_if_the_pinned_template_no_longer_emits_browserfs(self):
        html = '<script src="https://pygame-web.github.io/cdn/0.9.3/pythons.js"></script>'

        with self.assertRaisesRegex(ValueError, "found 0"):
            remove_removed_browserfs_script(html)

    def test_fails_closed_if_browserfs_loader_is_duplicated(self):
        html = (
            '<script src="https://pygame-web.github.io/cdn/0.9.3/pythons.js"></script>'
            '<script src="https://pygame-web.github.io/cdn/0.9.3/browserfs.min.js"></script>'
            '<script src="https://other.example/browserfs.min.js"></script>'
        )

        with self.assertRaisesRegex(ValueError, "found 2"):
            remove_removed_browserfs_script(html)


if __name__ == "__main__":
    unittest.main()
