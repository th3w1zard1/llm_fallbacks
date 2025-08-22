#!/usr/bin/env python3
"""Test script for the LLM Fallbacks CI/CD system."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

def test_generate_configs():
    """Test that generate_configs.py can run successfully."""
    print("Testing generate_configs.py...")
    
    try:
        # Import and test the generate_configs module
        from llm_fallbacks.generate_configs import to_litellm_config_yaml, CUSTOM_PROVIDERS
        
        # Test the function with empty providers
        config = to_litellm_config_yaml([], free_only=True)
        
        # Verify the config structure
        required_keys = ['cache', 'general_settings', 'litellm_settings', 'model_list', 'router_settings']
        for key in required_keys:
            if key not in config:
                print(f"❌ Missing required key: {key}")
                return False
        
        print("✅ generate_configs.py test passed")
        return True
        
    except Exception as e:
        print(f"❌ generate_configs.py test failed: {e}")
        return False

def test_config_structure():
    """Test that the configuration structure is valid."""
    print("Testing configuration structure...")
    
    try:
        # Test that we can import the config module
        from llm_fallbacks.config import (
            ALL_MODELS, FREE_MODELS, ALL_CHAT_MODELS, FREE_CHAT_MODELS,
            CUSTOM_PROVIDERS
        )
        
        # Verify that the lists are populated
        if not ALL_MODELS:
            print("❌ ALL_MODELS is empty")
            return False
            
        if not FREE_MODELS:
            print("❌ FREE_MODELS is empty")
            return False
            
        if not ALL_CHAT_MODELS:
            print("❌ ALL_CHAT_MODELS is empty")
            return False
            
        if not FREE_CHAT_MODELS:
            print("❌ FREE_CHAT_MODELS is empty")
            return False
            
        print("✅ Configuration structure test passed")
        return True
        
    except Exception as e:
        print(f"❌ Configuration structure test failed: {e}")
        return False

def test_core_functions():
    """Test that core functions work correctly."""
    print("Testing core functions...")
    
    try:
        from llm_fallbacks.core import (
            get_litellm_models,
            calculate_cost_per_token,
            sort_models_by_cost_and_limits
        )
        
        # Test getting models
        models = get_litellm_models()
        if not models:
            print("❌ No models returned from get_litellm_models")
            return False
            
        # Test cost calculation
        sample_model = next(iter(models.values()))
        cost = calculate_cost_per_token(sample_model)
        if cost < 0:
            print("❌ Invalid cost calculated")
            return False
            
        # Test sorting
        sorted_models = sort_models_by_cost_and_limits(models, free_only=True)
        if not sorted_models:
            print("❌ No free models found")
            return False
            
        print("✅ Core functions test passed")
        return True
        
    except Exception as e:
        print(f"❌ Core functions test failed: {e}")
        return False

def test_docker_files():
    """Test that Docker files exist and are valid."""
    print("Testing Docker files...")
    
    docker_files = [
        "Dockerfile.model-updater",
        "Dockerfile.scheduler"
    ]
    
    for docker_file in docker_files:
        if not Path(docker_file).exists():
            print(f"❌ Missing Docker file: {docker_file}")
            return False
            
        # Check if file has content
        if Path(docker_file).stat().st_size == 0:
            print(f"❌ Empty Docker file: {docker_file}")
            return False
    
    print("✅ Docker files test passed")
    return True

def test_requirements():
    """Test that requirements.txt exists and is valid."""
    print("Testing requirements.txt...")
    
    if not Path("requirements.txt").exists():
        print("❌ Missing requirements.txt")
        return False
        
    # Check if file has content
    if Path("requirements.txt").stat().st_size == 0:
        print("❌ Empty requirements.txt")
        return False
        
    print("✅ Requirements test passed")
    return True

def main():
    """Run all tests."""
    print("🚀 Running LLM Fallbacks CI/CD System Tests\n")
    
    tests = [
        test_generate_configs,
        test_config_structure,
        test_core_functions,
        test_docker_files,
        test_requirements
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is ready for deployment.")
        return 0
    else:
        print("❌ Some tests failed. Please fix the issues before deploying.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
