class TopClass:
    top = True

    def print_top(self):
        print('TopClass:', self.top)



class SubClass(TopClass):
    top = False


test = SubClass()

test.print_top()