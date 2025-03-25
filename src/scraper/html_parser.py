from bs4 import BeautifulSoup

def extract_table_data(innerHTML: str) -> list:
    """
    Extrae datos de una tabla HTML
    
    Args:
        innerHTML: HTML de la tabla
    
    Returns:
        Lista con los datos extraídos
    """
    soup = BeautifulSoup(innerHTML, 'html.parser')
    cells = soup.find_all('div', attrs={'role': 'gridcell'})
    
    data = []
    for cell in cells[1:]:
        cell_text = cell.find('div', class_='pivotTableCellWrap')
        if cell_text:
            data.append(cell_text.text.strip())
        else:
            data.append(cell.text.strip())
    
    return data