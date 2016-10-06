
try:
    import readchar
except ImportError:
    INTERACTIVE_AVAILABLE = False
else:
    INTERACTIVE_AVAILABLE = True

class ParseException(Exception):
    def __init__(self, index, character):
        super(ParseException, self).__init__(
            'Error during code parsing at character {}'.format(index)
        )
        self.error_index = index
        self.error_character = character

class BFEvaluator(object):
    def __init__(self, memory_size=1024, interactive=True):
        super(BFEvaluator, self).__init__()
        self.memory_size = memory_size
        self._interactive = interactive and INTERACTIVE_AVAILABLE

    @property
    def interactive(self):
        return self._interactive

    def _create_jump_map(self, program):
        jumps = []
        jump_map = {}

        for index, token in enumerate(program):
            if token == "[":
                jumps.append(index)
            elif token == "]":
                if len(jumps) == 0:
                    raise ParseException(index, token)

                start = jumps.pop()
                jump_map[start] = index
                jump_map[index] = start

        if len(jumps) != 0:
            raise ParseException(len(program), '')

        return jump_map

    def evaluate(self, program, input_string=None):
        jump_map = self._create_jump_map(program)

        index = 0
        program_counter = 0
        memory = bytearray([0 for i in range(self.memory_size)])
        while index < len(program):
            token = program[index]
            if token == ">":
                program_counter = program_counter + 1
            elif token == "<":
                program_counter = program_counter - 1
            elif token == "+":
                memory[program_counter] += 1
            elif token == "-":
                memory[program_counter] -= 1
            elif token == ".":
                print chr(memory[program_counter]),
            elif token == ",":
                if self.interactive:
                    memory[program_counter] = ord(readchar.readchar())
                elif input_string is not None:
                    if len(input_string) != 0:
                        memory[program_counter] = ord(input_string[0])
                        input_string = input_string[1:]
                    else:
                        memory[program_counter] = 0
            elif token == "[":
                if memory[program_counter] == 0:
                    index = jump_map[index]
            elif token == "]":
                if memory[program_counter] != 0:
                    index = jump_map[index]

            index = index + 1
