Contributing
============

We'd love for you to contribute to our source code and to make Kytos even better
than it is today! Here are the guidelines we follow:

-  `Got a Question or Problem? <#question>`__
-  `Found an Issue? <#issue>`__
-  `Want a Feature? <#feature>`__
-  `Want a Doc Fix? <#docs>`__
-  `Submission Guidelines <#submit>`__
-  `Coding Style <#style>`__
-  `Tests <#tests>`__
-  `Signing the CLA <#cla>`__
-  `IRC/Mailinglist <#contact>`__

Got a Question or Problem?
--------------------------

If you have questions about how to use any component of Kytos project, please
direct these to our `dev mailing list <#contact>`__. We are also available on
`IRC <#contact>`__.

Found an Issue?
---------------

If you find a bug in the source code or a mistake in the documentation, you can
help us by submitting an issue to our `GitHub Repository <https://github.com/kytos/python-openflow/issues>`__. Even better,
you can submit a Pull Request with a fix.

**Please see the Submission `Guidelines <#submit>`__ below**.

Want a Feature?
---------------

You can also request a new feature by submitting an issue to our `GitHub
  Repository <https://github.com/kytos/python-openflow/issues>`__. If you would like to implement a new feature, then
consider what kind of change it is:

-  | **Major Changes** that you wish to contribute to the project should be
   | discussed first on our `dev mailing list or IRC <#contact>`__, so that
   | we can better coordinate our efforts, prevent duplication of work, and help you
   | to craft the change so that it is successfully accepted into the project.

-  **Small Changes** can be crafted and submitted to the `GitHub
   Repository <github.com/kytos/python-openflow>`__ as a Pull Request.

Want a Doc Fix?
---------------

Feel free to `contact us <#contact>`__ or submit a pull request.

Submission Guidelines
---------------------

Submitting an Issue
~~~~~~~~~~~~~~~~~~~

Before you submit your issue, search the archive to check if the issue is
already there with an answer.

When opening a new issue, please, use the proper tags we provide to identify
the version of the release you are using and the type of the issue that is being
opened (i.e.: discussion, bugs, etc). It is important to note that these issues
will be used as release's cutoff.

If your issue appears to be a bug, and hasn't been reported, open a new issue.
Help us to maximize the effort we can spend both fixing issues and adding new
features by not reporting duplicate issues. The more relevant information you
provide, the faster contributors can tackle the issue. Here are some useful
information you might be able to provide:

-  **Check existing issues** for your issue. Duplicating an issue is slower for
   both parties so search through open and closed issues to see if what you’re
   running into has been already addressed;
-  **Be clear** about what your problem is: what was the expected outcome, what
   happened instead? Detail how someone else can recreate the problem;
-  **Motivation for or Use Case** - explain why this is a bug for you;
-  **Include system details** like what library or operating system you’re
   using and their versions;
-  **Paste error output** or logs in your issue or in a `Gist <http://gist.github.com/>`__. When
   pasting them in the issue, wrap it with three backticks: **\`\`\`** so that it
   renders nicely, like ``this``;
-  **Use Tags** Please, remember to tag your issue according to the version and
   the issue type;
-  **Steps to reproduce** - please inform all the steps to reproduce the error;
-  **Related Issues** - has a similar issue been reported before?
-  **Suggest a Fix** - if you can't fix the bug yourself, perhaps you can point
   to what might be causing the problem (line of code or commit).

For more information about github issues, please read `github's Issues
guide <https://guides.github.com/features/issues/>`__.

Submitting a Pull Request
~~~~~~~~~~~~~~~~~~~~~~~~~

If you’re able to patch the bug or add the feature yourself – fantastic, make a
pull request with the code! Be sure you’ve read the documents on contributing,
understand the license and have signed our `Contributor License Agreement
  (CLA) <#cla>`__. Once you’ve submitted a pull request, the maintainer(s) can
easily compare your branch to the existing one and decide whether or not to
incorporate (pull in) your changes.

All Kytos subproject uses uses the `Semantic Versioning <http://semver.org/>`__ and we follow
the `Gitflow Workflow <https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow>`__. All contributors should create a fork from
``develop`` branch with the feature's name. Once the feature is implemented the
contributor should place a pull request to the ``develop`` branch.

Before you submit your pull request consider the following guidelines:

-  Search `GitHub <https://github.com/kytos/python-openflow/pulls>`__ for an open or
   closed Pull Request that relates to your submission. You don't want to
   duplicate effort;
-  Please sign our `CLA <#cla>`__ before sending pull requests. We cannot accept
   code without this;
-  Make your changes in a new git branch, from ``develop`` branch:

   .. code:: shell

       git checkout -b my-fix-branch develop

-  **Include appropriate test cases**;
-  Follow our `Coding Rules <#rules>`__;
-  Commit your changes using very good and descriptive commit messages;
-  Please consider doing atomic commits (small changes in each commit).
-  Run our test suit to check if anything is broken:

   .. code:: shell

       python3 setup.py test

-  Push your branch to GitHub:

   .. code:: shell

       git push origin my-fix-branch

