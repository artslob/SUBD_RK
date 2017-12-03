import os
import re

import errno
from random import shuffle

from django.template import Template, Context, Engine

question_regexp = re.compile(r'('
                             r'(?P<title>Question: (?P<number>\d+)\n)'
                             r'(?P<text>(.|\n)+?)'
                             r'(?P<options>([A-E]\. (.|\n)+?)+?)'
                             r'(?P<answer>Answer: .+\n)'
                             r'(?P<explanation>Explanation:\n(.|\n)+?)?'
                             r'(?=(Question: \d+)|$)'
                             r')')

options_regexp = re.compile('(([A-E]\. )((.|\n)+?))(?=([A-E]\. |$))')

directory = 'questions'


# Document faults:
# Queestion 66
# Qustion:86
# Qustion:101
# 151 without answer

def main():
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    with open('template.html') as template_file:
        template = Template(template_file.read(), engine=Engine())

    with open('questions.txt') as file:
        questions = [el[0] for el in question_regexp.findall(file.read())]
        length = len(questions)
        print(length)
        for question in questions:
            question = question_regexp.search(question)
            options = [(el[1], without_line_breaks(el[2])) for el in options_regexp.findall(question.group('options'))]
            # shuffle(options)
            number = int(question.group('number'))
            with open(os.path.join(directory, f'question{question.group("number")}.html'), 'w') as html:
                context = Context({
                    'title': without_line_breaks(question.group('title')),
                    'prev': str(number - 1) if number > 1 else None,
                    'next': str(number + 1) if number < length else None,
                    'text': without_line_breaks(question.group('text')),
                    'options': options,
                    'answer': without_line_breaks(question.group('answer')),
                    'explanation': without_line_breaks(question.group('explanation')),
                    'length': str(length),
                })
                html.write(template.render(context))


def without_line_breaks(s: str):
    return s.replace('\n', '').replace('\r', '') if s else None


if __name__ == '__main__':
    main()
