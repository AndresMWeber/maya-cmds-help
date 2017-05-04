If you're looking into this tool, you're looking for a programmatic way of getting Maya function signatures.
I personally built it so that I could compare my maya command calls against kwargs/args Maya expects to reduce errors.
Hope you'll find it useful!  Once you install you will now have a CLI tool called mayasig.


Usage:
  mayasig ls
  mayasig -h | --help
  mayasig --version

Options:
  -h --help                         Show this screen.
  --version                         Show version.

Examples:
  mayasig group


This package only supports the Maya 2017 help docs so far so please be aware.
I might backport a couple versions of the maya online help, but this is totally dependent on time.
