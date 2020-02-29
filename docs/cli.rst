========
ebustool
========

*ebustool* is a command line interface to the ebus library which can be used to examine the library capabilities and play around ebusd on a real system allowing user to monitor and change the settings of their equipment::

    usage: ebustool [-h] [--host HOST] [--port PORT] [--timeout TIMEOUT]
                    [--version] [--debug]
                    {cmd,listen,ls,observe,read,state,write} ...

    positional arguments:
      {cmd,listen,ls,observe,read,state,write}
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
        state               Show EBUSD state
        write               Write value to the bus

    optional arguments:
      -h, --help            show this help message and exit
      --host HOST, -H HOST  EBUSD address. Default is '127.0.0.1'.
      --port PORT, -P PORT  EBUSD port. Default is 8888.
      --timeout TIMEOUT, -T TIMEOUT
                            EBUSD connection timeout. Default is 10.
      --version             show program's version number and exit
      --debug

Every command has a number of the same optional parameters which allow configuring *ebustool* with respect to the actual environment::

      --host HOST, -H HOST  EBUSD address. Default is '127.0.0.1'.
      --port PORT, -P PORT  EBUSD port. Default is 8888.
      --timeout TIMEOUT, -T TIMEOUT
                            EBUSD connection timeout. Default is 10.

Every command has its specific help available which one can see with *-h, --help* command line argument::

      -h, --help            show this help message and exit

*N.B. The above optional parameters will be omitted in the description below and only command specific optional parameters will be described.*

Messages and ebustool's path definition
=======================================

Many *ebustool* commands and their results are tightly coupled with circuits, messages and fields used by ebusd and these are reflected as paths in *ebustool*.
In the below example there are some messages and their values as represented by *ebustool*::

        broadcast/vdatetime/time                 ---u 22:53
        broadcast/vdatetime/date                 ---u 2020-02-29
        bai/ReturnTemp/temp                      r1-- 23.62°C [CH return temperature sensor]
        bai/ReturnTemp/tempmirror                r1-- 65157
        bai/ReturnTemp/sensor                    r1-- ok

Message format
--------------

The format of the message is a pattern that consists of the following::

    <circuit><.circuit index>/<message>/<field>

where::

    <circuit>           name of the ebusd's circuit
    <.circuit index>    if multiple circuits of the same kind exist then the second one and the
                        consequent ones will be suffixed with their index starting from zero,
                        e.g. the second unit will have ".1" index as its suffix
    <message>           ebusd message
    <field>             if ebusd message has fields those are represented as part of the path,
                        so any field can be addressed

In the example above, bai/ReturnTemp: *bai* is the circuit name (given without any index as this is the only one or the very first circuit of this kind),
*ReturnTemp* is the message and *temp*, *tempmirror* and *sensor* are the fields.

For more details please see `message definition <https://github.com/john30/ebusd/wiki/4.1.-Message-definition>`_ section of the ebusd documentation.

Message types
-------------

Every message has number of attributes which specify its type, e.g. if the message is for read, write or is an update value and if it has polling priority set.
For more details please see the corresponding section of the `ebusd documentation <https://github.com/john30/ebusd/wiki/4.1.-Message-definition#message-definition>`_
For example::

        broadcast/vdatetime/time                 ---u 22:53
        bai/ReturnTemp/temp                      r1-- 23.62°C [CH return temperature sensor]

Message types are defined as <rPwu>, where::

    <r>                 read message
    <P>                 read message polling priority
    <w>                 write message
    <u>                 update message

.. _message_pattern:

Message patterns 
----------------

Some of the *ebustool* commands support message patterns to specify one or more messages to be filtered by that command.
For example, to list all messages from all circuits which have *temp* (temperature) as their field::

        $ ebustool ls -H 192.168.10.1 "*/*/temp*"
        [snip]
        bai/StorageTemp/temp                     r1-- IntType(-2047.9, 2047.9, divider=16)
        bai/StorageTempDesired/temp              r1-- IntType(-2047.9, 2047.9, divider=16)
        bai/StorageTempMax/temp                  r1-- IntType(-2047.9, 2047.9, divider=16)
        bai/TempDiffBlock/temp0                  r1-- IntType(0, 254)
        [snip]

