import pygame as pg
from random import choice
from time import sleep
import widgets


def _ways(hist, x, y):
    ways = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    ways_res = []
    if x == 0 and y == m-1:
        return []
    for i in range(len(ways)):
        if not(ways[i][0] < 0 or ways[i][0] >= n or ways[i][1] < 0 or ways[i][1] >= m
               or hist[ways[i][0]][ways[i][1]] != 0):
            ways_res.append(ways[i])
    return ways_res


def generator(n, m):
    aG = [[1] * m for _ in range(n)]
    aV = [[1] * m for _ in range(n)]
    hist = [[0] * m for _ in range(n)]
    x, y, p, steck, k = n - 1, 0, 1, [], 0
    x1, y1 = x, y+1
    while p < n * m:
        p += 1
        hist[x][y] = 1
        steck.append((x, y))

        while len(_ways(hist, x, y)) == 0:
            x, y = steck[-1]
            steck.pop()

        my_ways = _ways(hist, x, y)
        if (x+(x-x1), y+(y-y1)) in my_ways:
            for i in range(100):
                my_ways.append((x+(x-x1), y+(y-y1)))

        if (x+1, y) in my_ways:
            for i in range(5):
                my_ways.append((x+1, y))

        if (x, y-1) in my_ways:
            for i in range(5):
                my_ways.append((x, y-1))

        x1, y1 = choice(my_ways)

        pg.draw.line(window, (0, 0, 150), (y * 10 + 5, x * 10 + 5),
                     (y1 * 10 + 5, x1 * 10 + 5), 2)
        pg.display.flip()
        # sleep(0.001)

        aV[x if x < x1 else x1][y] = 0 if x != x1 else aV[x if x < x1 else x1][y]
        aG[x][y if y < y1 else y1] = 0 if y != y1 else aG[x][y if y < y1 else y1]
        x, x1 = x1, x
        y, y1 = y1, y

    return aG, aV


def show(aG, aV):
    window.fill((100, 100, 100))

    for i in range(n):
        for j in range(m):
            if aG[i][j]:
                pg.draw.line(window, (0, 0, 0), (j * 10 + 10, i * 10), (j * 10 + 10, i * 10 + 10))

    for i in range(n):
        for j in range(m):
            if aV[i][j]:
                pg.draw.line(window, (0, 0, 0), (j * 10, i * 10 + 10), (j * 10 + 10, i * 10 + 10))

    pg.draw.rect(window, (250, 0, 0), ((m - 1) * 10 + 1, 1, 8, 8))
    pg.display.flip()


def finder(aG, aV, n, m, x, y):
    sx, sy = x, y
    status = [[0]*m for _ in range(n)]
    path = []

    while x != 0 or y != m-1:
        status[x][y] += 1
        path.append((x, y))
        mins = 1000
        way = (0, 0)
        w = [(x - 1, y), (x, y + 1), (x, y - 1), (x + 1, y)]
        st = [aV[x - 1][y], aG[x][y], aG[x][y - 1], aV[x][y]]
        k = 0
        for i in range(len(w)):
            if 0 <= w[i][0] < n and 0 <= w[i][1] < m and not st[i] and status[w[i][0]][w[i][1]] != 1000:
                k += 1
                if status[w[i][0]][w[i][1]] < mins:
                    mins = status[w[i][0]][w[i][1]]
                    way = w[i]

        if k == 1 and not(sx == x and sy == y):
            status[x][y] = 1000
            pg.draw.circle(window, (250, 0, 0), (y * 10 + 5, x * 10 + 5), 2)
        else:
            pg.draw.circle(window, (250, 150, 0), (y * 10 + 5, x * 10 + 5), 2)

        sleep(0.005)
        x, y = way
        pg.draw.circle(window, (250, 150, 0), (y * 10 + 5, x * 10 + 5), 2)
        pg.display.flip()

    ans = []
    for p in path:
        if status[p[0]][p[1]] != 1000:
            ans.append(p)

    return ans + [(0, m-1)]


pg.init()
window = pg.display.set_mode((400, 310))
pg.display.set_caption('Лабиринт')
window.fill((100, 100, 100))

widg = widgets.Widgets(window)
widg.Text('Длина', 30, 40, color=(100, 100, 100), font_size=20)
widg.Input('inp_n', 100, 30, h=30, text='60', font_size=20)
widg.Text('Ширина', 30, 80, color=(100, 100, 100), font_size=20)
widg.Input('inp_m', 100, 70, h=30, text='130', font_size=20)
widg.Button('СТАРТ', 'but', 120, 130, w=150, h=40, color='#999999', font_size=20)

