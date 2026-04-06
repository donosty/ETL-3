import pandas as pd
import pytest
from src.transformers.validator import DataValidator

def test_validator_drops_invalid_magnitude():
    
    data = {
        'id': ['q1', 'q2'],
        'place': ['California', 'Chile'],
        'magnitude': [4.5, 12.0],  # El 12.0 debe ser eliminado
        'latitude': [34.0, -33.4],
        'longitude': [-118.2, -70.6],
        'depth': [10.0, 25.0],
        'time_epoch': [1712345678000, 1712345679000],
        'updated_epoch': [1712345678000, 1712345679000]
    }
    
    df_fake = pd.DataFrame(data)
    
    df_clean = DataValidator.clean_and_validate(df_fake)
    
    assert len(df_clean) == 1
    assert df_clean.iloc[0]['id'] == 'q1'
    
    
def test_validator_raises_error_on_missing_columns():
    data = {'id': ['q1'], 'place': ['Alaska']}
    df_incomplete = pd.DataFrame(data)
    
    with pytest.raises(KeyError) as excinfo:
        DataValidator.clean_and_validate(df_incomplete)
        
    assert "Error de esquema" in str(excinfo.value)