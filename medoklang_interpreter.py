import pandas as pd
import medoklang_lexer
import medoklang_parser


class BasicExecute:
    def __init__(self, tree, env):
        self.env = env
        try:
            result = self.walkTree(tree)
            if result is not None and isinstance(result, int):
                print(result)
            if isinstance(result, str) and result[0] == '"':
                print(result)
        except Exception as e:
            print("Ana kesalahan:", str(e))
    

    def walkTree(self, node):
        if isinstance(node, int):
            return node
        if isinstance(node, str):
            return node

        if node is None:
            return None

        if node[0] == 'program':
            if node[1] is None:
                self.walkTree(node[2])
            else:
                self.walkTree(node[1])
                self.walkTree(node[2])

        if node[0] == 'num':
            return node[1]

        if node[0] == 'str':
            return node[1]

        if node[0] == 'print':
            if node[1][0] == '"':
                print(node[1][1:len(node[1])-1])
            else:
                return self.walkTree(node[1])

        if node[0] == 'if_stmt':
            result = self.walkTree(node[1])
            if result:
                return self.walkTree(node[2][1])
            return self.walkTree(node[2][2])

        if node[0] == 'condition_eqeq':
            return self.walkTree(node[1]) == self.walkTree(node[2])

        if node[0] == 'fun_def':
            self.env[node[1]] = node[2]

        if node[0] == 'fun_call':
            try:
                return self.walkTree(self.env[node[1]])
            except KeyError:
                raise KeyError("Fungsi '{}' ora ditetepake".format(node[1]))
                return None

        if node[0] == 'add':
            return self.walkTree(node[1]) + self.walkTree(node[2])
        elif node[0] == 'sub':
            return self.walkTree(node[1]) - self.walkTree(node[2])
        elif node[0] == 'mul':
            return self.walkTree(node[1]) * self.walkTree(node[2])
        elif node[0] == 'div':
            return int(self.walkTree(node[1]) / self.walkTree(node[2]))

        if node[0] == 'var_assign':
            self.env[node[1]] = self.walkTree(node[2])
            return node[1]

        if node[0] == 'var':
            try:
                return self.env[node[1]]
            except KeyError:
                raise KeyError("Variabel '{}' ora ditetepke".format(node[1]))

        if node[0] == 'for_loop':
            if node[1][0] == 'for_loop_setup':
                loop_setup = self.walkTree(node[1])

                loop_count = self.env.get(loop_setup[0])
                if loop_count is None:
                    raise KeyError("Variabel '{}' ora ditetepke".format(loop_setup[0]))

                loop_limit = loop_setup[1]

                for i in range(loop_count + 1, loop_limit + 1):
                    res = self.walkTree(node[2])
                    if res is not None:
                        print(res)
                    self.env[loop_setup[0]] = i
                del self.env[loop_setup[0]]

        if node[0] == 'for_loop_setup':
            return (self.walkTree(node[1]), self.walkTree(node[2]))
        

    def printEnvTable(self):
        env_table = pd.DataFrame(list(self.env.items()), columns=['Variable', 'Value'])
        print(env_table)

if __name__ == '__main__':
    lexer = medoklang_lexer.leksikal()
    parser = medoklang_parser.sintaksis()
    env = {}
    while True:
        try:
            text = input('medok > ')
        except EOFError:
            break
        if text:
            if text == 'tabin':
                executor.printEnvTable()
            else:
                try:
                    tree = parser.parse(lexer.tokenize(text))
                    executor = BasicExecute(tree, env)
                except Exception as e:
                    print("Ana kesalahan:", str(e))