widg.Text('Правила:', 30, 200, color=(100, 100, 100), font_size=14)
widg.Text('Старт - левый нижний угол, финиш - правый верхний. ', 50, 220, color=(100, 100, 100), font_size=14)
widg.Text('Рекомендуемый размер 60X130. ', 40, 240, color=(100, 100, 100), font_size=14)
widg.Text('Пройдите лабиринт, используя стрелки клавиатуры. ', 50, 260, color=(100, 100, 100), font_size=14)
widg.Text('Нажмите "f" чтобы программа помогла найти выход. ', 50, 280, color=(100, 100, 100), font_size=14)

game, sett = True, True
while sett:
    widg.update()
    pg.display.flip()
    for e in pg.event.get():
        ev = widg.event(e)
        if e.type == pg.QUIT:
            game, sett = False, False
        if ev == 'but':
            sett = False

n, m = int(widg.get('inp_n')['text']), int(widg.get('inp_m')['text'])
pg.quit()

aG, aV = [], []
if game:
    pg.init()
    window = pg.display.set_mode((m*10, n*10))
    pg.display.set_caption('Лабиринт '+str(n)+' X '+str(m))
    window.fill((100, 100, 100))
    aG, aV = generator(n, m)
    show(aG, aV)

win, x, y = False, n-1, 0
while game:
    pg.draw.circle(window, (250, 150, 0), (y * 10 + 5, x * 10 + 5), 4)
    pg.display.flip()

    if (x, y) == (0, m-1):
        font = pg.font.SysFont('segoeprint', 100)
        text = font.render('ПОБЕДА', True, (250, 50, 50))
        window.blit(text, (m*10 // 2-130, n*10 // 2-50))
        win = True

    for e in pg.event.get():
        if e.type == pg.QUIT:
            game = False

        if not win and e.type == pg.KEYDOWN:
            if e.key in [pg.K_RIGHT, pg.K_LEFT, pg.K_UP, pg.K_DOWN]:
                pg.draw.circle(window, (100, 100, 100), (y * 10 + 5, x * 10 + 5), 4)

            if e.key == pg.K_f:
                ans = finder(aG, aV, n, m, x, y)
                sleep(0.5)

                for i in range(n):
                    for j in range(m):
                        pg.draw.circle(window, (100, 100, 100), (j * 10 + 5, i * 10 + 5), 3)
                pg.draw.rect(window, (250, 0, 0), ((m - 1) * 10 + 1, 1, 8, 8))

                pos = ans[0]
                for i in range(len(ans)):
                    pg.draw.line(window, (250, 150, 0), (pos[1] * 10 + 5, pos[0] * 10 + 5),
                                 (ans[i][1] * 10 + 5, ans[i][0] * 10 + 5), 2)
                    pos = ans[i]
                    pg.display.flip()
                    sleep(0.005)
                win = True

            if e.key == pg.K_LEFT and y > 0 and not aG[x][y-1]:
                y -= 1
                while y > 0 and not aG[x][y-1] and aV[x-1][y] and aV[x][y]:
                    pg.draw.circle(window, (100, 100, 100), (y * 10 + 5, x * 10 + 5), 4)
                    y -= 1
                    pg.draw.circle(window, (250, 150, 0), (y * 10 + 5, x * 10 + 5), 4)
                    pg.display.flip()
                    sleep(0.01)

            if e.key == pg.K_RIGHT and y < m-1 and not aG[x][y]:
                y += 1
                while y < m-1 and not aG[x][y] and aV[x-1][y] and aV[x][y]:
                    pg.draw.circle(window, (100, 100, 100), (y * 10 + 5, x * 10 + 5), 4)
                    y += 1
                    pg.draw.circle(window, (250, 150, 0), (y * 10 + 5, x * 10 + 5), 4)
                    pg.display.flip()
                    sleep(0.01)

            if e.key == pg.K_UP and x > 0 and not aV[x-1][y]:
                x -= 1
                while x > 0 and not aV[x-1][y] and aG[x][y-1] and aG[x][y]:
                    pg.draw.circle(window, (100, 100, 100), (y * 10 + 5, x * 10 + 5), 4)
                    x -= 1
                    pg.draw.circle(window, (250, 150, 0), (y * 10 + 5, x * 10 + 5), 4)
                    pg.display.flip()
                    sleep(0.01)

            if e.key == pg.K_DOWN and x < n-1 and not aV[x][y]:
                x += 1
                while x < n-1 and not aV[x][y] and aG[x][y-1] and aG[x][y]:
                    pg.draw.circle(window, (100, 100, 100), (y * 10 + 5, x * 10 + 5), 4)
                    x += 1
                    pg.draw.circle(window, (250, 150, 0), (y * 10 + 5, x * 10 + 5), 4)
                    pg.display.flip()
                    sleep(0.01)
