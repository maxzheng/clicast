import sys

from clicast.cast import Cast, CastReader


def check_message(url, allow_exit=False, raises=False, **show_kwargs):
  """
  Check remote url for new messages and display them.

  :param str url: Cast file URL to check
  :param bool allow_exit: Perform sys.exit(1) if cast requests it.
  :param bool raises: Raise exception for failed to download/parse cast file or such.
                      Recommended to set this to False for production / in non-debug mode.
  :param dict show_kwargs: kwargs to be passed to :meth:`CastReader.show_messages`
  """

  try:
    cast = Cast.from_url(url)
    reader = CastReader(cast)
    reader.show_messages(**show_kwargs)

    if allow_exit and cast.alert_exit:
      sys.exit(1)
  except Exception:
    if raises:
      raise
