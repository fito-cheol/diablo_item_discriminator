from difflib import SequenceMatcher
import json
import re


with open('data/item.json') as json_file:
    item_dict = json.load(json_file)
    
class Item:
  equipment = None # 부위
  power_level = None # 신성 선조
  quality = None # 등급 
  power = None # 위력
  options = []
  required_level = None # 요구 레벨
  character_class = None # 직업
  
  def __init__(self, texts) -> None:
    self.texts = texts
    self.set_equipment()
    self.set_power_level()
    self.set_quality()
    self.set_power()
    self.set_options()
    self.set_required_level()
    self.set_character_class()
  
  def __repr__(self) -> str:
    repr_string = ""
    repr_string += f"{self.power_level or '일반'} {self.quality or ''} {self.equipment  or ''} \n"
    repr_string += f"위력: {self.power} \n"
    
    option_string = ""
    for option in self.options:
     option_string += str(option) + "\n"
    repr_string += f"{option_string}"
    
    repr_string += f"레벨 제한: {self.required_level} \n"
    repr_string += f"직업 제한: {self.character_class} \n"
    
    return repr_string
  
  def set_equipment(self):
    for text in self.texts:
      text = text.strip()
      for search_key in item_dict['equipment']:
        if search_key in text:
          self.equipment = search_key
          return
  
  def set_power_level(self):
    for text in self.texts:
      text = text.strip()
      for search_key in item_dict['power_level']:
        if search_key in text:
          self.power_level = search_key
          return
  
  def set_quality(self):
    for text in self.texts:
      text = text.strip()
      for search_key in item_dict['quality']:
        if search_key in text:
          self.quality = search_key
          return
        
  def set_options(self):
    for index, text in enumerate(self.texts):
      text = text.strip()
      for search_key in item_dict['option']:
        aff_key = search_key[:18]
        ratio = SequenceMatcher(None, text[:len(aff_key)], aff_key).ratio()
        if ratio < 0.95:
          continue
        next_line = self.texts[index + 1].strip()
        use_two_line = "]" in next_line and not "]" in text
        if use_two_line:
          self.options.append(Option(text=text + next_line, search_key=search_key))
        else:
          self.options.append(Option(text=text, search_key=search_key))
          
  def set_power(self):
    for text in self.texts:
      text = text.strip()
      for search_key in item_dict['power']:
        if search_key in text:
          self.power = get_numbers_from_string(text)[0]
          return
          
  def set_required_level(self):
    for text in self.texts:
      text = text.strip()
      for search_key in item_dict['required_level']:
        if search_key in text:
          self.required_level = get_numbers_from_string(text)[0]
          return
          
  def set_character_class(self):
    for text in self.texts:
      text = text.strip()
      for search_key in item_dict['character_class']:
        if search_key in text:
          self.character_class = search_key
          return
  
class Option:
  grade = None
  text = None
  search_key = None
  def __init__(self, text, search_key) -> None:
    self.text = text
    self.search_key = search_key
    self.set_grade()
    
  def __str__(self) -> str:
    if self.grade:
      return self.search_key + f", 등급: {self.grade}"  
    return self.text
  
  def __repr__(self) -> str:
    if self.grade:
      return self.search_key + f", 등급: {self.grade}"  
    return self.text
  
  def is_good(self):
    return self.grade == '상'
  
  def is_bad(self):
    return self.grade == '하'
  
  def set_grade(self):
    if not "[" in self.text or not "]" in self.text:
      return
    
    numbers = get_numbers_from_string(self.text)
    
    if len(numbers) == 2:
      self.grade = '상'
    elif len(numbers) == 3:
      value, min, max = [float(number) for number in numbers]
      good_criteria =  min + (max - min) * 0.8
      average = (min + max) /2
      
      if value >= good_criteria:
        self.grade = '상'
      elif value >= average:
        self.grade = '중'
      else:
        self.grade = '하'
    else:
      return
    
class ItemCrieria:
  equipment = None # 부위
  power_level = None # 신성 선조
  quality = None # 등급 
  power = None # 위력
  options = [] 
  required_level = None # 요구 레벨
  character_class = None # 직업
  


def get_numbers_from_string(string):
    numbers = re.findall(r'\d+\.\d+|\d+', string)
    return numbers

def get_similar_text_in_list(text, string_list):
  for compare_string in string_list:
    
    similarity = SequenceMatcher(None, text, compare_string).ratio()
    if similarity > 0.8:
      return compare_string
  return None    

if __name__ == "__main__":
  with open('data/item_text_sample_2.txt', 'r', encoding='utf-8') as f:
    item_text_sample = f.readlines()
  item_instance = Item(item_text_sample)
  print(item_instance)
  
  
  



