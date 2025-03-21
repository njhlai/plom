.. Plom documentation
   Copyright 2023 Colin B. Macdonald
   SPDX-License-Identifier: AGPL-3.0-or-later


Rubrics
=======

Plom uses the term "rubrics" to refer to reusable comments, where each
rubric is often (but not always) associated with a change in score.


Rubrics in the Client
---------------------

The list of rubrics appears on the left side of the client window, and
rubrics are typically organized into several tabs.  Keyboard shortcut
keys are designed to allow navigation up-and-down the list and between
tabs of rubrics.  You can press the ``?`` key to learn more about
Plom's shortcut keys.

Rubrics can be associated spatially with a particular region of the
page by dragging to create a box then clicking again to place the
rubric.

Rubrics are shared between markers.  When you create a new rubric, it
is immediately created server-side and shared with all users.

.. note::
   Currently rubrics are pulled from the server on Annotator start,
   or when users click the ``Sync`` button in the lower-left.
   We anticipate more automatic synchronization in the future.

One of Plom's goals is that a group of markers can collaboratively
construct and consistently apply a set of fair rubrics.  There are
several important caveats to be aware of in the current
implementation:

.. note::
   Currently, rubrics are owned by the user who created them.  If you
   need to modify someone else's rubric, Plom will instead offer to
   make a copy.  We anticipate relaxing this restriction in the future

.. warning::
   Currently, there is no mechanism to revisit papers that were
   affected by modifying a rubric.  For example if you change "-1 not
   the chain rule" into "-2 not the chain rule" then previously-marked
   papers will still have the "-1" version.  Developing a workflow for
   updating for such changes is of considerable interest.


Rubric Scope
------------

Question scope
^^^^^^^^^^^^^^

By default, rubrics are not shared between questions.
Currently this is not changeable, there is an [issue for that](TODO://).

Version-level scoping
^^^^^^^^^^^^^^^^^^^^^

If you have multiple versions, rubrics are by default shared between
versions of a question.  There are two ways of restricting things:

1. You can parameterize a rubric over versions, inserting text
   substitutions on a per-version basis.  This works well, for
   example, if one question has "x" while another has "y".


2. You can restrict rubrics to a particular version (or versions).

.. warning::
   Parameterized rubrics are a new feature: please discuss whether
   or not to use them with senior members of your grading team.


Scoping within a question
^^^^^^^^^^^^^^^^^^^^^^^^^

You can restrict a rubric to one part of a question in an informal
sense by creating groups.  For example, suppose Q3 is out of 12
points, where part (a) is worth 5 of those points.  You can create a
Rubric Group called "(a)", and restrict some of your rubrics to that
group.  Clients will typically display grouped rubrics in a tab.

Additionally, if several rubrics are marked as **exclusive** within a
group, then clients will allow you to choose at most one of them.
This can be combined with absolute rubrics such as "3 of 5: used
product and chain rules but calculations incorrect" and "4 of 5: right
idea, but there is a small calculation error".

.. warning::
   Rubric groups are a new feature: please discuss whether or not
   to use them with senior members of your grading team.


Managing rubrics
----------------

It also possible to populate the rubric database in bulk from external
tools such as a spreadsheet.  For example, this could be done before
marking begins or by re-using rubrics from a previous assessment.
See the :doc:`plom-create` command-line tool or the :doc:`module-plom-create`.
