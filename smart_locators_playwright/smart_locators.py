from playwright.sync_api._generated import Locator
from smart_locators_playwright import custom_exceptions
from playwright.sync_api._generated import Page as sync_page
from playwright.async_api._generated import Page as async_page
import logging,re,os,json
from pathlib import Path

class SmartLocators:
    def __init__(self, page:sync_page or async_page):
        """Initializes an instance of the Smart Locators class.

        Args:
            page (playwright.sync_api.Page or playwright.async_api.Page): The Playwright "page" instance used to interact with the browser."""

        self._page=page
        self._playwright_allowed_locators=["alt","label","placeholder","role","text","title"]
        self._custom_locators=["css","xpath"]
        self._cwd = os.getcwd()
        self._locators_file = f"{self._cwd}/SmartLocatorsLogs/default.json"
    
       
    def find(self,id:str=None, name:str=None, css:str=None, xpath:str=None, label:str=None, alt:str=None, placeholder:str=None, role:str=None, text:str=None, title:str=None,first_match:bool=True,element_name:str="",locator_update:bool=False,locators_file:str="",**kwargs)->Locator:
        """Finds the web element using provided locators. Tries locators in order until one succeeds.

        Args:
            id (str, optional): ID attribute. Defaults to None.
            name (str, optional): Name attribute. Defaults to None.
            css (str, optional): CSS selector. Defaults to None.
            xpath (str, optional): XPATH selector. Defaults to None.
            label (str, optional): Label attribute. Defaults to None.
            alt (str, optional): Alt attribute. Defaults to None.
            placeholder (str, optional): Placeholder attribute. Defaults to None.
            role (str, optional): Role attribute. Defaults to None.
            text (str, optional): Text content. Defaults to None.
            title (str, optional): Title attribute. Defaults to None.
            first_match (bool, optional): Returns first matching elements if True else returns all matching elements. Defaults to True
            **kwargs: Additional attributes and values if needed.
            
        Returns:
            Locator: The found web element. 
            List of locators if multiple elements are found and first_match is set to False
        
        Raises:
            NoSuchElementException: If no element is found for any of the given locators.
        """
        _locator_strategies_default={"id":id,"name":name,"css":css,"xpath":xpath,"label":label,"alt":alt,"placeholder":placeholder,"role":role,"text":text,"title":title}
        _locator_strategies={**_locator_strategies_default,**kwargs}
        _non_empty_locators={key:value for key,value in _locator_strategies.items() if value not in (None,"")}
        self.__reformat_locator(_non_empty_locators)
        _playwright_method_mappings={key:f'_get_by_{key}' for key,value in _non_empty_locators.items() if key.lower() in self._playwright_allowed_locators}
        _custom_method_mappings={key:f'_get_by_locator' for key,value in _non_empty_locators.items() if key.lower() not in self._playwright_allowed_locators}
        
        _locator_mappings={**_playwright_method_mappings,**_custom_method_mappings}
        ele=self.__find_element_internal(locators=_non_empty_locators,mappings=_locator_mappings)
        if ele:
            if locator_update:
                locators_file = self._locators_file if locators_file=="" else locators_file
                update_status = self.update_locators(element_name,ele.nth(0),locators_file)
                logging.info(f"Locator entry is updated for {element_name} in {locators_file} file. Refer the file for details")
            return ele.nth(0) if first_match else ele
        else:
            raise custom_exceptions.NoSuchElementException
        
    def __find_element_internal(self,locators:dict,mappings:dict,keys:list=None,index:int=0)->Locator:
        """
        Recursively attempts to find an element using a series of locators and their corresponding mapping methods.
        Args:
            locators (dict): A dictionary containing locator types as keys and their corresponding values.
            mappings (dict): A dictionary mapping locator types to method names that handle those locators.
            keys (list, optional): A list of locator key-value pairs. Defaults to None, in which case it is initialized from `locators`.
            index (int, optional): The current index in the `keys` list to process. Defaults to 0.
        Returns:
            Locator: The located element if found, otherwise False.
        """
        # If the method is called first time, initialize 'keys' as a list of key-value pairs (in tuple format) from locators
        if keys is None:
            keys=list(locators.items())
        
        # Base case: If index exceeds the length of keys, return False (element not found)
        if index>=len(keys):
            return False
        
        # Get the current locator type and value from the keys list (unpacking tuple with index)
        locator_type,value=keys[index]
        
        # Retrieve the method name from the mappings dictionary for the current locator type
        method=mappings.get(locator_type)
        
        # Dynamically call the method using getattr and pass the locator value as an argument
        result=getattr(self,method)(value)
        
        # If the result is valid (element found), return it
        # Otherwise, recursively call the function with the next index
        return result if result else self.__find_element_internal(locators,mappings,keys,index+1)   

    def __reformat_locator(self,locators:dict)->None:
        """Generate an XPath for attributes that do not have a native Playwright method. Otherwise, leave the locator unchanged.

        Args:
            locators (dict): A dictionary containing all locators.
        """
        for key,value in locators.items():
            if key.lower() not in self._playwright_allowed_locators and key.lower() not in self._custom_locators:
                if key.lower()=="element_name" or key.lower()=="locators_file":
                    continue
                locators[key]=(f"//*[@{key}='{value}']")
    
    def _get_by_role(self,locator):
        try:
            ele=self._page.get_by_role(locator)
            return ele if ele.count()>0 else False
        except Exception as e:
            return False
        
    def _get_by_alt(self,locator):
        try:
            ele=self._page.get_by_alt_text(locator)
            return ele if ele.count()>0 else False
        except Exception as e:
            return False
    
    def _get_by_label(self,locator):
        try:
            ele=self._page.get_by_label(locator)
            return ele if ele.count()>0 else False
        except Exception as e:
            return False
    
    def _get_by_placeholder(self,locator):
        try:
            ele=self._page.get_by_placeholder(locator)
            return ele if ele.count()>0 else False
        except Exception as e:
            return False
    
    def _get_by_text(self,locator):
        try:
            ele=self._page.get_by_text(locator)
            return ele if ele.count()>0 else False
        except Exception as e:
            return False
        
    def _get_by_title(self,locator):
        try:
            ele=self._page.get_by_title(locator)
            return ele if ele.count()>0 else False
        except Exception as e:
            return False
        
    def _get_by_locator(self,locator):
        try:
            ele=self._page.locator(locator)
            return ele if ele.count()>0 else False
        except Exception as e:
            return False

    def update_locators(self,element_name:str="",webelement:Locator=None,locators_file:str="")->bool:
        locators_file = self._locators_file if locators_file=="" else locators_file
        if webelement!="":
            outerHTML=webelement.evaluate("el => el.outerHTML")
            attributes=self.extract_html_attributes(outerHTML)
            status:bool=self.write_locators_to_json(element_name,attributes,locators_file)
            return status
        else:
            logging.debug("Supplied locator is empty, skipping locator collection...")
            return False

    def extract_html_attributes(self,html_string: str) -> dict:
        pattern = r'(\w+(?:-\w+)*)\s*=\s*"([^"]*)"'
        matches = re.findall(pattern, html_string)
        attributes_dict = {key: value for key, value in matches}
        return attributes_dict

    def write_locators_to_json(self, element_name: str, attributes: dict, locators_file: str) -> bool:
        try:
            # validate inputs
            if not element_name or not element_name.strip():
                logging.debug("Element name not provided")
                return False
            if not attributes or not isinstance(attributes, dict):
                logging.debug(f"Invalid attributes for {element_name}")
                return False
            file_path = Path(locators_file)
            is_file=str(file_path).endswith(".json")
            if not is_file:
                file_path = f"{str(file_path)}/default.json"
                file_path = Path(file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            if file_path.exists():
                with open(file_path, "r", encoding="utf-8") as f:
                    locators_data = json.load(f)
                logging.debug(f"Loaded existing locators from {file_path}")
            else:
                locators_data = {}
                logging.debug(f"Creating new locator file at {file_path}")
            locators_data[element_name] = attributes
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(locators_data, f, indent=2, ensure_ascii=False)
            logging.debug(f"Updated locator '{element_name}' with {len(attributes)} attributes")
            return True
        except Exception as e:
            logging.debug(f"Failed to write locators: {str(e)}")
            return False