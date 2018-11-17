import argparse
import errno
import os
import re
import sys

from django.template import Template, Context, Engine

question_regexp = re.compile(r'('
                             r'(?P<title>Question: (?P<number>\d+)\n)'
                             r'(?P<text>(.|\n)+?)'
                             r'(?P<options>([A-G]\. (.|\n)+?)+?)'
                             r'(?P<answer>Answer: .+\n)'
                             r'(?P<explanation>Explanation:\n(.|\n)+?)?'
                             r'(?=(Question: \d+)|$)'
                             r')')

options_regexp = re.compile('(([A-G]\. )((.|\n)+?))(?=([A-G]\. |$))')


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', dest='input', default='rk1_questions.txt', help='Input file with questions')
    parser.add_argument('-d', '--dir', dest='dir', default='rk1', help="Output dir which holds result html's")
    parser.add_argument('-t', '--no-title', dest='title', action='store_false',
                        help='Specify this flag if you do not want to see question number on page')
    return parser.parse_args()


def main():
    args = get_args()
    print('Use -h to see help')

    try:
        os.makedirs(args.dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            print('Error occurred:', e)
            sys.exit(1)

    try:
        with open('template.html') as template_file:
            template = Template(template_file.read(), engine=Engine())

        with open(args.input) as file:
            questions = [el[0] for el in question_regexp.findall(file.read())]
            length = len(questions)
            for question in questions:
                question = question_regexp.search(question)
                options = [(el[1], line_breaks_to_spaces(el[2])) for el in options_regexp.findall(question.group('options'))]
                number = int(question.group('number'))
                with open(os.path.join(args.dir, f'question{question.group("number")}.html'), 'w') as html:
                    context = Context({
                        'title': line_breaks_to_spaces(question.group('title')) if args.title else None,
                        'prev': str(number - 1) if number > 1 else None,
                        'next': str(number + 1) if number < length else None,
                        'text': line_breaks_to_spaces(question.group('text')),
                        'options': options,
                        'answer': line_breaks_to_spaces(question.group('answer')),
                        'explanation': line_breaks_to_spaces(question.group('explanation')),
                        'length': str(length),
                    })
                    html.write(template.render(context))
        print('done')
    except (OSError, IOError) as e:
        print('Error occurred:', e)


def line_breaks_to_spaces(s: str) -> str:
    return s.replace('\n', ' ').replace('\r', ' ').strip() if s else ''


if __name__ == '__main__':
    main()
