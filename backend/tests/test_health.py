"""Tests for health check endpoints"""
import pytest
from fastapi.testclient import TestClient


def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert data["app"] == "PharmaBot"
    assert data["version"] == "1.0.0"


def test_system_status(client):
    """Test the system status endpoint"""
    response = client.get("/api/status")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "operational"
    assert "services" in data
    assert data["services"]["api"] == "running"
    assert "timestamp" in data


def test_root_endpoint(client):
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert data["app"] == "PharmaBot"
    assert data["version"] == "1.0.0"
    assert data["status"] == "running"
    assert data["docs"] == "/docs"
