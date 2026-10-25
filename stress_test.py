#!/usr/bin/env python3
"""
Quick Performance & Memory Stress Test
"""

import asyncio
import sys
import os
import time
import json

sys.path.insert(0, os.getcwd())
import iterm2_mcp_server_optimized as optimized

async def stress_test():
    """Run a stress test to show memory management in action"""
    print("🔥 STRESS TEST: Memory Management Under Load")
    print("=" * 50)
    
    # Initial memory check
    initial_stats = await optimized.get_memory_stats()
    initial_data = json.loads(initial_stats)
    initial_memory = initial_data["memory_stats"]["rss_mb"]
    print(f"🏁 Starting memory: {initial_memory} MB")
    
    # Test 1: Multiple connection attempts (would cause memory bloat in original)
    print("\n⚡ Test 1: Connection stress (20 operations)")
    for i in range(20):
        result = await optimized.send_text(f"# Test {i}")
        if i % 5 == 0:
            print(f"   Operation {i+1}/20 completed")
    
    mid_stats = await optimized.get_memory_stats()
    mid_data = json.loads(mid_stats) 
    mid_memory = mid_data["memory_stats"]["rss_mb"]
    print(f"📊 Mid-test memory: {mid_memory} MB (+{mid_memory - initial_memory:.2f} MB)")
    
    # Test 2: Output capture stress with limits
    print("\n📺 Test 2: Output capture stress (10 operations)")
    for i in range(10):
        result = await optimized.run_command_optimized(
            f"echo 'Stress test {i}' && date && ls -la | head -20",
            max_output_chars=2000  # Keep output bounded
        )
        if i % 2 == 0:
            print(f"   Command {i+1}/10 completed")
    
    # Test 3: Terminal reading with line limits
    print("\n📖 Test 3: Terminal reading stress (10 operations)")
    for i in range(10):
        result = await optimized.read_terminal_output_optimized(
            max_lines=50  # Bounded line reading
        )
        if i % 2 == 0:
            print(f"   Read operation {i+1}/10 completed")
    
    # Force cleanup
    print("\n🧹 Running cleanup...")
    cleanup_result = await optimized.cleanup_connections()
    
    # Final memory check  
    final_stats = await optimized.get_memory_stats()
    final_data = json.loads(final_stats)
    final_memory = final_data["memory_stats"]["rss_mb"]
    
    print("\n🎯 STRESS TEST RESULTS:")
    print("=" * 30)
    print(f"Initial memory: {initial_memory:.2f} MB")
    print(f"Mid-test memory: {mid_memory:.2f} MB")
    print(f"Final memory: {final_memory:.2f} MB")
    print(f"Peak growth: +{mid_memory - initial_memory:.2f} MB")
    print(f"Net growth: +{final_memory - initial_memory:.2f} MB")
    
    if final_memory - initial_memory < 10:  # Less than 10MB growth
        print("✅ MEMORY MANAGEMENT: EXCELLENT! Minimal growth.")
    elif final_memory - initial_memory < 20:
        print("🟡 MEMORY MANAGEMENT: Good, some growth but controlled.")
    else:
        print("⚠️  MEMORY MANAGEMENT: Needs more optimization.")
        
    # Show connection manager state
    print(f"\nConnection Manager State:")
    print(f"  Active connection: {final_data['connection_manager']['has_active_connection']}")
    print(f"  Last used: {final_data['connection_manager']['last_used']}")

if __name__ == "__main__":
    asyncio.run(stress_test())
