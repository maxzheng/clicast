from clicast.cast import Cast, CastReader


def check_message(url, allow_exit=False, silent=False):
  """
  Check remote url for new messages and display them.

  :param str url: Cast file URL to check
  :param bool allow_exit: Perform sys.exit(1) if cast requests it.
  :param bool silent: Don't raise exception for failed to download/parse cast file or such.
                      Recommended to set this to True for production / in non-debug mode.
  """

  try:
    reader = CastReader(Cast.from_url(url))
    reader.show_messages()
  except Exception as e:
    if not silent:
      raise