-  In GitHub, send a pull request to ``python-openflow:develop``.
-  If we suggest changes then:
-  Make the required updates.
-  Re-run the test suite to ensure tests are still passing.
-  Commit your changes to your branch (e.g. ``my-fix-branch``).
-  | Push the changes to your GitHub repository (this will update your Pull
   | Request).

If the PR gets too outdated we may ask you to rebase and force push to update
the PR:

.. code:: shell

    git pull
    git rebase develop -i
    git push origin my-fix-branch -f

*WARNING. Squashing or reverting commits and forced push thereafter may remove
GitHub comments on code that were previously made by you and others in your
commits.*

That's it! Thank you for your contribution!

Hot Fix and Security Fix
~~~~~~~~~~~~~~~~~~~~~~~~

When a Hot or Security fix is required, a different workflow should be followed.
The contributer should clone the master branch and, after fixing the bug, it has
to be merged in master and develop branch.

First clone the master branch as following:

.. code:: bash

    git checkout -b issue-#001 master
    # Fix the bug
    git checkout master
    git merge issue-#001
    git push

Then, merge the fix to develop branch as well:

.. code:: shell

    git checkout develop
    git merge issue-#001
    git push

After your pull request is merged
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After your pull request is merged, you can safely delete your branch and pull
the changes from the main (upstream) repository:

-  | Delete the remote branch on GitHub either through the GitHub web UI or your
   | local shell as follows:

   .. code:: shell

       git push origin --delete my-fix-branch

-  Check out the ``develop`` branch:

   .. code:: shell

       git checkout develop -f

-  Delete the local branch:

   .. code:: shell

       git branch -D my-fix-branch

-  If you haven't done it yet, add the ``upstream`` repository (only once):

   .. code:: shell

       git remote add upstream https://github.com/kytos/python-openflow.git
       git remote # you should now see origin and upstream

-  Update your ``develop`` with the latest upstream version:

   .. code:: shell

       git pull upstream develop

Information about environment setup for developers can be found in the
:doc:`HACKING` section.

Pull Request Pro Tips
~~~~~~~~~~~~~~~~~~~~~

-  **`Fork <http://guides.github.com/activities/forking/>`__ the repository** and
   clone it locally. Connect your local repository to the original ‘upstream’ one
   by adding it as a remote. **Pull in** changes from ‘upstream’ often to stay
   up to date so that when you submit your pull request, merge
   conflicts will be less likely. See more detailed instructions
   `here <https://help.github.com/articles/syncing-a-fork>`__.
-  **Create a `branch <http://guides.github.com/introduction/flow/>`__** for your
   edits.
-  **Be clear** about what problem is occurring and how someone can recreate
   that problem or why your feature will help. Then be equally as clear about
   the steps you took to make your changes.
-  **It’s best to test**. Run your changes against any existing tests if they
   exist and create new ones when needed, trying to cover all your code.
   Whether tests exist or not, make sure your changes don’t break the existing
   project.
-  **Contribute using the project style** to the best of your abilities.
   This may mean using indents, semi colons or comments differently than you
   would in your own repository, but makes it easier for the maintainer to
   merge, others to understand and maintain it in the future.

Open Pull Requests
~~~~~~~~~~~~~~~~~~

Once you’ve opened a pull request, a discussion will start around your proposed
changes. Other contributors and users may chime in, but ultimately the decision
is made by the maintainer(s). You may be asked to make some changes to your pull
request. If so, add more commits to your branch and push them – they’ll
automatically go into the existing pull request.

If your pull request is merged – great! If it is not, no sweat, it may not be
what the project maintainer had in mind, or they were already working on it.
This happens, so our recommendation is to take any feedback you’ve received and
go forth and pull request again – or create your own open source project
starting with the forked repository.

Code contribution steps review:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Fork the project & clone locally
-  Create an upstream remote and sync your local copy before you branch
-  Branch for each separate piece of work
-  Do the work, write good commit messages, and follow the project coding style
-  Push to your origin repository
-  Create a new PR in GitHub
-  Respond to any code review feedback

Coding style
------------

We follow `PEP8 <http://www.python.org/dev/peps/pep-0008/>`__,
`PEP20 <http://www.python.org/dev/peps/pep-0020/>`__ and, as a short resume,
`The Best of the Best Practices (BOBP) Guide for Python <https://gist.github.com/sloria/7001839>`__

Tests
-----

This project tries to follow the TDD (Test Driven Development) process. Before
writing code to contribute, write the tests related to the functionality you
wish to implement and then write the code to pass this test.

More info about the tests can be found in the :doc:`HACKING` section.

Use the raw packet files
~~~~~~~~~~~~~~~~~~~~~~~~

We provide some files with raw packets to be used as input with the parser
library. Use theses files to test your features. To use our raw packet files,
please take a look inside ``raw`` directory.

Signing the CLA
---------------

Please sign our Contributor License Agreement (CLA) before sending pull
requests. For any code changes to be accepted, the CLA must be signed. It's a
quick process, we promise!

IRC/Mailinglist
---------------

You can find us on the **#of-ng** IRC channel on **freenode.net** network.

There is also our dev mailing list:
**of-ng-dev** (at) **ncc** (dot) **unesp** (dot) **br**
