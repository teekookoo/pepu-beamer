#! /usr/bin/env python3


import random
import os


# Adjust these to customize the program
# TODO implement as command line flags

# Author to show on title slide
AUTHOR_NAME = 'Tarmo Kivioja'

# Title of intro slide
INTRO_TITLE = 'Osallistujat'

# The format of raffling slide titles is
# [RAFFLE_PREFIX][ELIMINATED_NAME][RAFFLE_SUFFIX]
RAFFLE_PREFIX = ''
RAFFLE_SUFFIX = ' putosi :('

# Title of the last slide with winner name
CONGRATS_TITLE = 'Onnea voittajalle!'

# Name of the file that contains participants, one per row
PARTICIPANTS_FILE = 'osallistujat.txt'

# Name of the .tex template from which the slides are generated
# Should contain the following strings somewhere
#   %% AUTHOR_NAME %%
#   %% INTRO_FRAME %%
#   %% RAFFLE_FRAMES %%
#   %% CONGRATS_FRAME %%
TEMPLATE_FILE = 'rigged.template.tex'

# Name of the intermediate .tex file,
# The end result will have the same name with .pdf suffix
TEX_FILE = 'rigged.tex'

# Should the program compile and open the resulting slides with latexmk?
COMPILE_AND_PREVIEW = True


def main():
    template = read_template(TEMPLATE_FILE)
    participants = read_participants(PARTICIPANTS_FILE)
    tex_contents = make_tex(template, participants)
    write_tex(tex_contents)
    if COMPILE_AND_PREVIEW:
      os.system(f'latexmk -pdf -pv {TEX_FILE}')
    return 0


# Read the template file and return as a string
def read_template(filename):
    with open(filename) as f:
        return f.read()


# Read the participant file and return as a list of strings
def read_participants(filename):
    with open(filename) as f:
        return [name.strip() for name in f]


# Turn the template string into a valid .tex string
def make_tex(template, participants):
    raffle_frames, winner = make_raffle(participants)
    return (template
            .replace('%% AUTHOR_NAME %%', AUTHOR_NAME)
            .replace('%% INTRO_FRAME %%', make_intro(participants))
            .replace('%% RAFFLE_FRAMES %%', raffle_frames)
            .replace('%% CONGRATS_FRAME %%', make_congrats(winner))
            )


# Wrap `contents` in \begin{frame} ... \end{frame},
# optionally setting `title`
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

# Turn the items into a multicolumn itmeize list
# `items` is a list of (string, bool) tuples where
# the string is the participant name and
# the bool indicates whether the participant has been eliminated
def make_list(items):
    def color(name, eliminated):
        return f'\\textcolor{{elim}}{{{name}}}' if eliminated else f'\\textbf{{{name}}}'

    items = '\n'.join([f'\\item {color(name, eliminated)}'
                       for name, eliminated in items])
    return '\n'.join([r'\begin{AutoMultiColItemize}',
                      items,
                      r'\end{AutoMultiColItemize}'])


# Generate the slide that lists all participants before raffling
def make_intro(participants):
    items = [(p, False) for p in participants]
    return make_frame(make_list(items), INTRO_TITLE)


# Generate the raffling slides where one participant is eliminiated
# per slide
def make_raffle(participants):
    elimination_order = [name for name in participants]
    random.shuffle(elimination_order)
    eliminated = set()
    frames = []
    for eliminate in elimination_order[:-1]:
        eliminated.add(eliminate)
        items = [(name, name in eliminated) for name in participants]
        title = f'{RAFFLE_PREFIX}{eliminate}{RAFFLE_SUFFIX}'
        frames.append(make_frame(make_list(items), title))
    return ('\n\n'.join(frames), elimination_order[-1])


# Generate the last slide that contains the winner
def make_congrats(winner):
    contents = '\n'.join([
        r'\begin{center}',
        f'{{\\huge \\textbf{{{winner}}}}}',
        r'\end{center}'
    ])
    return make_frame(contents, CONGRATS_TITLE)


# Save `contents` to `TEX_FILE`
def write_tex(contents):
    with open(TEX_FILE, 'w') as f:
        f.write(contents)
    

# `main` is the entry point
if __name__ == '__main__':
    main()
