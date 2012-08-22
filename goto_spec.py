import os
import sublime, sublime_plugin

class GotoSpecCommand(sublime_plugin.WindowCommand):
	def run(self):
		path = self.window.active_view().file_name()
		file_name = path.split('/')[-1]
		rspec_filename = file_name.replace(".rb", "_spec.rb")
		
		#self.window.open_file(rspec_filename)
		if not self.window.folders():
			return

		project_root = self.window.folders()[0]
		spec_folder = "%s/spec" % project_root
		
		if not os.access(spec_folder, os.R_OK):
			return

		files = list_files(spec_folder)
		files = [f for f in files if f.endswith('/' + rspec_filename)]
		if not files:
			return
		spec_file = files[0]

		if self.window.num_groups() > 1:
			self.window.focus_group(1)
		self.window.open_file(spec_file)
		# sublime.message_dialog(str(files))


def list_files(dirname):
	files = []
	for dirname, dirnames, filenames in os.walk(dirname):
		for filename in filenames:
			files.append(os.path.join(dirname, filename))
	return files
