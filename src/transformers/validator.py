import pandas as pd
import logging

logger = logging.getLogger(__name__)

class DataValidator:
    @staticmethod
    def clean_and_validate(df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
        
        required_cols = ['id', 'place', 'mag', 'time', 'updated', 'longitude', 'latitude', 'depth']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise KeyError(f"Error de esquema: Faltan las columnas {missing_cols}")
        
        initial_count = len(df)
        
        df = df.dropna(subset=['id','place'])
        df = df.drop_duplicates(subset=['id'])
        
        df = df[(df['magnitude'] >= 0) & (df['magnitude'] <= 10)]
        df = df[(df['latitude'] >= -90) & (df['latitude'] <= 90)]
        df = df[(df['longitude'] >= -180) & (df['longitude'] <= 180)]
        
        df['depth'] = df['depth'].fillna(0)
        
        final_count = len(df)
        if final_count < initial_count:
            logger.warning(f"Validacion: Se eliminaron {initial_count - final_count} registros invalidos")
            
        return df