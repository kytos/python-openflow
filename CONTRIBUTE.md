## Contributing

[fork]: https://github.com/of-ng/ofx-parser/fork
[pr]: https://github.com/of-ng/ofx-parser/compare
[readme]: https://github.com/github/ofx-parser#readme

If you wanna contribute to this project, below we present some ways in
which you can contribute. Informations about environment setup for developers
can be found at the [HACKING.md](HACKING.md) file.

## Create an Issue

If you find a bug in the project (and you don’t know how to fix it),
have trouble following the documentation or have a question about the project
– create an issue! There’s nothing to it and whatever issue you’re having,
you’re likely not the only one, so others will find your issue helpful, too.
For more information on how issues work, check out
[github's Issues guide](https://guides.github.com/features/issues/).

### Issues Pro Tips

  - **Check existing issues** for your issue. Duplicating an issue is slower
    for both parties so search through open and closed issues to see if
    what you’re running into has been addressed already.
  - **Be clear** about what your problem is: what was the expected outcome,
    what happened instead? Detail how someone else can recreate the problem.
  - **Link to demos** recreating the problem on things like 
    [JSFiddle](http://jsfiddle.net/) or [CodePen](http://codepen.io/).
  - **Include system details** like what the library or operating system
    you’re using and its version.
  - **Paste error output** or logs in your issue or in a
    [Gist](http://gist.github.com/). If pasting them in the issue, wrap it in
    three backticks: \`\`\` so that it renders nicely.\`\`\` like ```this```


## Pull Request
If you’re able to patch the bug or add the feature yourself – fantastic, make a
pull request with the code! Be sure you’ve read any documents on contributing,
understand the license and have signed a CLA if required. Once you’ve submitted
a pull request the maintainer(s) can compare your branch to the existing one and
decide whether or not to incorporate (pull in) your changes.

### Pull Request Pro Tips

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
  - **Include screenshots** of the before and after if your changes include
    differences in HTML/CSS. Drag and drop the images into the body of your
    pull request.
  - **Contribute in the style of the project** to the best of your abilities.
    This may mean using indents, semi colons or comments differently than you
    would in your own repository, but makes it easier for the maintainer to
    merge, others to understand and maintain in the future.

### Open Pull Requests

Once you’ve opened a pull request a discussion will start around your proposed
changes. Other contributors and users may chime in, but ultimately the decision
is made by the maintainer(s). You may be asked to make some changes to your
pull request, if so, add more commits to your branch and push them – they’ll
automatically go into the existing pull request.

If your pull request is merged – great! If it is not, no sweat, it may not be
what the project maintainer had in mind, or they were already working on it.
This happens, so our recommendation is to take any feedback you’ve received and
go forth and pull request again – or create your own open source project.

## Code contribution steps review:
  - Fork the project & clone locally
  - Create an upstream remote and sync your local copy before you branch
  - Branch for each separate piece of work
  - Do the work, write good commit messages, and follow the project coding style
  - Push to your origin repository
  - Create a new PR in GitHub
  - Respond to any code review feedback

## Coding style


## Tests

This project follows the TDD (Test Driven Development) process.
Before writing code to contribute, write the tests related to the functionality
you wish to implement and then write the code to pass this test.

More info about the tests can be found on the
[HACKING.md](HACKING.md#tdd-test-driven-development) file.

## From raw files

We provide some files with raw packets to be used as input with the parser
library. To use our raw packet files, please take a look inside `raw` directory.

## IRC/Mailinglist

You can find us on the **#of-ng** IRC channel on **freenode.net** network.

There is also our dev mailing list:
**of-ng-dev** (at) **ncc** (dot) **unesp** (dot) **br**