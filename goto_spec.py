import os
import sublime_plugin
from itertools import takewhile


class GotoSpecCommand(sublime_plugin.WindowCommand):
    def run(self):
        file_path = self.window.active_view().file_name()
        rspec_file_path = file_path.replace(".rb", "_spec.rb")
        rspec_file_name = rspec_file_path.split('/')[-1]

        if not self.window.folders():
            return

        project_root = self.window.folders()[0]
        spec_folder = "%s/spec" % project_root

        if not os.access(spec_folder, os.R_OK):
            return

        files = list_files(spec_folder)
        matches = [common_start_len(f[::-1], rspec_file_path[::-1]) for f in files]

        if not matches:
            return

        perfect_match = files[matches.index(max(matches))]

        if not perfect_match.endswith(rspec_file_name):
            return

        if self.window.num_groups() > 1:
            self.window.focus_group(1)

        self.window.open_file(perfect_match)


def list_files(dirname):
    files = []
    for dirname, dirnames, filenames in os.walk(dirname):
        for filename in filenames:
            files.append(os.path.join(dirname, filename))
    return files


def common_start_len(a, b):
    return len(list(takewhile(lambda (x, y): x == y, zip(a, b))))
