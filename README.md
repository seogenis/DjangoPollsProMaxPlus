Welcome to Sean's first ever django web progamming project! My first time working with all concepts/tools using in this repo... Please be patient with me :pray:


This project features a poll system consisting of the following:

Pages:
- admin pages(polls/admin), with ability to modify questions and choices, using django default admin app template (templates/admin)
- poll questions overview, voting, and result pages
- web API pages, with ability to modify questions and choices
- pages in polls/views.py, html in polls/templates/polls, css in polls/static/polls

Database / Models:
- uses sqlite
- Question and Choice models (polls/models.py)

API / Serializers:
- QuestionSerializer and ChoiceSerializer inherits django's ModelSerializer class with built-in validation and other functions (polls/serializer.py)
- web API consists create, list, update, destroy, retrieve capabilities
- web API views in polls/views
