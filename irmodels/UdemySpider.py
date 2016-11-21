# -*- coding: utf-8 -*-
import re
import scrapy
import uuid

from scrapy.selector import Selector

from peewee import *

from model import Course

cleanr = re.compile('<.*?>')

class UdemySpider(scrapy.Spider):

    name = 'udemy'

    start_urls = [
            'https://www.udemy.com/automate/',
            'https://www.udemy.com/django-core/',
            'https://www.udemy.com/python-1000/',
            'https://www.udemy.com/django-core/',
            'https://www.udemy.com/swift-program/',
            'https://www.udemy.com/python-for-maya/',
            'https://www.udemy.com/devslopes-ios10/',
            'https://www.udemy.com/learn-core-java/',
            'https://www.udemy.com/advanced-python/',
            'https://www.udemy.com/ionic-by-example/',
            'https://www.udemy.com/learn-j2ee-basics/',
            'https://www.udemy.com/python-for-rookies/',
            'https://www.udemy.com/java-8-new-features/',
            'https://www.udemy.com/whats-new-in-java-8/',
            'https://www.udemy.com/understand-javascript/',
            'https://www.udemy.com/python-best-practices/',
            'https://www.udemy.com/complete-python-bootcamp/',
            'https://www.udemy.com/ionic-from-web-to-mobile/',
            'https://www.udemy.com/ionic-framework-jumpstart/',
            'https://www.udemy.com/java-programming-for-humans/',
            'https://www.udemy.com/java-an-introductory-course/',
            'https://www.udemy.com/plc-programming-from-scratch/',
            'https://www.udemy.com/python-2000-beyond-the-basics/',
            'https://www.udemy.com/learn-and-build-using-polymer/',
            'https://www.udemy.com/complete-ios-10-developer-course/',
            'https://www.udemy.com/introduction-to-java-programming/',
            'https://www.udemy.com/introduction-to-java-programming/',
            'https://www.udemy.com/python-gui-programming-solutions/',
            'https://www.udemy.com/ruby-on-rails-for-web-development/',
            'https://www.udemy.com/java-fundamentals-fast-and-simple/',
            'https://www.udemy.com/pythonic-python-part-i-the-basics/',
            'https://www.udemy.com/java-programming-the-master-course/',
            'https://www.udemy.com/learn-python-100-coding-challenges/',
            'https://www.udemy.com/introduction-typescript-development/'
            'https://www.udemy.com/java-essential-training-with-java-8/',
            'https://www.udemy.com/learn-python-programming-from-scratch/',
            'https://www.udemy.com/java-the-complete-java-developer-course/',
            'https://www.udemy.com/hybrid-mobile-app-development-with-ionic/',
            'https://www.udemy.com/build-apps-with-reactjs-the-complete-course/',
            'https://www.udemy.com/step-by-step-java-programming-complete-course/',
            'https://www.udemy.com/java-in-depth-become-a-complete-java-engineer/',
            'https://www.udemy.com/beginning-ionic-hybrid-application-development/',
            'https://www.udemy.com/getting-started-with-ionic-framework-and-parse/',
            'https://www.udemy.com/learning-python-for-data-analysis-and-visualization/',
            'https://www.udemy.com/ionic-2-rc0-kickstart-build-a-mobile-app-in-no-time/',
            'https://www.udemy.com/java-programming-from-zero-to-hero-the-complete-course/',
            'https://www.udemy.com/learn-java-se-8-and-prepare-for-the-java-associate-exam/',
            'https://www.udemy.com/php-for-complete-beginners-includes-msql-object-oriented/',
            'https://www.udemy.com/master-android-7-nougat-java-app-development-step-by-step/',
            'https://www.udemy.com/learn-python-in-3-days-the-best-python-training-in-3-days/',
            'https://www.udemy.com/pre-programming-everything-you-need-to-know-before-you-code/',
            'https://www.udemy.com/ionic-2-tutorial-course-learning-by-example-with-complete-apps/',
            'https://www.udemy.com/python-django-programming-beginner-to-advance-tutorial-step-by-step/',
            'https://www.udemy.com/learning-to-program-in-java-a-supplement-for-online-academic-learners/',
            ]

    def parse(self, response):
        course_title = response.css('h1.course-title::text').extract_first().strip()
        enrolled_information = response.css('span.rating-and-enrolled__element').extract()

        rating = [x.strip() for x in response.css('span.rate-count>span.tooltip-container::text').extract_first().strip().split("\n")]
        skill_level = response.css('div.right-middle>ul.list>li.list-item:nth-child(3)>span.list-right::text').extract_first()
        course_thumbnail = response.css('div.placeholder__thumbnail-container.play-button-trigger>img').extract_first()
        course_thumbnail = course_thumbnail[course_thumbnail.find('"')+1:].replace('">','').strip()

        course_description = response.css('div#desc').extract_first()
        course_description = re.sub(cleanr, '', course_description).replace("\n\n", '').replace("  ", ' ').strip()

        overall_rating = float(rating[0].replace(',', ''))
        ratings = float(rating[-1].replace('ratings)', '').replace('(','').replace(',','').strip())
        student_enrolled = re.sub(cleanr, '', enrolled_information[2].replace('students enrolled', '').strip()).strip()
        student_enrolled = int(student_enrolled.replace(',', ''))

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
                cover_image = course_thumbnail
                )
