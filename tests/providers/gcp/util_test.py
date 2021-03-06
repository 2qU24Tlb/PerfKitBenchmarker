# Copyright 2015 PerfKitBenchmarker Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for perfkitbenchmarker.providers.gcp.util."""


import unittest
import mock

from perfkitbenchmarker import resource
from perfkitbenchmarker.providers.gcp import util
import six


_GCLOUD_PATH = 'path/gcloud'


class GceResource(resource.BaseResource):

  def __init__(self, **kwargs):
    for k, v in six.iteritems(kwargs):
      setattr(self, k, v)

  def _Create(self):
    raise NotImplementedError()

  def _Delete(self):
    raise NotImplementedError()


class GcloudCommandTestCase(unittest.TestCase):

  def setUp(self):
    super(GcloudCommandTestCase, self).setUp()
    p = mock.patch(util.__name__ + '.FLAGS')
    self.mock_flags = p.start()
    self.addCleanup(p.stop)
    self.mock_flags.gcloud_path = _GCLOUD_PATH

  def testCommonFlagsWithoutOptionalFlags(self):
    gce_resource = GceResource(project=None)
    cmd = util.GcloudCommand(gce_resource, 'compute', 'images', 'list')
    self.assertEqual(cmd.GetCommand(), [
        'path/gcloud', 'compute', 'images', 'list', '--format', 'json',
        '--quiet'
    ])

  def testCommonFlagsWithOptionalFlags(self):
    gce_resource = GceResource(project='test-project', zone='test-zone')
    cmd = util.GcloudCommand(gce_resource, 'compute', 'images', 'list')
    self.assertEqual(cmd.GetCommand(), [
        'path/gcloud', 'compute', 'images', 'list', '--format', 'json',
        '--project', 'test-project', '--quiet', '--zone', 'test-zone'
    ])

  def testListValue(self):
    gce_resource = GceResource(project=None)
    cmd = util.GcloudCommand(gce_resource, 'compute', 'instances', 'create')
    cmd.flags['local-ssd'] = ['interface=nvme', 'interface=SCSI']
    self.assertEqual(cmd.GetCommand(), [
        'path/gcloud',
        'compute',
        'instances',
        'create',
        '--format',
        'json',
        '--local-ssd',
        'interface=nvme',
        '--local-ssd',
        'interface=SCSI',
        '--quiet',
    ])

  def testIssue(self):
    gce_resource = GceResource(project=None)
    cmd = util.GcloudCommand(gce_resource, 'compute', 'images', 'list')
    mock_issue_return_value = ('issue-return-value', 'stderr', 0)
    p = mock.patch(util.__name__ + '.vm_util.IssueCommand',
                   return_value=mock_issue_return_value)
    with p as mock_issue:
      return_value = cmd.Issue()
      mock_issue.assert_called_with(['path/gcloud', 'compute', 'images', 'list',
                                     '--format', 'json', '--quiet'])
    self.assertEqual(return_value, mock_issue_return_value)

  def testIssueWarningSuppressed(self):
    gce_resource = GceResource(project=None)
    cmd = util.GcloudCommand(gce_resource, 'compute', 'images', 'list')
    mock_issue_return_value = ('issue-return-value', 'stderr', 0)
    p = mock.patch(util.__name__ + '.vm_util.IssueCommand',
                   return_value=mock_issue_return_value)
    with p as mock_issue:
      return_value = cmd.Issue(suppress_warning=True)
      mock_issue.assert_called_with(
          ['path/gcloud', 'compute', 'images', 'list', '--format', 'json',
           '--quiet'],
          suppress_warning=True)
    self.assertEqual(return_value, mock_issue_return_value)

  def testIssueRetryable(self):
    gce_resource = GceResource(project=None)
    cmd = util.GcloudCommand(gce_resource, 'compute', 'images', 'list')
    mock_issue_return_value = ('issue-return-value', 'stderr', 0)
    p = mock.patch(util.__name__ + '.vm_util.IssueRetryableCommand',
                   return_value=mock_issue_return_value)
    with p as mock_issue:
      return_value = cmd.IssueRetryable()
      mock_issue.assert_called_with(['path/gcloud', 'compute', 'images', 'list',
                                     '--format', 'json', '--quiet'])
    self.assertEqual(return_value, mock_issue_return_value)

  def testGetRegionFromZone(self):
    zone = 'us-central1-xyz'
    self.assertEqual(util.GetRegionFromZone(zone), 'us-central1')

if __name__ == '__main__':
  unittest.main()
