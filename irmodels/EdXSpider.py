# -*- coding: utf-8 -*-
import re
import scrapy
import uuid

from scrapy.selector import Selector

from peewee import *

from model import Course

cleanr = re.compile('<.*?>')

class EdXSpider(scrapy.Spider):

    name = 'edx'

    start_urls = [
            'https://www.edx.org/xseries/java-android-beginners',
            'https://www.edx.org/course/introduction-c-microsoft-dev210x-1',
            'https://www.edx.org/course/machine-learning-columbiax-csmm-102x',
            'https://www.edx.org/course/think-create-code-adelaidex-code101x-2',
            'https://www.edx.org/course/introduction-devops-microsoft-dev212x-1',
            'https://www.edx.org/course/advanced-css-concepts-microsoft-dev218x',
            'https://www.edx.org/course/programming-basics-iitbombayx-cs101-1x-0',
            'https://www.edx.org/course/introduction-typescript-microsoft-dev201x-1',
            'https://www.edx.org/course/applied-machine-learning-microsoft-dat203-3x',
            'https://www.edx.org/course/introduction-apache-spark-uc-berkeleyx-cs105x',
            'https://www.edx.org/course/data-science-essentials-microsoft-dat203-1x-1',
            'https://www.edx.org/course/artificial-intelligence-ai-columbiax-csmm-101x',
            'https://www.edx.org/course/mobile-computing-app-inventor-cs-trinityx-t002x',
            'https://www.edx.org/course/html5-part-2-advanced-techniques-w3cx-html5-2x-1',
            'https://www.edx.org/course/learn-program-using-python-utarlingtonx-cse1309x',
            'https://www.edx.org/course/introduction-cloud-computing-ieeex-cloudintro-x-1',
            'https://www.edx.org/course/introduction-mobile-application-hkustx-comp107x-1',
            'https://www.edx.org/course/advanced-software-construction-java-mitx-6-005-2x',
            'https://www.edx.org/course/principles-machine-learning-microsoft-dat203-2x-1',
            'https://www.edx.org/course/introduction-mobile-application-hkustx-comp107x-1',
            'https://www.edx.org/course/big-data-analysis-apache-spark-uc-berkeleyx-cs110x',
            'https://www.edx.org/course/understanding-wireless-technology-notredamex-eg240x',
            'https://www.edx.org/course/introduction-programming-java-part-1-uc3mx-it-1-1x-1',
            'https://www.edx.org/course/cyberwar-surveillance-security-adelaidex-cyber101x-0',
            'https://www.edx.org/course/introduction-programming-java-part-1-uc3mx-it-1-1x-1',
            'https://www.edx.org/course/html5-part-1-html5-coding-essentials-w3cx-html5-1x-1',
            'https://www.edx.org/course/introduction-programming-java-part-1-uc3mx-it-1-1x-1',
            'https://www.edx.org/course/introduction-programming-java-part-2-uc3mx-it-1-2x-0',
            'https://www.edx.org/course/introduction-python-data-science-microsoft-dat208x-3',
            'https://www.edx.org/course/introduction-programming-java-part-2-uc3mx-it-1-2x-0',
            'https://www.edx.org/course/ap-computer-science-java-programming-purduex-cs180-1x',
            'https://www.edx.org/course/mobile-application-experiences-part-2-mitx-21w-789-2x',
            'https://www.edx.org/course/mobile-application-experiences-part-3-mitx-21w-789-3x',
            'https://www.edx.org/course/mobile-application-experiences-part-4-mitx-21w-789-4x',
            'https://www.edx.org/course/mobile-application-experiences-part-5-mitx-21w-789-5x',
            'https://www.edx.org/course/ap-computer-science-java-programming-purduex-cs180-1x',
            'https://www.edx.org/course/introduction-data-storage-management-ieeex-storage101x',
            'https://www.edx.org/course/creating-programmatic-sql-database-microsoft-dat215-2x',
            'https://www.edx.org/course/clep-information-systems-computer-upvalenciax-isc101-1x',
            'https://www.edx.org/course/clep-information-systems-computer-upvalenciax-isc101-2x',
            'https://www.edx.org/course/clep-information-systems-computer-upvalenciax-isc101-3x',
            'https://www.edx.org/course/clep-information-systems-computer-upvalenciax-isc101-4x',
            'https://www.edx.org/course/distributed-machine-learning-apache-uc-berkeleyx-cs120x',
            'https://www.edx.org/course/java-fundamentals-android-development-galileox-caad001x',
            'https://www.edx.org/course/introduction-java-programming-part-1-hkustx-comp102-1x-2',
            'https://www.edx.org/course/knowledge-management-big-data-business-hkpolyux-ise101x-1',
            'https://www.edx.org/course/cs-all-introduction-computer-science-harveymuddx-cs005x-0',
            'https://www.edx.org/course/angularjs-advanced-framework-techniques-microsoft-dev221x',
            'https://www.edx.org/course/introduction-devops-transforming-linuxfoundationx-lfs161x',
            'https://www.edx.org/course/data-cleansing-data-quality-services-dqs-microsoft-dat218x',
            'https://www.edx.org/course/computing-technology-inside-smartphone-cornellx-engri1210x-0',
            ]

    def parse(self, response):
        course_title = response.css('h1#course-intro-heading::text').extract_first().strip()
        # enrolled_information = response.css('span.rating-and-enrolled__element').extract()

        # rating = [x.strip() for x in response.css('span.rate-count>span.tooltip-container::text').extract_first().strip().split("\n")]
        skill_level = response.css('div#course-summary-area li:nth-child(6) span.block-list__desc::text').extract_first()

        course_thumbnail = response.css('div.course-detail-video a.video-link img').extract_first()
        course_thumbnail = course_thumbnail[course_thumbnail.find('"')+1:].replace('">','').strip()

        course_description = response.css('div#desc').extract_first()
        course_description = re.sub(cleanr, '', course_description).replace("\n\n", '').replace("  ", ' ').strip()

        overall_rating = float(rating[0].replace(',', ''))
        ratings = float(rating[-1].replace('ratings)', '').replace('(','').replace(',','').strip())
        student_enrolled = 0 # re.sub(cleanr, '', enrolled_information[2].replace('students enrolled', '').strip()).strip()
        student_enrolled = 0 # int(student_enrolled.replace(',', ''))

        Course.create(
                course_id = uuid.uuid4(), 
                course_title = course_title, 
                course_description = course_description, 
                language = 'English', 
                level = skill_level, 
                student_enrolled = student_enrolled, 
                ratings = ratings, 
                overall_rating = overall_rating, 
                course_url = response.url, 
                cover_image = course_thumbnail,
                source = 'edx'
                )
