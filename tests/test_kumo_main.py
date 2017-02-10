# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import pytest
import regex

from gcdt.kumo_main import version_cmd, list_cmd, preview_cmd

from .helpers_aws import check_preconditions, get_tooldata
from .helpers_aws import awsclient  # fixtures!
from .test_kumo_aws import simple_cloudformation_stack  # fixtures!
from .test_kumo_aws import simple_cloudformation_stack_folder  # fixtures!
from .helpers import temp_folder  # fixtures!
from . import here


# note: xzy_main tests have a more "integrative" character so focus is to make
# sure that the gcdt parts fit together not functional coverage of the parts.


def test_version_cmd(capsys):
    version_cmd()
    out, err = capsys.readouterr()
    assert out.startswith('gcdt version')


@pytest.mark.aws
@check_preconditions
def test_list_cmd(awsclient, capsys):
    tooldata = get_tooldata(
        awsclient, 'kumo', 'list',
        config_base_name='settings_large',
        location=here('./resources/simple_cloudformation_stack/'))
    list_cmd(**tooldata)
    out, err = capsys.readouterr()
    # using regular expression search in captured output
    assert regex.search('listed \d+ stacks', out) is not None


@pytest.mark.aws
@check_preconditions
def test_preview_cmd(awsclient, simple_cloudformation_stack,
                     simple_cloudformation_stack_folder, capsys):
    tooldata = get_tooldata(
        awsclient, 'kumo', 'preview',
        config_base_name='settings_large',
        location=here('./resources/simple_cloudformation_stack/'))
    preview_cmd(**tooldata)
    out, err = capsys.readouterr()
    # verify diff results
    assert 'InstanceType │ t2.micro      │ t2.medium ' in out
