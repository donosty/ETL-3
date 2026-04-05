import logging
from extractors.earthquake_extractor import EarthquakeExtractor
from transformers.cleaner import EarthquakerTransformer
from transformers.validator import DataValidator
from database.loader import DataLoader
from sqlalchemy import create_engine
import os

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def main():
    try:
        engine = create_engine(os.getenv("DATABASE_URL"))
        extractor = EarthquakeExtractor()
        loader = DataLoader(engine)
        
        raw_data = extractor.get_last_24h_earthquakes()
        if not raw_data:
            logger.error("No se obtuvieron datos. Abortando pipeline")
            return
        
        df = EarthquakerTransformer.process_geojson(raw_data)
        
        df_clean = DataValidator.clean_and_validate(df)
        
        if not df_clean.empty:
            loader.upsert_data(df_clean)
        else:
            logger.warning("No hay datos validos para cargar")
            
    except Exception as e:
        logger.critical(f"Fallo Critico del Pipeline {e}")
        
if __name__ == '__main__':
    main()