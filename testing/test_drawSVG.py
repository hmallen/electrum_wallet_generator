from drawSVG.drawSVG import SVG
import logging
import sys

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

svg = SVG()

svg.addChildElement('rect',
                    {'x':0, 'y':0,
                     'width':58, 'height':58,
                     'fill':'none',
                     'stroke':'black',
                     'stroke-width':0.5})

seed = 'leave mistake radar early head expand uncover stairs merge hazard swear dutch'
seed_words = seed.split(' ')

logger.debug(seed_words)

seed_lines = []
for x in range(0, 12, 2):
    word_num = x + 1
    #line = str(word_num) + ') ' + seed_words[x] + ' ' + str(word_num + 1) + ') ' + seed_words[x + 1]
    line = seed_words[x] + ' ' + seed_words[x + 1]
    seed_lines.append(line)

logger.debug(seed_lines)

position = 6.5
for x in range(0, 6):
    svg.addChildElement('text',
                        {'x':29, 'y':position,
                         'font-family':'Ubuntu',
                         'font-size':6,
                         'text-anchor':'middle',
                         'dominant-baseline':'central'},
                        seed_lines[x])
    position += 9

svg.write('test.svg')
