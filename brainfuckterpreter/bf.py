import readchar

class ParseException(Exception):
    def __init__(self, index, character):
        super(ParseException, self).__init__(
            'Error during code parsing at character {}'.format(index)
        )
        self.error_index = index
        self.error_character = character

class BFEvaluator(object):
    def __init__(self):
        super(BFEvaluator, self).__init__()

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

    def evaluate(self, program):
        jump_map = self._create_jump_map(program)

        index = 0
        program_counter = 0
        memory = bytearray([0 for i in range(1024)])
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
                memory[program_counter] = ord(readchar.readchar())
            elif token == "[":
                if memory[program_counter] == 0:
                    index = jump_map[index]
            elif token == "]":
                if memory[program_counter] != 0:
                    index = jump_map[index]

            index = index + 1
