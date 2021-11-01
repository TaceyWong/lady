"""Main module."""

import os
import html2text
from typing import Union,List,Dict
from datetime import datetime
from jinja2 import PackageLoader,Environment, FileSystemLoader,Template

TD_Left_To_Right = "ltr"
TD_Right_To_Left = "rtl"

class Columns:
    """contains meta-data for the different columns"""

    def __init__(self) -> None:
        self.custom_width = dict()
        self.custom_alignment = dict()

class Table:
    """an table where you can put data (pricing grid, a bill, and so on)"""
    def __init__(self) -> None:
        self.data = [[]]
        self.columns = Columns()

class Button:
    def __init__(self,color:str,text:str,link:str,text_color:str=None) -> None:
        self.color = color
        self.text_color = text_color
        self.text = text
        self.link = link

class Action:

    def __init__(self,instruction:str,button:Button,invite_code:str=None) -> None:
        self.instructions = instruction
        self.button = button
        self.invite_code = invite_code


class Theme:
    
    def __init__(self,name:str,html_path:str=None,html_template:str=None,
    plaintext_template:str=None,plaintext_path:str=None) -> None:
        self.name = ""
        self.html_template = html_template
        self.plaintext_template = plaintext_template
        self.html_path = html_path
        self.plaintext_path = plaintext_path
    def __verify(self):
        if self.html_template and not self.html_path:
            raise Exception("html_template and html_path must have one")


# class Template:

#     def __init__(self) -> None:
#         self.lady = Lady()
#         self.email = Email()
    
class Product:
    def __init__(self,name:str,link:str,logo:str=None,copyright:str=None,
    trouble_text:str=None) -> None:
        self.name = name
        self.link = link
        self.logo = ""
        self.copyright = ""
        self.trouble_text = ""


        

class Email:

    def __init__(self,name:str,intro:Union[str,list],action:Union[Action,List[Action]],dictionary:Dict[str,str]=None,table:Union[Table,List[Table]]=None,
    outro:Union[str,list]=None,greeting:str=None,signature:str=None,title:str=None,
    text_direction:str=TD_Left_To_Right) -> None:
        self.name = name # The name of the contacted person
        self.intro = intro # Intro sentences, first displayed in the email
        self.dictionary =dictionary # A list of key+value (useful for displaying parameters/settings/personal info)
        self.table = table
        self.action = action 
        self.outro = outro
        self.greeting = greeting
        self.signature = signature
        self.title = title
        self.text_direction = ""
        
        
class Lady:

    def __init__(self,theme:Union[str,Theme]=None,product:Product=None,text_direction:str=TD_Left_To_Right) -> None:
        self.theme = theme
        self.product = product
        self.text_direction = ""
        self.disable_css_inlining = False
        self.cache_html_template = None
        self.cache_plaintext_template = None
        # No product?
        if not self.product or not isinstance(self.product,Product):
            raise Exception("Please provide the `product` object.")

        #No product name or link?
        if (not self.product.name) or (not self.product.link):
            raise Exception("Please provide the product name and link.") 
        self.text_direction = text_direction
        self.product.copyright = self.product.copyright or \
        '&copy; ' +  str(datetime.now().year) + ' <a href="' + self.product.link + '" target="_blank">' + self.product.name + '</a>. All rights reserved.'
        self.__cache_themes()
        
    
    def generate_html(self,email:Email)->str:
        email = self.__parse_params(email)
        print(email.__dict__)
        return self.cache_html_template.render(email=email,lady=self)

    def generate_plaintext(self,email:Email)->str:
        pass
        #  html2text.html2text
    
    def __generate_template(self,email:Email,tpl:str)->str:
        return ""

    def __parse_params(self,email:Email)->dict:
        """Validates, parses and returns injectable ejs parameters"""
        # Basic params validation
        if not email or not isinstance(email,Email):
            raise Exception("Please provide parameters for generating transactional e-mails.'")
        
        # Pass text direction to template
        email.text_direction =  email.text_direction or  self.text_direction
        
        # Support for custom greeting/signature (fallback to sensible defaults)
        email.greeting = email.greeting or "Hi"
        
        # Only set signature if signature is not false
        if email.signature != "FALSE":
            email.signature = email.signature or  "Yours truly"
        #  Use `greeting` and `name` for title if not set
        if not email.title:
            email.title = (email.greeting + ' ' + email.name  if email.name else email.greeting)+","

        #  Convert intro, outro, and action to arrays if a string or object is used instead
        email.intro = self.__convert_to_list(email.intro)
        email.outro = self.__convert_to_list(email.outro)
        email.action = self.__convert_to_list(email.action)
        email.table = self.__convert_to_list(email.table)
        return email

    @staticmethod
    def __convert_to_list(data:Union[str,list]):
        if not isinstance(data,list):
            data = [data]
        return data

    def __cache_themes(self)->None:
        """Build path to theme file (make it possible to pass in a custom theme path, fallback to mailgen-bundled theme)"""
        if isinstance(self.theme,Theme) and (self.theme.html_path or self.theme.html_template):
            if self.theme.html_path:
                with open(self.theme.html_path) as t:
                    self.cache_html_template = Template(t.read())
            else:
                self.cache_html_template = Template(self.theme.html_template)
            if self.theme.plaintext_path:
                with open(self.theme.plaintext_path) as t:
                    self.cache_plaintext_template = Template(t.read())
            elif self.theme.plaintext_template:
                self.cache_plaintext_template = Template(self.theme.plaintext_template)
        else: # from built-in of Lady
            if isinstance(self.theme,Theme):
                self.theme = self.theme.name
            env = Environment(loader=PackageLoader('lady','themes'))
            self.cache_html_template= env.get_template(f"{self.theme}/index.html")
            self.cache_plaintext_template=env.get_template(f"{self.theme}/index.txt")
    
        

if __name__ == "__main__":
    lady = Lady(theme=Theme(name="xxxx",html_path="themes/default/index.txt"),
                product=Product(name="测试产品",link="http://www.baidu.com"))
    email = Email(name="Tacey Wong",
                  intro="测试intro",
                  action=Action(instruction="测试Action",
                   button=Button(
                       text="按钮",link="http://www.qq.com",color="#ff0000"
                   )),
                   outro="测试outro",
                   dictionary={"name":"王信用"})
    print(lady.generate_html(email))
    