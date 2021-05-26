#! /usr/bin/env python3


import random
import os


AUTHOR_NAME = 'Tarmo Kivioja'
RAFFLE_PREFIX = ''
RAFFLE_POSTFIX = ' putosi :('
INTRO_TITLE = 'Osallistujat'
CONGRATS_TITLE = 'Onnea voittajalle!'
PARTICIPANTS_FILE = 'osallistujat.txt'
TEMPLATE_FILE = 'rigged.template.tex'
TEX_FILE = 'rigged.tex'


def main():
    template = read_template()
    participants = read_participants()
    tex_contents = make_tex(template, participants)
    write_tex(tex_contents)
    os.system(f'latexmk -pdf -pv {TEX_FILE}')
    return 0


def read_template():
    with open(TEMPLATE_FILE) as f:
        return f.read()


def read_participants():
    with open(PARTICIPANTS_FILE) as f:
        return [name.strip() for name in f]


def make_tex(template, participants):
    raffle_frames, winner = make_raffle(participants)
    return (template
            .replace('%% AUTHOR_NAME %%', AUTHOR_NAME)
            .replace('%% INTRO_FRAME %%', make_intro(participants))
            .replace('%% RAFFLE_FRAMES %%', raffle_frames)
            .replace('%% CONGRATS_FRAME %%', make_congrats(winner))
            )


def make_frame(contents, title=''):
    if title == '':
      return '\n'.join([
          r'\begin{frame}',
          f'{contents}',
          r'\end{frame}'
      ])
    else:
      return '\n'.join([
          r'\begin{frame}',
          f'\\frametitle{{{title}}}',
          f'{contents}',
          r'\end{frame}'
      ])

def make_list(items):
    def color(name, eliminated):
        return f'\\textcolor{{elim}}{{{name}}}' if eliminated else f'\\textbf{{{name}}}'

    items = '\n'.join([f'\\item {color(name, eliminated)}'
                       for name, eliminated in items])
    return '\n'.join([r'\begin{AutoMultiColItemize}',
                      items,
                      r'\end{AutoMultiColItemize}'])


def make_intro(participants):
    items = [(p, False) for p in participants]
    return make_frame(make_list(items), INTRO_TITLE)


def make_raffle(participants):
    elimination_order = [name for name in participants]
    random.shuffle(elimination_order)
    eliminated = set()
    frames = []
    for eliminate in elimination_order[:-1]:
        eliminated.add(eliminate)
        items = [(name, name in eliminated) for name in participants]
        title = f'{RAFFLE_PREFIX}{eliminate}{RAFFLE_POSTFIX}'
        frames.append(make_frame(make_list(items), title))
    return ('\n\n'.join(frames), elimination_order[-1])


def make_congrats(winner):
    contents = '\n'.join([
        r'\begin{center}',
        f'{{\\huge \\textbf{{{winner}}}}}',
        r'\end{center}'
    ])
    return make_frame(contents, CONGRATS_TITLE)


def write_tex(contents):
    with open(TEX_FILE, 'w') as f:
        f.write(contents)
    

if __name__ == '__main__':
    main()
