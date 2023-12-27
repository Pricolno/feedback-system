# Course feedback ranking system
Collecting feedback on university courses and ranking by preference


> @spbu_feedback_bot

> It was created on the basis of SPbU University, Faculty of Mathematics and Computer Science 

## Launching the application

To launch the application, you need to execute the command

```bash
docker-compose up --build
```

Сервер слушает на порту 5000. 

## About the product
> [The full presentation](https://github.com/Pricolno/feedback-system/tree/bot/doc/feedback-system.pdf)

### Independent Microservices

* Database
* Recommendation systems
* Async telegram bot


### Bot interface

Main menu
![](./img/1_hello.png)

Search for a course by title
![](./img/2_choose_course.png)

Action with the course
![](./img/3_work_with.png)

Student feedback
![](./img/4_feedback.png)

Course feedback
![](./img/5_text_feedback.png)

Course Metrics
![](./img/6_metrics_by_course.png)

Tag Search
![](./img/7_searchin_tags.png)

View tags
![](./img/8_watching_tags.png)

Getting relevant courses
![](./img/9_getting_relevant_courses.png)



### How do we get the tags?

 Tags are generated from the course text description

* Automatically download course descriptions
* How to generate tags from text?
    * ChatGPT
    * PLSA
    * Different neural networks
* Normalization

### Database architecture

![](./img/bd_archet.png)

### Scenario of bot operation

> without rate sistem
![](./img/without_rate__bot_scenaries.png)

> with rate sistem
![](./img/with_rate_bot_scenaries.png)

### Future

* Improve tag selection and normalization
* User authorization system
* Support for courses in other departments

---

> https://t.me/spbu_feedback_bot
