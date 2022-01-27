
import pygame
import time


class Widgets:
    def __init__(self, window):
        self.window = window
        self.wid = []

    def Input(self, id, x, y, w=100, h=20, text='', color='#FFFFFF', act=0, font_size=16):
        self.wid.append({'type': 'Input', 'text': text, 'id': id, 'x': x, 'y': y, 'w': w, 'h': h,
                         'color': color, 'act': act, 'elem': len(text), 'font_size': font_size})

    def Button(self, text, id, x, y, w=100, h=30, color='#FFFFFF', font_size=16):
        self.wid.append({'type': 'Button', 'text': text, 'id': id, 'x': x, 'y': y, 'w': w, 'h': h,
                         'color': color, 'font_size': font_size})

    def Text(self, text, x, y, color='#FFFFFF', font_size=16):
        self.wid.append({'type': 'Text', 'text': text, 'id': '', 'x': x, 'y': y, 'w': len(text)*7+3, 'h': 20,
                         'color': color, 'font_size': font_size})

    def update(self):

        x, y = pygame.mouse.get_pos()
        for w in self.wid:
            if w['type'] == 'Button' and w['x'] < x < w['x'] + w['w'] and w['y'] < y < w['y'] + w['h']:
                pygame.draw.rect(self.window, '#FF3333', (w['x'], w['y'], w['w'], w['h']))
            else:
                pygame.draw.rect(self.window, w['color'], (w['x'], w['y'], w['w'], w['h']))
            if w['type'] != 'Text':
                pygame.draw.rect(self.window, (0, 0, 0), (w['x'], w['y'], w['w'], w['h']), 1)
            font = pygame.font.SysFont('arial', w['font_size'])
            text = font.render(w['text'], True, (0, 0, 0))
            if w['type'] == 'Text' or w['type'] == 'Button':
                self.window.blit(text, (w['x'] + w['w']//2-len(w['text']*4)-7, w['y'] + w['h']//2-14))
            else:
                self.window.blit(text, (w['x'] + 3, w['y'] + 1))
            if w['type'] == 'Input':
                if w['act'] and int(time.time()-w['act']) % 2 == 0:
                    fs = w['font_size']-1
                    pygame.draw.line(self.window, (50, 50, 50), (w['x']+4+w['elem']*fs//2, w['y']+3),
                                     (w['x']+4+w['elem']*fs//2, w['y']+fs+3), 2)

    def event(self, event):
        for w in self.wid:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if w['type'] == 'Input':
                    w['act'] = 0
                if w['x'] < x < w['x'] + w['w'] and w['y'] < y < w['y'] + w['h']:
                    if w['type'] == 'Input':
                        w['act'] = time.time()
                        w['elem'] = len(w['text'])
                    if w['type'] == 'Button':
                        return w['id']

            if w['type'] == 'Input' and w['act'] and event.type == pygame.KEYDOWN:
                w['act'] = time.time()
                if 47 < event.key < 58 and len(w['text']) < w['w']//(w['font_size']//2)-1:
                    w['text'] += chr(event.key)
                    w['elem'] += 1
                if event.key == pygame.K_BACKSPACE and len(w['text']) > 0:
                    w['text'] = w['text'][:w['elem']-1] + w['text'][w['elem']:]
                    w['elem'] -= 1
                if event.key == pygame.K_LEFT and w['elem'] > 0:
                    w['elem'] -= 1
                if event.key == pygame.K_RIGHT and w['elem'] < len(w['text']):
                    w['elem'] += 1

    def get(self, id):
        for w in self.wid:
            if w['id'] == id:
                return w
        return {}
