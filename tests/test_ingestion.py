"""Unit tests for ingestion modules"""

# Import libraries
from unittest.mock import MagicMock, patch

import pytest
import requests

from src.ingestion.api_client import APIClient


class TestAPIClient:
    """Test API client"""

    def test_init_default_values(self):
        """Test default initialization values"""
        client = APIClient()
        assert client.max_retries == 3
        assert client.retry_delay == 1.0

    def test_init_custom_values(self):
        """Test custom initialization values"""
        client = APIClient(max_retries=5, retry_delay=2.0)
        assert client.max_retries == 5
        assert client.retry_delay == 2.0

    @patch("src.ingestion.api_client.requests.get")
    def test_fetch_success(self, mock_get):
        """Test successful API fetch"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": "test"}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        client = APIClient()
        result = client.fetch("http://test.com/api")

        assert result == {"data": "test"}
        mock_get.assert_called_once()

    @patch("src.ingestion.api_client.requests.get")
    def test_fetch_retry_on_failure(self, mock_get):
        """Test retry logic on failure"""
        mock_get.side_effect = [
            requests.RequestException("Connection error"),
            requests.RequestException("Connection error"),
            MagicMock(json=lambda: {"data": "success"}, raise_for_status=lambda: None),
        ]

        client = APIClient(max_retries=3, retry_delay=0.1)
        result = client.fetch("http://test.com/api")

        assert result == {"data": "success"}
        assert mock_get.call_count == 3


class TestIngestionFunctions:
    """Tests for ingestion functions"""

    @patch("src.ingestion.gdp_ingestion.APIClient")
    @patch("src.ingestion.gdp_ingestion.get_engine")
    def test_ingest_gdp_returns_batch_id(self, mock_engine, mock_client):
        """Test GDP ingestion returns a batch ID"""
        mock_client_instance = MagicMock()
        mock_client_instance.fetch.return_value = [{"date": "2024-01", "value": 100}]
        mock_client.return_value = mock_client_instance

        mock_conn = MagicMock()
        mock_engine.return_value.connect.return_value.__enter__ = MagicMock(
            return_value=mock_conn
        )
        mock_engine.return_value.connect.return_value.__exit__ = MagicMock(
            return_value=False
        )

        from src.ingestion.gdp_ingestion import ingest_gdp_data

        batch_id = ingest_gdp_data()

        assert batch_id is not None
        assert len(batch_id) == 36
