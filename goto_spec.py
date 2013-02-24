import os
import sublime_plugin
from itertools import takewhile


class GotoSpecCommand(sublime_plugin.WindowCommand):
    def run(self):
        if not self.window.folders():
            return

        file_path = self.window.active_view().file_name()
        searching_spec = not file_path.endswith("_spec.rb")

        if searching_spec:
            searched_file_path = file_path.replace(".rb", "_spec.rb")
        else:
            searched_file_path = file_path.replace("_spec.rb", ".rb")

        project_root = self.window.folders()[0]

        if searching_spec:
            search_path = "%s/spec" % project_root
        else:
            search_path = project_root

        perfect_match = search_in_directory(searched_file_path, search_path)

        if self.window.num_groups() > 1:
            self.window.focus_group(1 if searching_spec else 0)

        self.window.open_file(perfect_match)


def list_files(dirname):
    files = []
    for dirname, dirnames, filenames in os.walk(dirname):
        for filename in filenames:
            files.append(os.path.join(dirname, filename))
    return files


def search_in_directory(file_path, directory_path):
    if not os.access(directory_path, os.R_OK):
        return

    file_name = file_path.split('/')[-1]

    files = list_files(directory_path)
    matches = [common_start_len(f[::-1], file_path[::-1]) for f in files]

    if not matches:
        return

    perfect_match = files[matches.index(max(matches))]

    if perfect_match.endswith('/' + file_name):
        return perfect_match


def common_start_len(a, b):
    return len(list(takewhile(lambda (x, y): x == y, zip(a, b))))
