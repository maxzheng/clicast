import re
import sys


REGEX_IN_MSG_RE = re.compile('^\[(.+)\] *(.+)$', flags=re.DOTALL)

def match_cli_args(msg, alert=False, cli_args=None):
  """
  Look for messages that starts with "[pattern] message" and search the pattern against
  the given args (or sys.argv).

  :param str msg: Message to search
  :param bool alert: Is alert message?
  :param str cli_args: Optional args used for testing instead of sys.argv
  :ret str: New message without [pattern] or None if pattern doesn't match CLI args
  """
  match = REGEX_IN_MSG_RE.match(msg)

  if match:
    regex = match.group(1)
    msg = match.group(2)
    args = cli_args or ' '.join(sys.argv)
    if not re.search(regex, args):
      return None

  return msg
