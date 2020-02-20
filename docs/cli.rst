ebustool
========

Command Line Tool::

    usage: ebustool [-h] [--version] {cmd,listen,ls,observe,read,write} ...

    positional arguments:
      {cmd,listen,ls,observe,read,write}
                            Sub Commands
        cmd                 Issue TCP Command on EBUSD. See
                            https://github.com/john30/ebusd/wiki/3.1.-TCP-client-
                            commands for reference.
        listen              Listen on the bus, decode messages and and print
        ls                  List all messages
        observe             Read all known messages once and continue listening so
                            that ALL EBUS values are available, decode every
                            message and print.
        read                Read values from the bus, decode and print
        write               Write value to the bus

    optional arguments:
      -h, --help            show this help message and exit
      --version             show program's version number and exit
