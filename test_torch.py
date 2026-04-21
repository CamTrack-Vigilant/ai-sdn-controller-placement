#!/usr/bin/env python3
"""Quick test for torch availability."""
try:
    import torch
    print(f"✓ torch installed: {torch.__version__}")
except ImportError:
    print("✗ torch not available (install via: pip install torch)")
