import pandas as pd
from typing import Dict, List, Optional, Union
import logging

class ExcelLoader:
    """Loader untuk file Excel dengan berbagai format dan sheet"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def load_sheet(self, file_path: str, sheet_name: Optional[str] = None) -> pd.DataFrame:
        """Load single sheet dari Excel"""
        try:
            return pd.read_excel(file_path, sheet_name=sheet_name)
        except Exception as e:
            self.logger.error(f"Error loading sheet {sheet_name} from {file_path}: {e}")
            return pd.DataFrame()
    
    def load_all_sheets(self, file_path: str) -> Dict[str, pd.DataFrame]:
        """Load semua sheet dari Excel"""
        try:
            return pd.read_excel(file_path, sheet_name=None)
        except Exception as e:
            self.logger.error(f"Error loading all sheets from {file_path}: {e}")
            return {}
    
    def get_sheet_names(self, file_path: str) -> List[str]:
        """Dapatkan nama semua sheet"""
        try:
            excel_file = pd.ExcelFile(file_path)
            return excel_file.sheet_names
        except Exception as e:
            self.logger.error(f"Error getting sheet names from {file_path}: {e}")
            return []
    
    def load_with_options(self, file_path: str, **kwargs) -> pd.DataFrame:
        """Load Excel dengan opsi custom"""
        try:
            return pd.read_excel(file_path, **kwargs)
        except Exception as e:
            self.logger.error(f"Error loading Excel with options from {file_path}: {e}")
            return pd.DataFrame()
    
    def export_to_excel(self, data: Union[pd.DataFrame, Dict[str, pd.DataFrame]], 
                       output_path: str) -> bool:
        """Export data ke Excel"""
        try:
            if isinstance(data, pd.DataFrame):
                data.to_excel(output_path, index=False)
            elif isinstance(data, dict):
                with pd.ExcelWriter(output_path) as writer:
                    for sheet_name, df in data.items():
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
            return True
        except Exception as e:
            self.logger.error(f"Error exporting to Excel {output_path}: {e}")
            return False