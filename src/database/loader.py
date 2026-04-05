from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError
from database.models import Earthquake
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class DataLoader:
    def __init__(self, engine):
        self.engine = engine
        
    def upsert_data(self, df: pd.DataFrame):
        """
        Realiza un 'UPSERT': Inserta si no existe, actualiza si existe.
        Esto previene errores de 'Unique Constraint' con el ID del sismo.
        """
        
        if df.empty:
            return
        
        records = df.to_dict(orient='records')
        
        try:
            with self.engine.begin() as conn:
                for record in records:
                    stmt = insert(Earthquake).values(record)
                    
                    stmt = stmt.on_conflict_do_update(
                        index_elements=['id'],
                        set_={
                            'magnitude': stmt.excluded.magnitude,
                            'place': stmt.excluded.place,
                            'updated_epoch': stmt.excluded.updated_epoch
                        }
                    )
                    conn.execute(stmt)
            logger.info(f'Insert completado: {len(records)} registros procesados')
        
        except SQLAlchemyError as e:
            logger.error(f"Error de base de datos: {e}")
            raise