The wildcards supported are::

    '*' matches any character
    '?' matches one character

If multiple filters are required then those need to be separated with a semicolon::

        $ ebustool ls -H 192.168.10.1 "bai/R*/temp*;b7v/z1*Temp*/temp?"
        Loading Message Definitions ... 408 messages (391 read, 12 update, 229 write) with 801 fields DONE.
        Listing 10 messages (10 read, 0 update, 6 write) with 11 fields
        bai/ReturnTemp/temp                      r1-- IntType(-2047.9, 2047.9, divider=16)
        bai/ReturnTemp/tempmirror                r1-- IntType(0, 65534)
        bai/ReturnTempExternal/temp              r1-- IntType(-2047.9, 2047.9, divider=16)
        bai/ReturnTempMax/temp                   r1-- IntType(-2047.9, 2047.9, divider=16)
        b7v/z1ActualRoomTempDesired/tempv        r2w- FloatType()
        b7v/z1CoolingTemp/tempv                  r-w- FloatType()
        b7v/z1DayTemp/tempv                      r2w- FloatType()
        b7v/z1HolidayTemp/tempv                  r-w- FloatType()
        b7v/z1NightTemp/tempv                    r2w- FloatType()
        b7v/z1QuickVetoTemp/tempv                r-w- FloatType()
        b7v/z1RoomTemp/tempv                     r1-- FloatType()

.. _polling_ttl:

Polling priority, time to live (TTL) and wait for scan to complete
==================================================================

Read operation and its derivatives provide a possibility for better controlling how the messages are retrieved from the e-bus: polling priority and time to live.
These are described in detail in ebusd `read command <https://github.com/john30/ebusd/wiki/3.1.-TCP-client-commands#read>`_ description.

Polling priority is used to tell ebusd to periodically query the e-bus and read messages which have polling priority set.
This can be controlled with *--prio* argument of *ebustool* for the commands which support it.

In order not to overload e-bus with frequent reads ebusd may cache values and in that case it may return a cached value if its age is less than some predefined number of seconds (300 by default).
*--ttl* argument can be used to specify the exact agening to be used during the read operation.

At the very start ebusd scans the e-bus for available equipment. Until that scanning is done not all or none of the messages are known to ebusd.
It is sometimes handy to let ebusd complete the scanning and wait until it is done.
For that, *--scanwait* argument can be provided for the commands which rely on message availability.

cmd
===

**cmd** command allows issuing a request to the ebusd just like using ebusd's native ebusctl tool or using a telnet connection to the daemon::

    usage: ebustool cmd [-h] [--host HOST] [--port PORT] [--timeout TIMEOUT]
                        [--infinite]
                        cmd

    positional arguments:
      cmd                   TCP Command. See
                            https://github.com/john30/ebusd/wiki/3.1.-TCP-client-
                            commands for reference.

    optional arguments:
      --infinite, -i        Do not abort command processing on empty line.


For more information on the exact commands and their arguments please read `ebusd documentation <https://github.com/john30/ebusd/wiki/3.1.-TCP-client-commands>`_
Please note, that in order to pass arguments the command itself and its arguments must be surrounded with quotes.
For example, to read heater's return temperature use::

        $ ebustool cmd -H 192.168.10.1 'read -c bai ReturnTemp'

        24.38;65145;ok

*--infinite, -i* command line argument could be useful for the ebusd commands which once started may deliver their results asynchronously. For example, ebusd's *listen* command will output its results as parameters change or new messages are observed on e-bus::

        $ ebustool cmd -H 192.168.10.1 -i listen
        listen started

        broadcast vdatetime = 22:46:16;29.02.2020

.. _listen_command:

listen
======

**listen** command is a monitoring tool which reads and decodes all the message definitions known to ebusd for the current session, e.g. those which are in use by ebusd after performing equipment scanning::

    usage: ebustool listen [-h] [--host HOST] [--port PORT] [--timeout TIMEOUT]
                       [--scanwait]
                       [patterns]

    positional arguments:
      patterns              Message patterns separated by ';' (i.e.
                            'ui/OutsideTemp'). Default is '*/*' for all.

    optional arguments:
      --scanwait, -w        EBUSD scans the bus for available devices. Wait until
                            this scan does not find any new messages. Specify this
                            option, if EBUSD was started within the last minutes.

