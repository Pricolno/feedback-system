import os, sys
# add ranking directory to sys.path
sys.path.append(os.path.dirname(__file__))


from typing import Callable, Union, List, Tuple, Dict
from struct_data.aliases import TagId, TagTitle, CourseShortName, ChatBotId

from struct_data.tag import Tag
# from struct_data.context import Context
from struct_data.user import User
from struct_data.course import Course

from simple_data.simpleCourses import simple_courses
from simple_data.simpleUsers import simple_users
from simple_data.simpleTags import simple_tags

from model_text_to_tags.chatGPT.chatGPT import ChatGPT


# algorithms
import Levenshtein # distance


class RankingSystem:
    # В целом, нам нужен будет только один запрос 
    # весь context от user и course  
    # Поэтому, в будущем нужно будет кешировать запрос к курсам 

    def __init__(self, users : Dict[ChatBotId, User] = None,
                  courses : Dict[CourseShortName, Course] = None,
                  tags : Dict[TagTitle, Tag] = None) -> None:
        self.users :  Dict[ChatBotId, User] = users
        self.courses : Dict[CourseShortName, Course] = courses
        self.tags : Dict[TagTitle, Tag] = tags

        # sync data
        self.update_courses()
        self.update_tags()
        self.update_users()

        
    # COURSES
    def _get_simple_courses(self):
        return simple_courses

    def update_courses(self):
        # обращение к базе данных
        # нужно получить Dict[ShortNameCourse, Course]
        
        # change on request to BD
        # try except
        self.courses = self._get_simple_courses()

    def _get_courses(self) -> Dict[CourseShortName, Course]:
        return self.courses
    
    def _print_courses(self):
        print("[\ course]")
        for course in self.courses:
            print(course)
        print("[course /]")

    # __COURSES

    # USERS
    def _get_simple_users(self):
        return simple_users

    def update_users(self):
        # change on request to BD
        # try except
        self.users = self._get_simple_users()

    def _get_users(self) -> List[User]:
        return self.users
    
    def _print_users(self):
        print("[\ users]")
        for _, user in self.users.items():
            print(user)
        print("[users /]")

    # __USERS

    # TAGS
    def _get_simple_tags(self):
        return simple_tags

    def update_tags(self):
        # change on request to BD
        # try except
        self.tags = self._get_simple_tags()
    
    def _get_tags(self) -> Dict[TagTitle, Tag]:
        return self.tags

    def _print_tags(self):
        print("[\ tags]")
        for tag_title in self.tags:
            print(self.tags[tag_title])
        print("[tags /]")
    
    # __TAGS

    # TOP_MATH
    def _calc_distance_between_user_and_course(self, user : User, course : Course):
        distance = 0
        for tag_title in user.context:
            if tag_title in course.context:
                distance += 1

        return distance
    
    def get_top_relevant_UserCourse(self, chat_bot_id: ChatBotId, max_count : int = 10):
        if chat_bot_id not in self.users:
            print(f"Такого юзера={chat_bot_id} нету в базе данных!")
            self.update_users()

            if chat_bot_id not in self.users:
                print(f"!!Такого юзера={chat_bot_id} нету в базе данных после обновления!!!!!!")
                return None, None
        
        user = self.users[chat_bot_id]

        list_distCourse = self._get_top_relevant_UserCourse(user=user, max_count=max_count)
        return list_distCourse
        

    def _get_top_relevant_UserCourse(self, user: User, max_count : int = 10):
        list_dist_and_course = []
        for course_short_name, course in self.courses.items():
            distance = self._calc_distance_between_user_and_course(user, course)
            list_dist_and_course.append((distance, course))
        
        list_dist_and_course = sorted(list_dist_and_course, key=lambda x: x[0], reverse=True)

        result_count = min(max_count, len(list_dist_and_course))
        result = list_dist_and_course[:result_count]

        return  [res[1] for res in result], [res[0] for res in result]

    # __TOP_MATH

    # TOP_TAGS_FOR_SNIPPET 
    ## DEFINE_DISTANCE
    @staticmethod
    def _levenshtain_distance(s1 : str, s2 : str) -> int:
        """
        distance: 0 - s1 and s2 is same
        distance: 100 - s1 and s2 is different
        """
        return Levenshtein.distance(s1, s2)

    @staticmethod
    def _inv_levenshtain_ratio(s1 : str, s2 : str) -> float:
        """
        Calculates a normalized indel similarity in the range [0, 1]. 1 - (1 - normalized_distance)
        ratio: 0 - s1 and s2 is same
        ratio: 1 - s1 and s2 is different
        """
        
        return 1. - Levenshtein.ratio(s1, s2)
    ## __DEFINE_DISTANCE
    
    ## TAG_TEXT_TO_TAG
    def get_top_suitable_tags_by_text(self, tag_req : str,
                                       metric_func : Callable[[str, str], Union[int, float]] = _levenshtain_distance,
                                       max_count : int = 20) -> Tuple[List[Tag], List[Union[int, float]]] :
        
        metric_and_tag_list = []

        for tag_title in self.tags:
            metric = metric_func(tag_req, self.tags[tag_title].title)
            metric_and_tag_list.append((metric, self.tags[tag_title]))

        metric_and_tag_list = sorted(metric_and_tag_list, key=lambda x: x[0], reverse=False)
        
        result_count = min(max_count, len(metric_and_tag_list))
        result = metric_and_tag_list[:result_count]

        return [res[1] for res in result], [res[0] for res in result]
    ## __TAG_TEXT_TO_TAG

    ## COURSE_TEXT_TO_COURSE
    def get_top_suitable_courses_by_text(self, course_req : str,
                                          metric_func : Callable[[str, str], Union[int, float]] = _levenshtain_distance,
                                          max_count : int = 20) -> Tuple[List[Course], List[Union[int, float]]] :
        
        metric_and_course_list = []

        for course_short_name, course in self.courses.items():
            metric = metric_func(course_req, course.full_name)
            metric_and_course_list.append((metric, course))

        metric_and_course_list = sorted(metric_and_course_list, key=lambda x: x[0], reverse=False)
        
        result_count = min(max_count, len(metric_and_course_list))
        result = metric_and_course_list[:result_count]

        return [res[1] for res in result], [res[0] for res in result]
    ## __COURSE_TEXT_TO_COURSE

    ## OFFER_TAGS_WITHOUT_USER_TEXT
    def get_top_suitable_tags_by_context(self, user : User, 
                                         count : int = 20) -> Tuple[List[Tag], List[Union[int, float]]]:
        # TODO
 
        pass

    ## __OFFER_TAGS_WITHOUT_USER_TEXT
    # __TOP_TAGS_FOR_SNIPPET

    # GET_TAGS_FOR_COURSES
    # @staticmethod
    # def _get_courses_tags() -> Dict[]

    @staticmethod
    def _get_all_tags(model_name: str = "ChatGPT") -> Dict[TagTitle, Tag]:
        model = None
        if model_name == "ChatGPT":
            model = ChatGPT()
        
        all_tags = model.load_all_tags()

        return all_tags
    
    @staticmethod
    def _get_all_courses(model_name: str = "ChatGPT") -> List[Course]:
        model = None
        if model_name == "ChatGPT":
            model = ChatGPT()
        
        courses_list = model.read_all_courses_json_to_courses()

        return courses_list

    # __GET_TAGS_FOR_COURSES