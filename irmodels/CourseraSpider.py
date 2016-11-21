# -*- coding: utf-8 -*-
import re
import json
import scrapy
import uuid

from scrapy.selector import Selector

from peewee import *

from model import Course

cleanr = re.compile('<.*?>')

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class CourseraSpider(scrapy.Spider):

    name = 'udemy'

    start_urls = [
            'https://www.coursera.org/learn/html',
            'https://www.coursera.org/learn/python',
            'https://www.coursera.org/learn/matlab',
            'https://www.coursera.org/learn/crypto',
            'https://www.coursera.org/learn/progfun1',
            'https://www.coursera.org/learn/introcss',
            'https://www.coursera.org/learn/progfun1',
            'https://www.coursera.org/learn/parprog1',
            'https://www.coursera.org/learn/introcss',
            'https://www.coursera.org/learn/javascript',
            'https://www.coursera.org/learn/python-data',
            'https://www.coursera.org/learn/game-design',
            'https://www.coursera.org/learn/neurohacking',
            'https://www.coursera.org/learn/developer-iot',
            'https://www.coursera.org/learn/r-programming',
            'https://www.coursera.org/learn/ml-foundations',
            'https://www.coursera.org/learn/website-coding',
            'https://www.coursera.org/learn/neural-networks',
            'https://www.coursera.org/learn/web-development',
            'https://www.coursera.org/learn/machine-learning',
            'https://www.coursera.org/learn/learn-to-program',
            'https://www.coursera.org/learn/arduino-platform',
            'https://www.coursera.org/learn/responsivedesign',
            'https://www.coursera.org/learn/intro-programming',
            'https://www.coursera.org/learn/swift-programming',
            'https://www.coursera.org/learn/augmented-reality',
            'https://www.coursera.org/learn/web-design-project',
            'https://www.coursera.org/learn/python-text-mining',
            'https://www.coursera.org/learn/meteor-development',
            'https://www.coursera.org/learn/python-network-data',
            'https://www.coursera.org/learn/html-css-javascript',
            'https://www.coursera.org/learn/python-network-data',
            'https://www.coursera.org/learn/python-data-analysis',
            'https://www.coursera.org/learn/political-philosophy',
            'https://www.coursera.org/learn/python-data-analysis',
            'https://www.coursera.org/learn/interactive-python-2',
            'https://www.coursera.org/learn/interactive-python-1',
            'https://www.coursera.org/learn/duke-programming-web',
            'https://www.coursera.org/learn/data-scientists-tools',
            'https://www.coursera.org/learn/raspberry-pi-platform',
            'https://www.coursera.org/learn/responsive-web-design',
            'https://www.coursera.org/learn/algorithmic-thinking-1',
            'https://www.coursera.org/learn/python-machine-learning',
            'https://www.coursera.org/learn/how-to-create-a-website',
            'https://www.coursera.org/learn/principles-of-computing-1',
            'https://www.coursera.org/learn/hybrid-mobile-development',
            'https://www.coursera.org/learn/introduction-to-algorithms',
            'https://www.coursera.org/learn/python-social-network-analysis',
            'https://www.coursera.org/learn/python-programming-introduction',
            'https://www.coursera.org/learn/single-page-web-apps-with-angularjs',
            'https://www.coursera.org/learn/html-css-javascript-for-web-developers',
            ]

    def parse(self, response):
        data = response.css('script[type="application/ld+json"]::text').extract_first()
        data = json.loads(data)

        Course.create(
                course_id = uuid.uuid4(), 
                course_title = data['name'], 
                course_description = data['description'], 
                language = 'English', 
                level = 'All Levels', # response.css('td.td-data[data-reactid="153"]::text').extract_first(), 
                student_enrolled = 0, 
                ratings = 0, # int(response.css('span[data-reactid="383"]::text').extract_first()), 
                overall_rating = 0, # overall_rating, 
                course_url = response.url, 
                cover_image = data['thumbnail']['contentUrl'],
                source = 'coursera'
                )
