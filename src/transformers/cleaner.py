import pandas as pd
import logging

logger = logging.getLogger(__name__)

class EarthquakerTransformer:
    @staticmethod
    def process_geojson(payload: dict) -> pd.DataFrame:
        if not payload or "features" not in payload:
            return pd.DataFrame()
        
        features = payload["features"]
        
        df_props = pd.DataFrame([f['properties'] for f in features])
        
        df_props['id'] = [f["id"] for f in features]
        
        coords = [f['geometry']['coordinates'] for f in features]
        df_coords = pd.DataFrame(coords, columns=['longitude','latitude','depth'])
        
        final_df = pd.concat([df_props, df_coords], axis=1)
        
        columns_to_keep = ['id', 'place', 'mag', 'time', 'updated', 'longitude', 'latitude', 'depth']
        final_df = final_df[columns_to_keep]
        
        final_df = final_df.rename(columns={
            'mag':'magnitude',
            'time':'time_epoch',
            'updated':'updated_epoch'
        })
        
        logger.info(f"Datos transformados y aplanados: {final_df.shape[0]} filas")
        
        return final_df