Example output::

        $ ebustool listen -H 192.168.10.1
        Loading Message Definitions ... 408 messages (391 read, 12 update, 229 write) with 801 fields DONE.
        Listening to 405 messages (391 read, 11 update, 227 write) with 801 fields
        broadcast/vdatetime/time                 ---u 22:53
        broadcast/vdatetime/date                 ---u 2020-02-29
        bai/ReturnTemp/temp                      r1-- 23.62°C [CH return temperature sensor]
        bai/ReturnTemp/tempmirror                r1-- 65157
        bai/ReturnTemp/sensor                    r1-- ok

In the snippet above we can see that currently ebusd knows 408 messages of which 391 read, 12 update and 229 write. The number of messages and their descriptions are subject to their availability in ebusd configuration files and scanned equipment. More specifically, *ebustool* issues *find* command to ebusd in order to get all known messages
(`find command <https://github.com/john30/ebusd/wiki/3.1.-TCP-client-commands#find>`_)

*listen* command supports `message patterns <message_pattern_>`_, so it is possible to specify which exact messages or groups of messages to listen to.

ls
==

**ls** command is used to list all known messages and their types as seen by *ebustool*::

    usage: ebustool ls [-h] [--host HOST] [--port PORT] [--timeout TIMEOUT]
                       [--scanwait] [--name-only] [--type TYPE]
                       [patterns]

    positional arguments:
      patterns              Message patterns separated by ';' (i.e.
                            'ui/OutsideTemp'). Default is '*/*' for all.

    optional arguments:
      --scanwait, -w        EBUSD scans the bus for available devices. Wait until
                            this scan does not find any new messages. Specify this
                            option, if EBUSD was started within the last minutes.
      --name-only, -n       Just print names.
      --type TYPE, -t TYPE  Type to be checked, 'r' for readable, 'w' for
                            writable.

Example output::

        $ ebustool -H 192.168.10.1 ls
        Loading Message Definitions ... 408 messages (391 read, 12 update, 229 write) with 801 fields DONE.
        Listing 405 messages (391 read, 11 update, 227 write) with 801 fields
        b7v/AdaptHeatCurve/yesno                 r-w- EnumType(('no', 'yes'))
        b7v/BankHolidayEndPeriod/hto             r-w- DateType()
        b7v/BankHolidayStartPeriod/hfrom         r-w- DateType()
        b7v/ContinuosHeating/tempv               r-w- FloatType()
        b7v/CylinderChargeHyst/calibrationv      r-w- FloatType()
        b7v/CylinderChargeOffset/calibrationv    r-w- FloatType()
        b7v/Date/date                            r-w- DateType()

        $ ebustool -H 192.168.10.1 ls --name-only
        Loading Message Definitions ... 408 messages (391 read, 12 update, 229 write) with 801 fields DONE.
        Listing 405 messages (391 read, 11 update, 227 write) with 801 fields
        b7v/AdaptHeatCurve/yesno
        b7v/BankHolidayEndPeriod/hto
        b7v/BankHolidayStartPeriod/hfrom
        b7v/ContinuosHeating/tempv
        b7v/CylinderChargeHyst/calibrationv
        b7v/CylinderChargeOffset/calibrationv
        b7v/Date/date
        b7v/DisplayedOutsideTemp/tempv
        b7v/FrostOverRideTime/hoursum2


**TODO: ADD TYPE DESCRIPTION**

*ls* command supports `message patterns <message_pattern_>`_, so it is possible to specify which exact messages or groups of messages to list.

observe
=======

**observe** command is used to read all the fields as done by the `read command <read_command_>`_ and then switch to listening mode as
done by the `listen command <listen_command_>`_ with *--infinite* argument::

    usage: ebustool observe [-h] [--host HOST] [--port PORT] [--timeout TIMEOUT]
                            [--scanwait] [--prio] [--ttl TTL]
                            [patterns]

    positional arguments:
      patterns              Message patterns separated by ';' (i.e.
                            'ui/OutsideTemp'). Default is '*/*' for all.

    optional arguments:
      --scanwait, -w        EBUSD scans the bus for available devices. Wait until
                            this scan does not find any new messages. Specify this
                            option, if EBUSD was started within the last minutes.
      --prio, -p            Set poll priority
      --ttl TTL, -t TTL     Maximum age of value in seconds

