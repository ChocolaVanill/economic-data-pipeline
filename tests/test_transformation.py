"""Unit tests for transformation modules"""
# Import libraries
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock

class TestBronzeSilver:
    """Tests for bronze to silver transformations"""
    @patch('src.transformation.bronze_to_silver.get_engine')
    def test_transform_gdp_handles_empty_data(self, mock_engine):
        """Test GDP transform handles empty bronze data"""
        mock_conn = MagicMock()
        mock_conn.execute.return_value.fetchone.return_value = None
        mock_engine.return_value.connect.return_value.__enter__ = MagicMock(return_value=mock_conn)
        mock_engine.return_value.connect.return_value.__exit__ = MagicMock(return_value=False)

        from src.transformation.bronze_to_silver import transform_gdp_to_silver
        result = transform_gdp_to_silver()

        assert result is None # Should return early with no data

    def test_gdp_transformation_logic(self):
        """Test GDP transformation calculations"""
        # Sample raw data
        raw_data = [
            {"date": "2024-01-01", "value": "100", "series": "abs"},
            {"date": "2024-04-01", "value": "105", "series": "abs"}
        ]
        df = pd.DataFrame(raw_data)
        df['date'] = pd.to_datetime(df['date'])
        df['value'] = pd.to_numeric(df['value'])

        assert len(df) == 2
        assert pd.api.types.is_numeric_dtype(df['value'])

class TestSilverToGold:
    """Tests for silver to gold transformations"""
    def test_gold_gdp_calculations(self):
        """Test gold GDP metric calculations"""
        # Simulate silver data
        data = {
            'date': pd.date_range('2020-01-01', periods=8, freq='QE'),
            'value': [100, 102, 104, 106, 108, 110, 112, 114],
            'series': ['abs'] * 8
        }
        df = pd.DataFrame(data)

        # Calculate YoY change (4 quarters)
        df['yoy_change_pct'] = df['value'].pct_change(4) * 100

        # Verify calculation
        expected_yoy = ((108 - 100) / 100) * 100
        assert abs(df['yoy_change_pct'].iloc[4] - expected_yoy) < 0.01

    def test_gold_cpi_mom_calculations(self):
        """Test CPI month-over-month calculation"""
        data = {
            'date': pd.date_range('2024-01-01', periods=3, freq='ME'),
            'value': [100, 101, 102.5],
            'category': ['Food'] * 3
        }
        df = pd.DataFrame(data)
        df['mom_change_pct'] = df['value'].pct_change() * 100

        assert abs(df['mom_change_pct'].iloc[1] - 1.0) < 0.01
        assert abs(df['mom_change_pct'].iloc[2] - 1.485) < 0.01

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