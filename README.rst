clicast
=======

Broadcast messages for CLI tools, such as a warning for critical bug or notification about new features.

How to Use
----------

As easy as 1-2-3:

1. Install

   .. code::

     pip install clicast

2. Create your own cast file and make it accessible as an URL.
   I.e. https://raw.githubusercontent.com/maxzheng/clicast/master/test/example.cast

3. Import and call check_message

   .. code::

     from clicast import check_message

     def main():
        check_message('https://raw.githubusercontent.com/maxzheng/clicast/master/test/example.cast',
                      allow_exit=True,
                      header='=' * 80,
                      footer='=' * 80)

Try It Out
----------

Don't even want to write the bin script to try? I got you covered! :)

.. code::

  $ wget https://raw.githubusercontent.com/maxzheng/clicast/master/bin/cast-example
  $ chmod +x cast-example

If you run cast-example for the first time, you will see::

  $ ./cast-example
  ================================================================================
  We found a big bad bug. Please try not to step on it!! Icky...
  No worries. It will be fixed soon! :)

  New messages on top as messages are displayed in same order as you see here

  Version 0.1 has been released! Upgrade today to get cool features.

  Version 0.2 has been released! If you upgrade, you will get:
  1) Cool feature 1
  2) Cool feature 2
  So what are you waiting for? :)

  There is a small bug over there, so watch out!
  ================================================================================
  Hello World!

And run it again::

  $ cast-example
  ================================================================================
  We found a big bad bug. Please try not to step on it!! Icky...
  No worries. It will be fixed soon! :)
  ================================================================================
  Hello World!

That's it!

Contribute / Report Bugs
-------------------------
Github project: https://github.com/maxzheng/clicast

Report issues/bugs: https://github.com/maxzheng/clicast/issues
