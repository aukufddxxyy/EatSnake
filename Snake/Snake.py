class map:
    def __init__(self):
        self.size = 31
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]

class Snake:
    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]

    def __init__(self, head: tuple, width):
        self.lenth = 10
        self.width = width
        self.d = 0
        self.direction = self.directions[self.d]
        self.body = [(head[0]+i, head[1]) for i in range(self.lenth)]
        self.head = self.body[0]

    def move(self, food):
        if self.eat(food):
            self.body.insert(0, food)
            self.head = food
            return ((True, (self.body[-1], self.body[0])))
        else:
            head = self.wall()
            tail = self.eat_self()
            if head:
                self.body.insert(0, head)
            else:
                head = (self.body[0][0]+self.direction[0], self.body[0][1]+self.direction[1])
                self.body.insert(0, head)
            if not tail:
                tail = [self.body.pop()]
            self.head = head
            return((False, (tail, head)))

    def change_direction(self, d: int):
        if 0 <= d <= 3:
            if (d <= 1 and self.d >= 2) or (d >= 2 and self.d <=1):
                self.d = d
                self.direction = self.directions[self.d]

    def eat(self, food):
        if food[0] == self.body[0][0] + self.direction[0] and food[1] == self.body[0][1] + self.direction[1]:
            return True
        else:
            return False
    
    def wall(self):
        if self.head[0] + self.direction[0] < 0:
            return (self.width-1, self.head[1])
        elif self.head[0] + self.direction[0] >= self.width:
            return (0, self.head[1])
        elif self.head[1] + self.direction[1] < 0:
            return (self.head[0], self.width-1)
        elif self.head[1] + self.direction[1] >=self.width:
            return (self.head[0], 0)

    def eat_self(self):
        try:
            index = self.body.index((self.head[0]+self.direction[0], self.head[1]+self.direction[1]))
        except ValueError:
            pass
        else:
            tail = self.body[index:]
            self.body = self.body[:index+1]
            return tail

if __name__ == '__main__':
    # snake = Snake((1, 1))
    # # snake.move()
    # snake.eat((0, 1))
    # snake.change_direction(2)
    # print(snake.move())
    # print(snake.body)
    a = [1, 2, 3]
    b = a.index(2)
    a = a[b+1:]
    print(a)