Please see `polling priority and TTL <polling_ttl_>`_ description for *--prio* and *--ttl* arguments.

*observe* command supports `message patterns <message_pattern_>`_, so it is possible to specify which exact messages or groups of messages need to be observed.

.. _read_command:

read
====

**read** command is used to read ebusd messages::

    usage: ebustool read [-h] [--host HOST] [--port PORT] [--timeout TIMEOUT]
                         [--scanwait] [--prio] [--ttl TTL]
                         [patterns]

    positional arguments:
      patterns              Message patterns separated by ';' (i.e.
                            'ui/OutsideTemp'). Default is '*/*' for all.

    optional arguments:
      --scanwait, -w        EBUSD scans the bus for available devices. Wait until
                            this scan does not find any new messages. Specify this
                            option, if EBUSD was started within the last minutes.
      --prio, -p            Set poll priority
      --ttl TTL, -t TTL     Maximum age of value in seconds

Please see `polling priority and TTL <polling_ttl_>`_ description for *--prio* and *--ttl* arguments.

Example output::

        $ ebustool -H 192.168.10.1 read 'b*/Return*/temp*;b7v/Hc1*Temp*/*'
        Loading Message Definitions ... 408 messages (391 read, 12 update, 229 write) with 801 fields DONE.
        Reading to 10 messages (10 read, 0 update, 5 write) with 11 fields
        bai/ReturnTemp/temp                      r1-- 23.62°C
        bai/ReturnTemp/tempmirror                r1-- 65157
        bai/ReturnTempExternal/temp              r1-- -1.81°C
        bai/ReturnTempMax/temp                   r1-- 82.94°C
        b7v/Hc1ActualFlowTempDesired/tempv       r1-- 0.0°C
        b7v/Hc1ExcessTemp/calibrationv           r-w- 0.0K
        b7v/Hc1FlowTemp/tempv                    r--- 23.0°C
        b7v/Hc1MaxFlowTempDesired/tempv          r-w- 45.0°C
        b7v/Hc1MinFlowTempDesired/tempv          r-w- 15.0°C
        b7v/Hc1RoomTempSwitchOn/rcmode           r2w- thermostat
        b7v/Hc1SummerTempLimit/tempv             r-w- 21.0°C

state
=====

**state** command is used to get current connection state, e.g. if *ebustool* is connected to ebusd or if ebusd has acquired signal and so on::

    usage: ebustool state [-h] [--host HOST] [--port PORT] [--timeout TIMEOUT]

Example output::

        $ ebustool -H 192.168.10.1 state
        ok

        $ ebustool -H 192.168.10.1 state
        ERROR: OSError(101, 'Network is unreachable')

        $ ebustool state
        ERROR: ConnectionRefusedError(111, "Connect call failed ('127.0.0.1', 8888)")

For more details please see ebusd `state command <https://github.com/john30/ebusd/wiki/3.1.-TCP-client-commands#state>`_
This can, for example, be used to determine if ebustool's listen command, ran with *--infinite* argument, needs to be restarted because of the dropped connection.

write
=====

**write** command is used to update a writable field::

    usage: ebustool write [-h] [--host HOST] [--port PORT] [--timeout TIMEOUT]
                          [--scanwait]
                          field value

    positional arguments:
      field                 Field (i.e. 'ui/OutsideTemp/temp')
      value                 Value to apply (i.e. '5'). 'NONE' is reserved for no
                            value.

    optional arguments:
      --scanwait, -w        EBUSD scans the bus for available devices. Wait until
                            this scan does not find any new messages. Specify this
                            option, if EBUSD was started within the last minutes.

Example::

        $ ebustool -H 192.168.10.1 write 'b7v/Hc1SummerTempLimit/tempv' 20.0
        Loading Message Definitions ... 408 messages (391 read, 12 update, 229 write) with 801 fields DONE.
        ERROR: UnboundLocalError("local variable 'values' referenced before assignment")


**TODO: ADD WRITE EXAMPLE**

For more details please see ebusd `write command <https://github.com/john30/ebusd/wiki/3.1.-TCP-client-commands#write>`_.
