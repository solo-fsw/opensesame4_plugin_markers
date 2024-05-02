#-*- coding:utf-8 -*-

"""
OpenSesame 4 extension for creating a tab with the marker tables after the experiment is finished.
Part of the markers_os4 plugin.
"""

import time
from libopensesame.py3compat import *
from libopensesame.exceptions import UserAborted 
from libqtopensesame.extensions import BaseExtension
from libopensesame import misc
from libopensesame.plugins import list_plugins, set_plugin_property, plugin_properties
from libopensesame.metadata import major_version
from libqtopensesame.misc.config import cfg
import sys


class MarkersOs4Extension(BaseExtension):

	"""
	desc:
		- Checks OpenSesame version on startup
		- Shows marker tables in separate tab after an experiment has finished.
	"""

	def event_startup(self):

		"""
		desc:
			Handles startup of OpenSesame: disables outdated plugins
		"""		

		md = u'Time: ' + str(time.ctime()) + u'\n\n'

		try:	

			if major_version[0] == '4':

				list_old_plugins = ["markers_os3_extension", "markers_os3_init", "markers_os3_send", "markers_extension", "markers_init", "markers_send"]
				plugins_available = []

				'Get list of plugins and extensions'
				plugin_list = list_plugins(filter_disabled=False)
				extension_list = list_plugins(filter_disabled=False, _type=u'extensions')

				'loop through lists and check whether old plugins are installed'
				for plugin_name in plugin_list:
					if plugin_name in list_old_plugins:
						plugins_available.append(plugin_name)

				for extension_name in extension_list:
					if extension_name in list_old_plugins:
						plugins_available.append(extension_name)

				if plugins_available:
					self.extension_manager.fire(u'notify',
						message=_(u'One or more outdated marker plugins were found. Please check the markers version tab for more info.'),
						category=u'warning')
					
					md += 'The following outdated plugins/extensions were found: \n\n'
					for plugin in plugins_available:
						md += '- ' + str(plugin) + '\n\n'

			else:

				self.extension_manager.fire(u'notify',
                    message=_(u'The markers_os4 plugin can only run in OpenSesame 4. Check your version and check the markers version tab for more info.'),
                    category=u'warning')
			
		except:
			md += f'\n\nError: {sys.exc_info()[1]}'

		self.tabwidget.open_markdown(md, title=_(u'debugging'),
									icon=u'document-new')			

	def event_end_experiment(self, ret_val):

		"""
		desc:
			Handles the end of an experiment.

		arguments:
			ret_val:
				desc:	An Exception, or None if no exception occurred.
				type:	[Exception, NoneType]
		"""

		self.print_markers(ret_val)

	def print_markers(self, e):

		"""
		desc:
			Prints marker tables in md file that is shown in tab after the experiment.
		"""

		var = self.extension_manager.provide(
			'jupyter_workspace_variable',
			name='var'
		)
		
		if hasattr(var, 'marker_device_used'):

			try:

				marker_tags = self.extension_manager.provide(
					'jupyter_workspace_variable',
					name='markers_tags'
				)

				# Init markdown
				md = u'Time: ' + str(time.ctime()) + u'\n\n'

				if e is None:
					md += u'The experiment finished succesfully.\n\n'
				elif isinstance(e, UserAborted):
					md += u'**The experiment was aborted.**\n\n The marker tables show the markers that were sent until the experiment was aborted.\n\n'
				else:
					md += u'**An error occured:**\n\n' + str(e) + '\n\n Could not show marker tables.\n\n'
					self.tabwidget.open_markdown(md, u'os-finished-error', u'Marker tables')
					return

				for tag in marker_tags:

					# Add tag
					md += u'#' + str(tag) + u'\n'

					# Add marker device properties
					cur_marker_props = self.extension_manager.provide(
						'jupyter_workspace_variable',
						name=f"markers_prop_{tag}"
					)	

					for marker_prop in cur_marker_props:
						md += u'- ' + str(marker_prop) + u': ' + str(cur_marker_props[marker_prop]) + u'\n'

					# Get marker tables
					summary_df = self.extension_manager.provide(
						'jupyter_workspace_variable',
						name=f"markers_summary_table_{tag}"
					)

					marker_df = self.extension_manager.provide(
						'jupyter_workspace_variable',
						name=f"markers_marker_table_{tag}"
					)

					error_df = self.extension_manager.provide(
						'jupyter_workspace_variable',
						name=f"markers_error_table_{tag}"
					)	

					# Add summary table
					summary_df = summary_df.round(decimals=3)
					md = add_table_to_md(md, summary_df, 'Summary table')

					if summary_df.empty:
						md += u'No markers were sent, summary table empty\n\n'

					# Add marker table
					marker_df = marker_df.round(decimals=3)
					md = add_table_to_md(md, marker_df, 'Marker table')

					if marker_df.empty:
						md += u'No markers were sent, marker table empty\n\n'

					# Add error table
					md = add_table_to_md(md, error_df, 'Error table')

					if error_df.empty:
						md += u'No marker errors occurred, error table empty\n\n'

				# Show markers
				if e is None:
					self.tabwidget.open_markdown(md, u'os-finished-success', u'Marker tables')
				else:
					self.tabwidget.open_markdown(md, u'os-finished-error', u'Marker tables')


			# Occasionally, something goes wrong getting the marker tables
			except:

				md += f'\n\nError: {sys.exc_info()[1]}'
				md += u'\n\nSomething went wrong while generating the marker tables. This can happen when the experiment crashed.'
				self.tabwidget.open_markdown(md, u'os-finished-error', u'Marker tables')	
			

def add_table_to_md(md, df, table_title):

	# Table title
	md += u'##' + table_title + u':##' + u'\n'

	ncols = len(df.columns)

	# Column headers
	md += u'| '
	for column in df:

		if "_s" in column:
			column = column.replace("_s", " (s)")
		if "_ms" in column:
			column = column.replace("_ms", " (ms)")
		if "_" in column:
			column = column.replace("_", " ")
		column = column.capitalize()

		md += column + u' | '
	md += u'\n'

	# Header separator
	md += u'|'
	for col in range(ncols):
		md += u':---|'
	md += u'\n'

	# Values
	md += u'| '
	for index, row in df.iterrows():
		for column in df:
			cur_value = row[column]
			if isinstance(cur_value, float):
				cur_value = round(cur_value, 3)
			md += str(cur_value) + u' | '
		md += u'\n'

	md += u'\n\n'

	return md
