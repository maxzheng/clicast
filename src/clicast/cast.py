from ConfigParser import ConfigParser
import os
from StringIO import StringIO
import tempfile

import requests


class CastError(Exception):
  pass


class Cast(object):
  """ Represents all cast options/messages. """

  ALERT_SECTION = 'Alert'
  MESSAGES_SECTION = 'Messages'
  REQUIRED_SECTIONS = (ALERT_SECTION, MESSAGES_SECTION)
  ALERT_MSG_KEY = 'message'
  ALERT_EXIT_KEY = 'exit'

  class CastMessage(object):
    """ Represents a single message in a cast. """
    def __init__(self, key, msg):
      """
      :param str key: Message key
      :param str msg: The actual message
      """
      self.key = key
      self.msg = msg

  def __init__(self, alert=None, alert_exit=False, messages=None):
    """
    :param str alert: Alert message
    :param bool alert_exit: Should exit indicator for alert
    :param list(tuple) messages: List of tuple of (key, message)
    """
    self.alert = alert
    self.alert_exit = alert_exit
    self.messages = messages and [CastMessage(*m) for m in messages] or []

  @classmethod
  def from_string(cls, cast):
    """ Create a :class:`Cast` from the given string. """
    cast_fp = StringIO(cast)
    parser = ConfigParser()
    parser.readfp(cast_fp)

    for section in cls.REQUIRED_SECTIONS:
      if section not in parser.sections():
        raise CastError('Missing "%s" section in cast file' % section)

    alert_msg = None
    alert_exit = None

    for key, value in parser.items(ALERT_SECTTION):
      if ALERT_MSG_KEY == key:
        alert_msg = value
      elif ALERT_EXIT_KEY == key:
        alert_exit = bool(value)
      else:
        raise CastError('Invalid key "%s" in %s section', key, ALERT_SECTION)

    messages = parser.items(MESSAGES_SECTION)

    return cls(alert_msg, alert_exit, messages)


  @classmethod
  def from_file(cls, cast_file):
    """ Create a :class:`Cast` from the given file. """
    with open(cast_file) as fp:
      return cls.from_string(fp.read())

  @classmethod
  def from_url(cls, cast_url):
    """ Create a :class:`Cast` from the given url. """
    response = requests.get(cast_url)
    response.raise_for_status()
    return cls.from_string(response.text)



class CastReader(object):
  """ Reads a :class:`Cast` and keep track of read messages """

  READ_MSG_FILE = os.path.join(tempfile.gettempdir(), 'clicast.read_messages')

  def __init__(self, cast):
    self.cast = cast

  def show_messages(self, logger=None, header=None, footer=None):
    """ Print new messages to stdout unless a logger is given. """
    msgs = self.new_messages()

    if msgs:
      if header:
        msgs.insert(0, header)
      if footer:
        msgs.append(footer)

      for msg in msgs:
        if logger:
          logger.info(msg)
        else:
          print msg

  def new_messages(self, mark_as_read=True):
    """
    :param bool mark_as_read: Mark new messages as read
    :ret list(str): List of new messages
    """
    read_keys = self._read_msg_keys()
    new_messages = [m for m in self.cast.messages if m.key not in read_keys]

    if new_messages and mark_as_read:
      self._mark_as_read(new_messages)

    return [m.message for m in new_messages]

  def _read_msg_keys(self):
    """ Set of read messages. """

    try:
      with open(READ_MSG_FILE) as fp:
        read_keys = fp.read()
        return set(read_keys.split())
    except Exception:
      return []

  def _mark_as_read(self, messages):
    """ Mark the given list of :class:`CastMessage` as read. """

    keys = self._read_msg_keys
    keys.update(messages)

    with open(READ_MSG_FILE, 'w') as fp:
      fp.write(' '.join(keys))
