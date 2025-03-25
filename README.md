# PowerBI Scraper

Este proyecto implementa un scraper para extraer datos de dashboards de PowerBI.

## Instalación

```bash
git clone https://github.com/nickmend/powerbi-crawler.git
cd powerbi-scraper
pip install -r requirements.txt
```

## Uso

```python
from src.scraper.powerbi_scraper import PowerBIScraper

scraper = PowerBIScraper()
scraper.initialize_driver()
df = scraper.scrape_table()
scraper.save_data(df, "datos_powerbi.csv")
scraper.cleanup()
```

## Estructura del Proyecto

- `src/`: Código fuente del proyecto
- `data/`: Datos raw y procesados
- `notebooks/`: Jupyter notebooks para desarrollo y ejemplos
- `tests/`: Tests unitarios
- `config/`: Archivos de configuración
