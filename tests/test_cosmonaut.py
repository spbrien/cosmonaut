#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `cosmonaut` package."""


import unittest
from click.testing import CliRunner

from cosmonaut import cosmonaut
from cosmonaut import cli


class TestCosmonaut(unittest.TestCase):
    """Tests for `cosmonaut` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_help(self):
        """Test the CLI."""
        runner = CliRunner()
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert 'Deploys static assets to S3.' in help_result.output
        assert '--help' in help_result.output
