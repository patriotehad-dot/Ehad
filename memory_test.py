#!/usr/bin/env python3
"""
Memory Test Script for iTerm2 MCP Server
Tests both original and optimized versions under memory stress
"""

import asyncio
import psutil
import os
import time
import sys
import json
from pathlib import Path

# Add the current directory to the path so we can import both servers
sys.path.insert(0, os.getcwd())

def get_memory_usage():
    """Get current memory usage in MB"""
    process = psutil.Process(os.getpid())
    return round(process.memory_info().rss / 1024 / 1024, 2)

def simulate_mcp_tool_calls(server_module, num_calls=20):
    """Simulate multiple MCP tool calls to test memory usage"""
    print(f"\n🧪 Testing {server_module.__name__} with {num_calls} tool calls...")
    
    initial_memory = get_memory_usage()
    print(f"Initial memory: {initial_memory} MB")
    
    memory_samples = [initial_memory]
    
    # Run the event loop for testing
    async def test_session():
        nonlocal memory_samples
        
        # Test 1: Multiple connection-heavy operations
        print("📡 Test 1: Connection stress test...")
        for i in range(num_calls // 4):
            try:
                # These would normally be MCP tool calls
                if hasattr(server_module, 'get_session_info'):
                    result = await server_module.get_session_info()
                    if i % 2 == 0:  # Sample memory every other call
                        memory_samples.append(get_memory_usage())
            except Exception as e:
                print(f"   Error in call {i}: {e}")
        
        # Test 2: Output capture stress test
        print("📺 Test 2: Output capture stress test...")
        for i in range(num_calls // 4):
            try:
                if hasattr(server_module, 'read_terminal_output'):
                    result = await server_module.read_terminal_output()
                elif hasattr(server_module, 'read_terminal_output_optimized'):
                    result = await server_module.read_terminal_output_optimized()
                memory_samples.append(get_memory_usage())
            except Exception as e:
                print(f"   Error in output test {i}: {e}")
        
        # Test 3: Command execution stress test  
        print("⚡ Test 3: Command execution stress test...")
        for i in range(num_calls // 4):
            try:
                # Run a harmless command that produces output
                if hasattr(server_module, 'run_command'):
                    result = await server_module.run_command(f"echo 'Test command {i}' && ls -la", wait_for_output=True)
                elif hasattr(server_module, 'run_command_optimized'):
                    result = await server_module.run_command_optimized(f"echo 'Test command {i}' && ls -la", wait_for_output=True)
                memory_samples.append(get_memory_usage())
            except Exception as e:
                print(f"   Error in command test {i}: {e}")
        
        # Test 4: Mixed operations
        print("🔀 Test 4: Mixed operations...")
        for i in range(num_calls // 4):
            try:
                # Alternate between different operations
                if i % 3 == 0 and hasattr(server_module, 'send_text'):
                    await server_module.send_text(f"# Test input {i}")
                elif i % 3 == 1 and hasattr(server_module, 'clear_screen'):
                    await server_module.clear_screen()
                else:
                    if hasattr(server_module, 'get_session_info'):
                        await server_module.get_session_info()
                        
                memory_samples.append(get_memory_usage())
            except Exception as e:
                print(f"   Error in mixed test {i}: {e}")
    
    # Run the async test session
    try:
        asyncio.run(test_session())
    except Exception as e:
        print(f"Test session failed: {e}")
    
    final_memory = get_memory_usage()
    peak_memory = max(memory_samples)
    memory_growth = final_memory - initial_memory
    
    print(f"\n📊 Memory Results for {server_module.__name__}:")
    print(f"   Initial: {initial_memory} MB")
    print(f"   Final: {final_memory} MB") 
    print(f"   Peak: {peak_memory} MB")
    print(f"   Growth: {memory_growth:+.2f} MB")
    print(f"   Samples: {len(memory_samples)} data points")
    
    return {
        'initial': initial_memory,
        'final': final_memory,
        'peak': peak_memory,
        'growth': memory_growth,
        'samples': memory_samples
    }

def compare_servers():
    """Compare original vs optimized server memory usage"""
    print("🐒 iTerm2 MCP Server Memory Comparison Test")
    print("=" * 50)
    
    results = {}
    
    # Test original server (if available)
    try:
        import iterm2_mcp_server as original
        results['original'] = simulate_mcp_tool_calls(original, num_calls=20)
        
        # Cleanup between tests
        time.sleep(2)
        
    except ImportError:
        print("❌ Original server not available for comparison")
        results['original'] = None
    
    # Test optimized server
    try:
        import iterm2_mcp_server_optimized as optimized
        results['optimized'] = simulate_mcp_tool_calls(optimized, num_calls=20)
        
        # Test the cleanup function
        print("\n🧹 Testing cleanup function...")
        initial_cleanup = get_memory_usage()
        asyncio.run(optimized.cleanup_connections())
        post_cleanup = get_memory_usage()
        print(f"   Memory before cleanup: {initial_cleanup} MB")
        print(f"   Memory after cleanup: {post_cleanup} MB")
        print(f"   Cleanup freed: {initial_cleanup - post_cleanup:.2f} MB")
        
        # Test memory stats function
        print("\n📈 Testing memory stats function...")
        stats_result = asyncio.run(optimized.get_memory_stats())
        stats_data = json.loads(stats_result)
        if stats_data['success']:
            print(f"   Current RSS: {stats_data['memory_stats']['rss_mb']} MB")
            print(f"   Memory %: {stats_data['memory_stats']['percent']}%")
        
    except ImportError as e:
        print(f"❌ Optimized server not available: {e}")
        results['optimized'] = None
    
    # Generate comparison report
    print("\n" + "=" * 50)
    print("🎯 COMPARISON SUMMARY")
    print("=" * 50)
    
    if results['original'] and results['optimized']:
        orig = results['original']
        opt = results['optimized']
        
        improvement = orig['growth'] - opt['growth']
        peak_improvement = orig['peak'] - opt['peak']
        
        print(f"Memory Growth Comparison:")
        print(f"   Original: {orig['growth']:+.2f} MB")
        print(f"   Optimized: {opt['growth']:+.2f} MB")
        print(f"   Improvement: {improvement:+.2f} MB ({improvement/abs(orig['growth'])*100:+.1f}%)")
        
        print(f"\nPeak Memory Comparison:")
        print(f"   Original Peak: {orig['peak']:.2f} MB")
        print(f"   Optimized Peak: {opt['peak']:.2f} MB")  
        print(f"   Peak Improvement: {peak_improvement:+.2f} MB")
        
        if improvement > 0:
            print("\n✅ OPTIMIZATION SUCCESS! Memory usage reduced.")
        else:
            print("\n⚠️  Optimization needs more work.")
            
    elif results['optimized']:
        opt = results['optimized']
        print(f"Optimized Server Results:")
        print(f"   Memory Growth: {opt['growth']:+.2f} MB")
        print(f"   Peak Usage: {opt['peak']:.2f} MB")
        print("✅ Optimized server running successfully!")
    
    else:
        print("❌ No servers available for testing")

if __name__ == "__main__":
    compare_servers()
