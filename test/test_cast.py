import os

import pytest

from clicast.cast import Cast, CastReader


def casts():
  cast_file = os.path.join(os.path.dirname(__file__), 'test.cast')
  return [Cast.from_file(cast_file),
          Cast.from_url('https://raw.githubusercontent.com/maxzheng/clicast/test/test.cast')]


class TestCast(object):
  @classmethod

  @pytest.mark.parametrize('cast_from_source', casts())
  def test_from(cast):
    assert cast.alert == 'We found a big bad bug. Please try not to step on it!! Icky...\nNo worries. It will be fixed soon! :)'
    assert cast.alert_exit
    assert [m.message for m in cast.messages] == [
           'Version 0.1 has been released! Upgrade today to get cool features.',
           'Version 0.2 has been released! If you upgrade, you will get:\n'
             '1) Cool feature 1\n'
             '2) Cool feature 2\n'
             'So what are you waiting for? :)',
           'There is a small bug over there, so watch out!']



class TestCastReader(object):
  pass
