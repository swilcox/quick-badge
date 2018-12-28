# quick-badge
A flask app to serve [shields.io](https://shields.io) badges for use with static docs that need dynamic shields.io badge / images.

## overview

This was mainly an excuse for me to play with a simple flask app, but serves a purpose where I work. We have internal
tests and metrics on a Jenkins server. The internal enterprise github `README.md` file needs badges that not only display
 the build status from Jenkins (which can be accomplished via a Jenkins plugin), but also test coverage percentage and flake8 (pep8)
 compliance which in our case is not part of the regular test.

## notes

Python 3 only now!

## usage

The project is designed to run on a Jenkins or other test server.

The current version of the code, supports coverage, flake8 and version status badges. The default directory where the files should
be added is `../stati/<project>/<status_name>`.

For example, the output of the `coverage report` command should be written to `../stati/myproject/coverage`.

Then, to gain access to the coverage badge, you'd have a link to an image (`img` tag) with a `src=http://jenkins-server:5000/myproject/coverage`.

The quick-badge app will read the `coverage` file contents and parse the results according to the coverage metrics rules which parses the
output file and decideds which color to apply (based on the percentage). It then gets the results for the badge from shields.io and passes
that on as the image data.

For unknown types, it will just use the last line of the file and lightgray as the color.

Again, this was just for experimenting but might be of value to someone. Obviously, a bunch of things could be done to make this better including:

- caching
- self-generation of the svg
- plugable architecture
- soft-encoding of configuration
