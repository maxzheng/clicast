import sys

from clicast.cast import Cast, CastReader


def check_message(url, cache_duration=None, allow_exit=False, raises=False, **show_kwargs):
  """
  Check remote url for new messages and display them.

  :param str url: Cast file URL to check
  :param int cache_duration: Cache messages locally for number of seconds to avoid checking the URL too often.
                             This is useful for response latency sensitive CLI to ensure user's experience
                             isn't compromised. Alternatively, you may want to check messages in a seperate thread.
  :param bool allow_exit: Perform sys.exit(1) if cast requests it.
  :param bool raises: Raise exception for failed to download/parse cast file or such.
                      Recommended to set this to False for production / in non-debug mode.
  :param dict show_kwargs: kwargs to be passed to :meth:`CastReader.show_messages`
  """

  try:
    cast = Cast.from_url(url, cache_duration)
    reader = CastReader(cast)
    reader.show_messages(**show_kwargs)

    if allow_exit and cast.alert_exit:
      sys.exit(1)
  except Exception:
    if raises:
      raise
