WIN = "win32"
LUX = "linux"

ALIAS = "alias"
ARGS = "args"

HELP_CMD = {WIN: {"--help": "/?", "/?": "/?"},
            LUX: {"--help": "--help", "/?": "--help"}}

COMMANDS = {
    "cd": {
        WIN: {ALIAS: "cd", ARGS: {**HELP_CMD[WIN]}},
        LUX: {ALIAS: "cd", ARGS: {**HELP_CMD[LUX]}}
    },
    "pwd": {
        WIN: {ALIAS: "cd", ARGS: {**HELP_CMD[WIN]}},
        LUX: {ALIAS: "pwd", ARGS: {**HELP_CMD[LUX]}}
    },
    "ls": {
        WIN: {ALIAS: "dir", ARGS: {**HELP_CMD[WIN]}},
        LUX: {ALIAS: "ls", ARGS: {**HELP_CMD[LUX]}}
    },
    "mkd": {
        WIN: {ALIAS: "mkdir", ARGS: {**HELP_CMD[WIN]}},
        LUX: {ALIAS: "mkdir", ARGS: {**HELP_CMD[LUX]}}
    },
    "mkf": {
        WIN: {ALIAS: "echo>", ARGS: {**HELP_CMD[WIN]}},
        LUX: {ALIAS: "echo>", ARGS: {**HELP_CMD[LUX]}}
    },
    "rmd": {
        WIN: {ALIAS: "rmdir", ARGS: {**HELP_CMD[WIN]}},
        LUX: {ALIAS: "rm -r", ARGS: {**HELP_CMD[LUX]}}
    },
    "rmf": {
        WIN: {ALIAS: "del", ARGS: {**HELP_CMD[WIN]}},
        LUX: {ALIAS: "rm", ARGS: {**HELP_CMD[LUX]}}
    },
    "echo": {
        WIN: {ALIAS: "echo", ARGS: {**HELP_CMD[WIN]}},
        LUX: {ALIAS: "echo", ARGS: {**HELP_CMD[LUX]}}
    },
    "dog": {
        WIN: {ALIAS: "type", ARGS: {**HELP_CMD[WIN]}},
        LUX: {ALIAS: "cat", ARGS: {**HELP_CMD[LUX]}}
    },
    "cp": {
        WIN: {ALIAS: "copy", ARGS: {**HELP_CMD[WIN]}},
        LUX: {ALIAS: "cp", ARGS: {**HELP_CMD[LUX]}}
    },
    "mv": {
        WIN: {ALIAS: "move", ARGS: {**HELP_CMD[WIN]}},
        LUX: {ALIAS: "mv", ARGS: {**HELP_CMD[LUX]}}
    },
    "rn": {
        WIN: {ALIAS: "move", ARGS: {**HELP_CMD[WIN]}},
        LUX: {ALIAS: "mv", ARGS: {**HELP_CMD[LUX]}}
    },
    "root": {
        WIN: {ALIAS: "", ARGS: {}},
        LUX: {ALIAS: "", ARGS: {}}
    },
}
