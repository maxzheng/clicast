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
    def __init__(self, key, message):
      """
      :param str key: Message key
      :param str message: The actual message
      """
      self.key = key
      self.message = message

  def __init__(self, alert=None, alert_exit=False, messages=None):
    """
    :param str alert: Alert message
    :param bool alert_exit: Should exit indicator for alert
    :param list(tuple) messages: List of tuple of (key, message)
    """
    self.alert = alert
    self.alert_exit = alert_exit
    self.messages = messages and [self.CastMessage(*m) for m in messages] or []

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

    for key, value in parser.items(cls.ALERT_SECTION):
      if cls.ALERT_MSG_KEY == key:
        alert_msg = value
      elif cls.ALERT_EXIT_KEY == key:
        alert_exit = bool(value)
      else:
        raise CastError('Invalid key "%s" in %s section', key, cls.ALERT_SECTION)

    messages = parser.items(cls.MESSAGES_SECTION)

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
      if logger:
        if header:
          logger.info(header)
        for msg in msgs:
            logger.info(msg)
        if footer:
          logger.info(footer)

      else:
        if header:
          print header
        print '\n\n'.join(msgs)
        if footer:
          print footer

  def new_messages(self, mark_as_read=True):
    """
    :param bool mark_as_read: Mark new messages as read
    :ret list(str): List of new messages with alert being the first if any.
    """
    read_keys = self._read_msg_keys()
    new_messages = [m for m in self.cast.messages if m.key not in read_keys]

    if new_messages and mark_as_read:
      self._mark_as_read(new_messages)

    msgs = [m.message for m in new_messages]

    if self.cast.alert:
      msgs.insert(0, self.cast.alert)

    return msgs

  def _read_msg_keys(self):
    """ Set of read messages. """

    try:
      with open(self.READ_MSG_FILE) as fp:
        read_keys = fp.read()
        return set(read_keys.split())
    except Exception:
      return set()

  def _mark_as_read(self, messages):
    """ Mark the given list of :class:`CastMessage` as read. """

    keys = self._read_msg_keys()
    keys.update(m.key for m in messages)

    with open(self.READ_MSG_FILE, 'w') as fp:
      fp.write(' '.join(keys))
