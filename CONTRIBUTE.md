## Contributing

We'd love for you to contribute to our source code and to make Kytos even better
than it is today! Here are the guidelines we'd like you to follow:

 - [Code of Conduct](#coc)
 - [Question or Problem?](#question)
 - [Issues and Bugs](#issue)
 - [Feature Requests](#feature)
 - [Submission Guidelines](#submit)
 - [Coding Rules](#rules)
 - [Commit Message Guidelines](#commit)
 - [Signing the CLA](#cla)
 - [Further Info](#info)


## <a name="coc"></a> Code of Conduct

Help us keep Kytos open and inclusive. Please read and follow our [Code of
Conduct][coc].

## <a name="question"></a> Got a Question or Problem?

If you have questions about how to use any component of Kytos project, please
direct these to our [dev mailing list][kytos-dev]. We are also
available on [IRC][irc].

## <a name="issue"></a> Found an Issue?

If you find a bug in the source code or a mistake in the documentation, you can
help us by submitting an issue to our [GitHub Repository][github]. Even better
you can submit a Pull Request with a fix.

**Please see the Submission Guidelines below**.

## <a name="feature"></a> Want a Feature?
You can also request a new feature by submitting an issue to our [GitHub
Repository][github].  If you would like to implement a new feature then consider
what kind of change it is:

* **Major Changes** that you wish to contribute to the project should be
  discussed first on our [dev mailing list][kytos-dev] or [IRC][irc] so that we
can better coordinate our efforts, prevent duplication of work, and help you to
craft the change so that it is successfully accepted into the project.

* **Small Changes** can be crafted and submitted to the [GitHub
  Repository][github] as a Pull Request.

## <a name="docs"></a> Want a Doc Fix?

[describe the doc fix steps here]

## <a name="submit"></a> Submission Guidelines

### Submitting an Issue

When oppening a new issue, please, use the proper tags we provide to identify
the version of the release and the type of the issue that is being opened (i.e.:
discussion, bugs, etc). It is important to note that these issues will be used
as release's cutoff.

Before you submit your issue search the archive, maybe your question was already
answered.

If your issue appears to be a bug, and hasn't been reported, open a new issue.
Help us to maximize the effort we can spend fixing issues and adding new
features, by not reporting duplicate issues.  Providing the following
information will increase the chances of your issue being dealt with quickly:

* **Check existing issues** for your issue. Duplicating an issue is slower for
  both parties so search through open and closed issues to see if what you’re
running into has been addressed already.
* **Be clear** about what your problem is: what was the expected outcome, what
  happened instead? Detail how someone else can recreate the problem.
* **Motivation for or Use Case** - explain why this is a bug for you;
* **Include system details** like what the library or operating system you’re
  using and its version.
* **Paste error output** or logs in your issue or in a [Gist][github-gist]. If
  pasting them in the issue, wrap it in three backticks: \`\`\` so that it
renders nicely.\`\`\` like ```this```
* **Use Tags** Please, remember to tag your issue according to the version and the issue type.
* **Steps to reproduce** - please inform all the steps to reproduce the error;
* **Related Issues** - has a similar issue been reported before?;
* **Suggest a Fix** - if you can't fix the bug yourself, perhaps you can point
  to what might be causing the problem (line of code or commit)

For more information about github issues, please read [github's Issues
guide][github-issues].

### Submitting a Pull Request

If you’re able to patch the bug or add the feature yourself – fantastic, make a
pull request with the code! Be sure you’ve read any documents on contributing,
understand the license and have signed our [Contributor License Agreement
(CLA)](#cla). Once you’ve submitted a pull request the maintainer(s) can compare
your branch to the existing one and decide whether or not to incorporate (pull
in) your changes.

All Kytos subproject uses uses the [Semantic Versioning][semver] and we follow
the [Gitflow Workflow][gitflow]. All contributors should create a fork from
`develop` branch with the feature's name. Once the feature is implemented the
contributer should place a merge request to `develop` branch.

Before you submit your pull request consider the following guidelines:

* Search [GitHub](https://github.com/kytos/python-openflow/pulls) for an open or
  closed Pull Request that relates to your submission. You don't want to
  duplicate effort;
* Please sign our [CLA](#cla) before sending pull requests. We cannot accept
  code without this;
* Make your changes in a new git branch, from `develop` branch:

     ```shell
     git checkout -b my-fix-branch develop
     ```

* Create your patch, **including appropriate test cases**;
* Follow our [Coding Rules](#rules);
* Run the full Kytos test suite, as described in the [developer
  documentation][dev-doc], and ensure that all tests pass;
* Commit your changes using a very good descriptive commit message;

     ```shell
     git commit -a
     ```
  Note: the optional commit `-a` command line option will automatically "add"
  and "rm" edited files.

* Run our test suit to see if anything is broken:

    ```shell
    python3 setup.py test
    ```

* Push your branch to GitHub:

    ```shell
    git push origin my-fix-branch
    ```

* In GitHub, send a pull request to `python-openflow:develop`.
* If we suggest changes then:
  * Make the required updates.
  * Re-run the test suite to ensure tests are still passing.
  * Commit your changes to your branch (e.g. `my-fix-branch`).
  * Push the changes to your GitHub repository (this will update your Pull
    Request).

If the PR gets too outdated we may ask you to rebase and force push to update
the PR:

    ```shell
    git rebase master -i
    git push origin my-fix-branch -f
    ```

*WARNING. Squashing or reverting commits and forced push thereafter may remove
GitHub comments on code that were previously made by you and others in your
commits.*

That's it! Thank you for your contribution!

#### Hot Fix and Security Fix

#TODO: Quick describe of a hotfix

When a Hot or Security fix is required, a different workflow should be followed.
The contributer should clone the master branch and, after fixing the bug, it has
to be merged in master and develop branch.

First clone the master branch as following:

  ```shell
  git checkout -b issue-#001 master
  # Fix the bug
  git checkout master
  git merge issue-#001
  git push
  ```

Then, merge the fix to develop branch as well:

  ```shell
  git checkout develop
  git merge issue-#001
  git push
  ```

#### After your pull request is merged

After your pull request is merged, you can safely delete your branch and pull
the changes from the main (upstream) repository:

* Delete the remote branch on GitHub either through the GitHub web UI or your
  local shell as follows:

    ```shell
    git push origin --delete my-fix-branch
    ```

* Check out the `develop` branch:

    ```shell
    git checkout develop -f
    ```

* Delete the local branch:

    ```shell
    git branch -D my-fix-branch
    ```

* Update your `develop` with the latest upstream version:

    ```shell
    git pull --ff upstream develop
    ```

Information about environment setup for developers can be found at the
[HACKING.md](HACKING.md) file.


#### Pull Request Pro Tips

  - **[Fork](http://guides.github.com/activities/forking/) the repository** and
    clone it locally. Connect your local to the original ‘upstream’ repository
    by adding it as a remote. **Pull in** changes from ‘upstream’ often so that
    you stay up to date so that when you submit your pull request, merge
    conflicts will be less likely. See more detailed instructions
    [here](https://help.github.com/articles/syncing-a-fork).
  - **Create a [branch](http://guides.github.com/introduction/flow/)** for your
    edits.
  - **Be clear** about what problem is occurring and how someone can recreate
    that problem or why your feature will help. Then be equally as clear about
    the steps you took to make your changes.
  - **It’s best to test**. Run your changes against any existing tests if they
    exist and create new ones when needed. Whether tests exist or not,
    make sure your changes don’t break the existing project.
  - **Contribute in the style of the project** to the best of your abilities.
    This may mean using indents, semi colons or comments differently than you
    would in your own repository, but makes it easier for the maintainer to
    merge, others to understand and maintain in the future.

#### Open Pull Requests

Once you’ve opened a pull request a discussion will start around your proposed
changes. Other contributors and users may chime in, but ultimately the decision
is made by the maintainer(s). You may be asked to make some changes to your pull
request, if so, add more commits to your branch and push them – they’ll
automatically go into the existing pull request.

If your pull request is merged – great! If it is not, no sweat, it may not be
what the project maintainer had in mind, or they were already working on it.
This happens, so our recommendation is to take any feedback you’ve received and
go forth and pull request again – or create your own open source project.

#### Code contribution steps review:

  - Fork the project & clone locally
  - Create an upstream remote and sync your local copy before you branch
  - Branch for each separate piece of work
  - Do the work, write good commit messages, and follow the project coding style
  - Push to your origin repository
  - Create a new PR in GitHub
  - Respond to any code review feedback

## Coding style

We follow [PEP8](http://www.python.org/dev/peps/pep-0008/),
[PEP20](http://www.python.org/dev/peps/pep-0020/) and, as a short resume,
[The Best of the Best Practices (BOBP) Guide for Python](https://gist.github.com/sloria/7001839)

## Tests

This project tries to follow the TDD (Test Driven Development) process.  Before
writing code to contribute, write the tests related to the functionality you
wish to implement and then write the code to pass this test.

More info about the tests can be found on the
[HACKING.md](HACKING.md#tdd-test-driven-development) file.

## Use the raw raw files

We provide some files with raw packets to be used as input with the parser
library. Use theses files to test your features. To use our raw packet files,
please take a look inside `raw` directory.

## <a name="cla"></a> Signing the CLA

Please sign our Contributor License Agreement (CLA) before sending pull
requests. For any code changes to be accepted, the CLA must be signed. It's a
quick process, we promise!

* For individuals we have a [simple click-through form][individual-cla].

## IRC/Mailinglist

You can find us on the **#of-ng** IRC channel on **freenode.net** network.

There is also our dev mailing list:
**of-ng-dev** (at) **ncc** (dot) **unesp** (dot) **br**



[fork]: https://github.com/of-ng/ofx-parser/fork
[pr]: https://github.com/of-ng/ofx-parser/compare
[readme]: https://github.com/github/ofx-parser#readme
[github-gist]: http://gist.github.com/
[github-issues]: https://guides.github.com/features/issues/
[semver]: http://semver.org/
[gitflow]: https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow
