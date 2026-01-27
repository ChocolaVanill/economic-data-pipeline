"""Data quality validation checks"""
# Import libraries
import pandas as pd
from src.utils.logger import get_logger


logger = get_logger(__name__)


class DataQualityValidator:
    """Validates data quality across pipeline layers"""
    def __init__(self, df: pd.DataFrame, dataset_name: str):
        self.df = df
        self.dataset_name = dataset_name
        self.issues = []

    def check_nulls(self, columns: list, threshold: float = 0.05) -> bool:
        """Check if null percentage exceeds threshold"""
        passed = True
        for col in columns:
            if col in self.df.columns:
                null_pct = self.df[col].isnull().mean()
                if null_pct > threshold:
                    self.issues.append(f"{col}: {null_pct:.1%} nulls (threshold: {threshold:.1%})")
                    passed = False
        return passed

    def check_duplicates(self, subset: list) -> bool:
        """Check for duplicate records"""
        dup_count = self.df.duplicated(subset=subset).sum()
        if dup_count > 0:
            self.issues.append(f"Found {dup_count} duplicate rows on {subset}")
            return False
        return True
    
    def check_date_range(self, date_col: str, min_date: str = None, max_date: str = None) -> bool:
        """Check if dates fall within expected range"""
        passed = True
        dates = pd.to_datetime(self.df[date_col])

        if min_date and dates.min() < pd.to_datetime(min_date):
            self.issues.append(f"Date below minimum: {dates.min()} < {min_date}")
            passed = False
        if max_date and dates.max() > pd.to_datetime(max_date):
            self.issues.append(f"Date above maximum: {dates.max()} > {max_date}")
            passed = False
        return passed

    def check_value_range(self, col: str, min_val: float = None, max_val: float = None) -> bool:
        """Check if values fall within expected range"""
        passed = True
        if min_val is not None and self.df[col].min() < min_val:
            self.issues.append(f"{col} below minimum: {self.df[col].min()} < {min_val}")
            passed = False
        if max_val is not None and self.df[col].max() > max_val:
            self.issues.append(f"{col} above maximum: {self.df[col].max()} > {max_val}")
            passed = False
        return passed

    def check_row_count(self, min_rows: int) -> bool:
        """Check if dataset has minimum required rows"""
        if len(self.df) < min_rows:
            self.issues.append(f"Row count {len(self.df)} below minimum {min_rows}")
            return False
        return True

    def report(self) -> dict:
        """Generate validation report"""
        result = {
            "dataset": self.dataset_name,
            "row_count": len(self.df),
            "passed": len(self.issues) == 0,
            "issues": self.issues
        }

        if result["passed"]:
            logger.info(f"🟢 {self.dataset_name}: All quality checks passed")
        else:
            logger.warning(f"⚠️ {self.dataset_name}: {len(self.issues)} issue(s) found")
            for issue in self.issues:
                logger.warning(f"   - {issue}")
            return result

        return result


# Pre-built validators for each dataset
def validate_gdp(df: pd.DataFrame) -> dict:
    v = DataQualityValidator(df, "GDP")
    v.check_nulls(['trend_date', 'gdp_value'])
    v.check_duplicates(['trend_date'])
    v.check_value_range('gdp_value', min_val=0)
    v.check_row_count(min_rows=10)
    return v.report()


def validate_cpi(df: pd.DataFrame) -> dict:
    v = DataQualityValidator(df, "CPI")
    v.check_nulls(['date', 'value', 'category'], threshold=0.10)
    v.check_duplicates(['date', 'category'])
    v.check_value_range('value', min_val=0)
    return v.report()


def validate_labour(df: pd.DataFrame) -> dict:
    v = DataQualityValidator(df, "Labour")
    v.check_nulls(['date', 'metric', 'value'])
    v.check_duplicates(['date', 'metric'])
    return v.report()


def validate_exchange_rates(df: pd.DataFrame) -> dict:
    v = DataQualityValidator(df, "Exchange Rates")
    v.check_nulls(['date', 'currency_code', 'rate'])
    v.check_duplicates(['date', 'currency_code'])
    v.check_value_range('rate', min_val=0)
    return v.report()

    
def validate_population(df: pd.DataFrame) -> dict:
    v = DataQualityValidator(df, "Population")
    v.check_nulls(['date', 'population'])
    v.check_value_range('population', min_val=0)
    return v.report()