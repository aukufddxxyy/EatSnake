import random


class Map:
    def __init__(self, size):
        self.size = size
        self.blanks = []
        for i in range(self.size):
            for j in range(self.size):
                self.blanks.append((i, j))

    def new_food(self):
        return random.choice(self.blanks)

    def change_blanks(self, head: list, tail: list):
        if tail:
            for i in tail:
                self.blanks.append(i)
        if head:
            for i in head:
                self.blanks.remove(i)


class Snake(Map):
    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    lenth = 10
    d = 0

    def __init__(self, size):
        super().__init__(size)
        self.head = (self.size // 2, self.size // 2)
        self.direction = self.directions[self.d]
        self.body = []
        self.init_body()
        self.food = self.new_food()

    def init_body(self):
        self.blanks.remove(self.head)
        for i in range(self.lenth):
            self.body.append((self.head[0]+i+1, self.head[1]))
            self.blanks.remove((self.head[0]+i+1, self.head[1]))

    def move(self):
        tail = []
        try:
            index = self.body.index(self.head)
        except ValueError:
            tail.append(self.body.pop())
        else:
            tail = tail + self.body[index-1:]
            self.body = self.body[:index-1]
        finally:
            self.body.insert(0, self.head)
            if self.eat_food():
                self.head = self.wall(self.food)
                self.body.insert(0, self.food)
                if self.head in self.body:
                    self.change_blanks([self.food], tail)
                else:
                    self.change_blanks([self.food, self.head], tail)
                self.food = self.new_food()
            else:
                self.head = self.wall(self.head)
                if self.head in self.body:
                    self.change_blanks([], tail)
                else:
                    self.change_blanks([self.head], tail)

    def change_direction(self, d: int):
        if 0 <= d <= 3:
            if (d <= 1 and self.d >= 2) or (d >= 2 and self.d <= 1):
                self.d = d
                self.direction = self.directions[self.d]

    def eat_food(self):
        if self.food[0] == self.body[0][0] + self.direction[0] and self.food[1] == self.body[0][1] + self.direction[1]:
            return True
    
    def wall(self, head):
        if head[0] + self.direction[0] < 0:
            return self.size-1, head[1]
        elif head[0] + self.direction[0] >= self.size:
            return 0, head[1]
        elif head[1] + self.direction[1] < 0:
            return head[0], self.size-1
        elif head[1] + self.direction[1] >= self.size:
            return head[0], 0
        else:
            return head[0]+self.direction[0], head[1]+self.direction[1]
    
    def eat_self(self, head):
        tail = []
        try:
            index = self.body.index(head)
        except ValueError:
            pass
        else:
            tail = tail + self.body[index-1:]
            self.body = self.body[:index-1]


if __name__ == '__main__':
    snake = Snake(31)
    # print(snake.food)
