"""
Test custom Django management commands
"""

# Mock behavior of database
from unittest.mock import patch

# possible before db ready error
from psycopg2 import OperationalError as Psycopg2Error

# simulate calling command on db
from django.core.management import call_command

# another potential error on any stage of db ready process 
from django.db.utils import OperationalError
from django.test import SimpleTestCase

@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
	"""Test commands"""

	def test_wait_for_db_ready(self,patched_check):
		"""Test waiting for database if database ready."""

		patched_check.return_value = True

		call_command('wait_for_db')

		patched_check.assert_called_once_with(databases=['default'])

	@patch('time.sleep')
	def test_wait_for_db_ready(self,patch_sleep,patched_check):
		"""Test waiting for database when getting OperationError."""
		patched_check.side_effect = [Psycopg2Error] * 2 + [OperationalError] * 3 + [True]

		call_command('wait_for_db')

		self.assertEqual(patched_check.call_count,6)
		patched_check.assert_called_with(databases=['default'])
		