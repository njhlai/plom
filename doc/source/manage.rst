.. Plom documentation
   Copyright 2020-2022 Colin B. Macdonald
   SPDX-License-Identifier: AGPL-3.0-or-later


Managing a server
=================

Plom Manager is a tool to monitor the marking team's progress as well
as perform various server oversight actions.

.. warning::

   This tool is not particularly well-tested, and is still under development.
   Proceed with caution.


Starting Plom Manager
----------------------

You can use the regular :doc:`Plom Client <install-client>`
but login as ``manager`` instead of your regular user.

Alternatively, you can run :doc:`plom-manager` from the command line.


User management
---------------

You can add users, change passwords, and disable/enable accounts in
the "Users" tab.


Progress
--------

Some basic statistics and other information can be found in the
"Progress" tab.



Communication with your marking team
------------------------------------

Currently this is best handled out of band, for example, in-person or
using a chat or video conferencing tool.


Reverting annotations
---------------------

The "Review" tab of the Manager UI allows you to search based on
various criteria.
You can "Remove annotations" which will revert the marking of a
question and place it back in the "todo" pile.


Reviewing annotations
---------------------

Occasionally you might need to check over the marking of one of your
users.
The "Review" tab of the Manager UI allows you to search based on user
name, or other criteria.
You can sort the results by score, marking time, when the marking was
done, etc.

If you highlight some rows and click "Flag for review", the tasks
will be assigned to a special ``reviewer`` user.
The annotations will not be lost but the original user who marked them
will no longer be able to see them.
You can then login with the ``reviewer`` user in the regular marking
client and look through the tasks, possibly revising the marking.

.. caution::

   As far as we know, the "review" feature has not been used in
   practice; some caution is warranted.


Technical docs
--------------

* The command-line tool :doc:`plom-manager` directly launches the Plom
  Manager.  It can also be launched by logging into :doc:`plom-client`
  using the ``manager`` account.

* For scripting or other advanced usage, you can ``import plom.manager``
  in your own Python code.  See :ref:`module-plom-manager`.
