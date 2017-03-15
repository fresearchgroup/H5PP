from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from h5pp.h5p.h5pmodule import *
from h5pp.h5p.h5pclasses import H5PDjango
from h5pp.h5p.library.h5pclasses import *
from h5pp.h5p.editor.h5peditorclasses import H5PDjangoEditor
import django

# Create your tests here.

class H5pModuleTestCase(TestCase):

	def setUp(self):
		library = h5p_libraries.objects.create(
			library_id='1',
			machine_name='H5P.Test',
			title='Test',
			major_version=1,
			minor_version=1,
			patch_version=2,
			runnable=1,
			fullscreen=0,
			embed_types='',
			preloaded_js="[u'scripts/test.js']",
			preloaded_css="[u'styles/test.css']",
			drop_library_css=None,
			semantics='',
			restricted=0,
			tutorial_url=''
		)
		test = User.objects.create(
			username='titi'
		)
		print('setUp of ModuleTestCase ---- Ready')

	def test_exportpath(self):
		content = {
			'id': 1,
			'slug': 'interactive-video'
		}
		self.assertEqual('/home/pod/H5PP/media/exports/interactive-video-1.h5p', h5pGetExportPath(content))
		content = {
			'id': 2
		}
		self.assertEqual('/home/pod/H5PP/media/exports/2.h5p', h5pGetExportPath(content))
		print('test_exportpath ---- Check')

	def test_library_details_title(self):
		self.assertEqual({'title': 'Test'}, h5pLibraryDetailsTitle(1))
		self.assertEqual(None, h5pLibraryDetailsTitle(2))
		print('test_library_details_title ---- Check')

	def test_add_core_assets(self):
		assets = {
			'js': [
				"/static/h5p/js/jquery.js",
    			"/static/h5p/js/h5p.js",
			    "/static/h5p/js/h5p-event-dispatcher.js",
			    "/static/h5p/js/h5p-x-api-event.js",
			    "/static/h5p/js/h5p-x-api.js",
			    "/static/h5p/js/h5p-content-type.js",
			    "/static/h5p/js/h5p-confirmation-dialog.js",
			    "/static/h5p/js/h5p-action-bar.js"
			],
			'css': [
				"/static/h5p/styles/h5p.css",
			    "/static/h5p/styles/h5p-confirmation-dialog.css",
			    "/static/h5p/styles/h5p-core-button.css"
			]
		}
		self.assertEqual(assets, h5pAddCoreAssets())
		print('test_add_core_assets ---- Check')

	def test_get_core_settings(self):
		user = User.objects.get(username='titi')
		core = h5pGetCoreSettings(user)

		self.assertTrue(core['postUserStatistics'])
		self.assertTrue('user' in core)
		print('test_get_core_settings ---- Check')

	##
	# TODO
	# Place request-based test
	##

class H5PClassesTestCase(TestCase):

	def setUp(self):
		h5p_libraries.objects.create(
			library_id='1',
			machine_name='H5P.Test',
			title='Test',
			major_version=1,
			minor_version=1,
			patch_version=2,
			runnable=1,
			fullscreen=0,
			embed_types='',
			preloaded_js="[u'scripts/test.js']",
			preloaded_css="[u'styles/test.css']",
			drop_library_css=None,
			semantics='',
			restricted=0,
			tutorial_url=''
		)
		test = User.objects.create(
			username='titi'
		)
		print('setUp of ClassesTestCase ---- Ready')

	def test_get_instance(self):
		user = User.objects.get(username='titi')
		interface = H5PDjango(user)

		self.assertTrue(isinstance(interface.h5pGetInstance('validator'), H5PValidator))
		self.assertTrue(isinstance(interface.h5pGetInstance('storage'), H5PStorage))
		self.assertTrue(isinstance(interface.h5pGetInstance('contentvalidator'), H5PContentValidator))
		self.assertTrue(isinstance(interface.h5pGetInstance('export'), H5PExport))
		self.assertTrue(isinstance(interface.h5pGetInstance('interface'), H5PDjango))
		self.assertTrue(isinstance(interface.h5pGetInstance('core'), H5PCore))
		self.assertTrue(isinstance(interface.h5pGetInstance('editor'), H5PDjangoEditor))
		print('test_get_instance ---- Check')

	def test_get_platform_info(self):
		user = User.objects.get(username='titi')
		interface = H5PDjango(user)
		info = {
			'name': 'django',
			'version': django.get_version(),
			'h5pVersion': '7.x'
		}
		self.assertEqual(info, interface.getPlatformInfo())
		print('test_get_platform_info --- Check')

	def test_load_libraries(self):
		user = User.objects.get(username='titi')
		interface = H5PDjango(user)

		self.assertTrue(len(interface.loadLibraries()) > 0)
		self.assertTrue('H5P.Test' in interface.loadLibraries())

		h5p_libraries.objects.filter(library_id='1').delete()

		self.assertFalse(len(interface.loadLibraries()) > 0)
		self.assertEqual('', interface.loadLibraries())
		print('test_load_libraries ---- Check')

	def test_get_library_id(self):
		user = User.objects.get(username='titi')
		interface = H5PDjango(user)

		self.assertEqual(1, interface.getLibraryId('H5P.Test'))
		self.assertEqual(1, interface.getLibraryId('H5P.Test', 1, 1))

		h5p_libraries.objects.filter(library_id='1').delete()

		self.assertTrue(interface.getLibraryId('H5P.Test') == None)
		print('test_get_library_id ---- Check')

	def test_is_patched_library(self):
		user = User.objects.get(username='titi')
		interface = H5PDjango(user)
		library = {
			'machineName': 'H5P.Test',
			'majorVersion': 1,
			'minorVersion': 1,
			'patchVersion': 2 
		}
		self.assertFalse(interface.isPatchedLibrary(library))
		h5p_libraries.objects.create(
			library_id='2',
			machine_name='H5P.Test',
			title='Test',
			major_version=1,
			minor_version=1,
			patch_version=1,
			runnable=1,
			fullscreen=0,
			embed_types='',
			preloaded_js="[u'scripts/test.js']",
			preloaded_css="[u'styles/test.css']",
			drop_library_css=None,
			semantics='',
			restricted=0,
			tutorial_url=''
		)
		self.assertTrue(interface.isPatchedLibrary(library))
		print('test_is_patched_library ---- Check')

	def test_save_library_data(self):
		user = User.objects.get(username='titi')
		interface = H5PDjango(user)
		libraryData = {
			'title': 'Test2',
			'majorVersion': 1,
			'minorVersion': 1,
			'patchVersion': 2,
			'runnable': 1,
			'machineName': 'H5P.Test2',
			'author': 'drclockwork',
			'license': 'MIT',
			'coreApi': {
				'majorVersion': 1,
				'minorVersion': 6
			},
			'preloadedJs': [
				{
				'path': 'js/test.js'
				}
			],
			'preloadedCss': [
				{
				'path': 'css/test.css'
				}
			],

		}
		interface.saveLibraryData(libraryData)
		result = h5p_libraries.objects.filter(library_id=2).values()
		
		self.assertTrue(result[0]['machine_name'] == 'H5P.Test2')

		libraryData['title'] = 'Test3'
		libraryData['libraryId'] = 2
		interface.saveLibraryData(libraryData, False)
		result = h5p_libraries.objects.filter(library_id=2).values()

		self.assertTrue(result[0]['title'] == 'Test3')
		print('test_save_library_data ---- Check')

		##
		# TODO
		# Place libraries dependencies test
		##