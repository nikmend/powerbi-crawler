from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from typing import Tuple, Optional, Dict
import logging

logger = logging.getLogger(__name__)

def get_relative_xpath(element: WebElement) -> str:
    """
    Genera un XPath relativo para un elemento web.
    
    Args:
        element: Elemento WebElement de Selenium
    
    Returns:
        str: XPath relativo del elemento
    """
    try:
        # Obtener los atributos del elemento
        attributes = element.parent.execute_script("""
            var items = {};
            for (index = 0; index < arguments[0].attributes.length; ++index) {
                items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value
            };
            return items;
        """, element)
        
        # Construir XPath basado en atributos
        tag_name = element.tag_name
        xpath_parts = [f"//{tag_name}"]
        
        # Priorizar atributos más útiles para identificación
        priority_attrs = ['id', 'name', 'class', 'role', 'aria-label']
        for attr in priority_attrs:
            if attr in attributes:
                # Manejar clases múltiples
                if attr == 'class':
                    classes = attributes[attr].split()
                    xpath_parts.append(f"[contains(@class, '{classes[0]}')]")
                else:
                    xpath_parts.append(f"[@{attr}='{attributes[attr]}']")
                
        return "".join(xpath_parts)
    
    except Exception as e:
        logger.error(f"Error generando XPath relativo: {str(e)}")
        return ""

def get_element_attributes(driver, element: WebElement) -> Dict:
    """
    Obtiene todos los atributos computados de un elemento.
    
    Args:
        driver: Instancia del WebDriver
        element: Elemento WebElement
    
    Returns:
        Dict: Diccionario con los atributos computados
    """
    return driver.execute_script("""
        var items = {};
        var computedStyle = window.getComputedStyle(arguments[0]);
        for (var i = 0; i < computedStyle.length; i++) {
            var prop = computedStyle[i];
            items[prop] = computedStyle.getPropertyValue(prop);
        }
        return items;
    """, element)

def find_scrollable_parent(element: WebElement) -> Tuple[Optional[WebElement], Optional[str]]:
    """
    Encuentra el elemento padre más cercano que tiene capacidad de scroll.
    
    Args:
        element: Elemento WebElement inicial
    
    Returns:
        Tuple[Optional[WebElement], Optional[str]]: 
            - El elemento padre con scroll
            - El XPath del elemento encontrado
    """
    try:
        driver = element.parent
        current_element = element
        
        while current_element:
            # Obtener propiedades de overflow
            style = get_element_attributes(driver, current_element)
            overflow = style.get('overflow', 'visible')
            overflow_y = style.get('overflow-y', 'visible')
            
            # Verificar si el elemento tiene scroll
            has_scroll = (
                overflow in ['auto', 'scroll'] or 
                overflow_y in ['auto', 'scroll']
            )
            
            # Verificar si el elemento tiene contenido que puede hacer scroll
            scroll_height = driver.execute_script(
                "return arguments[0].scrollHeight > arguments[0].clientHeight;",
                current_element
            )
            
            if has_scroll and scroll_height:
                xpath = get_relative_xpath(current_element)
                logger.info(f"Elemento scrollable encontrado: {xpath}")
                return current_element, xpath
            
            # Obtener el elemento padre
            current_element = driver.execute_script(
                "return arguments[0].parentElement;",
                current_element
            )
        
        logger.warning("No se encontró elemento padre con scroll")
        return None, None
        
    except Exception as e:
        logger.error(f"Error buscando elemento scrollable: {str(e)}")
        return None, None

def scroll_element(driver, element: WebElement, amount: int =