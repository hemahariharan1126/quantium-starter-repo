import pytest
from dash.testing.application_runners import import_app

def test_header_present(dash_duo):
    """Test that the header is present in the app"""
    app = import_app("app")
    dash_duo.start_server(app)
    
    # Check if header H1 element exists
    dash_duo.wait_for_element("h1", timeout=4)
    header = dash_duo.find_element("h1")
    
    # Verify header text contains expected content
    assert "Pink Morsel" in header.text or "Sales" in header.text

def test_visualization_present(dash_duo):
    """Test that the visualization/graph is present"""
    app = import_app("app")
    dash_duo.start_server(app)
    
    # Check if the graph component exists
    dash_duo.wait_for_element("#sales-chart", timeout=4)
    graph = dash_duo.find_element("#sales-chart")
    
    # Verify the graph element is displayed
    assert graph is not None

def test_region_picker_present(dash_duo):
    """Test that the region picker/radio buttons are present"""
    app = import_app("app")
    dash_duo.start_server(app)
    
    # Check if the region filter radio items exist
    dash_duo.wait_for_element("#region-filter", timeout=4)
    region_filter = dash_duo.find_element("#region-filter")
    
    # Verify the region filter is present
    assert region_filter is not None
    
    # Optionally verify all 5 options are present
    radio_inputs = dash_duo.find_elements("input[type='radio']")
    assert len(radio_inputs) == 5
