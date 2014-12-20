import os

from clicast.cast import Cast, CastReader

class TestCast(object):
  def test_from_file(self):
    cast_file = os.path.join(os.path.dirname(__file__), 'test.cast')
    cast = Cast.from_file(cast_file)

    assert cast.alert == 'We found a big bad bug. Please try not to step on it!! Icky...
         No worries. It will be fixed soon! :)'
    assert cast.exit
    assert cast.message == None

  def test_from_url(self):
    pass



class TestCastReader(object):
  pass
