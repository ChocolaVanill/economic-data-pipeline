"""Unit tests for data quality validators"""
# Import libraries
import pandas as pd

class TestDataValidators:
    """Tests for data quality validators"""
    def test_validator_detects_nulls(self):
        """Test null detection"""
        from src.quality.validators import DataQualityValidator

        df = pd.DataFrame({
            'date': ['2024-01', None, '2024-03'],
            'value': [100, 200, 300]
        })
        v = DataQualityValidator(df, "Test")
        passed = v.check_nulls(['date'], threshold=0.1)

        assert passed is False
        assert len(v.issues) == 1

    def test_validator_detects_duplicates(self):
        """Test duplicate detection"""
        from src.quality.validators import DataQualityValidator

        df = pd.DataFrame({
            'date': ['2024-01', '2024-01', '2024-02'],
            'series': ['abs', 'abs', 'abs']
        })
        v = DataQualityValidator(df, "Test")
        passed = v.check_duplicates(['date', 'series'])

        assert passed is False
        assert 'duplicate' in v.issues[0].lower()

    def test_validator_passes_clean_data(self):
        """Test validator passes with clean data"""
        from src.quality.validators import DataQualityValidator

        df = pd.DataFrame({
            'date': ['2024-01', '2024-02', '2024-03'],
            'value': [100, 200, 300]
        })
        v = DataQualityValidator(df, "Test")
        v.check_nulls(['date', 'value'])
        v.check_row_count(min_rows=2)
        result = v.report()

        assert result['passed'] is True
        assert len(result['issues']) == 0
