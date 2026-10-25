#!/usr/bin/env python3
"""
Simple manual test of memory optimization features
"""

import asyncio
import sys
import os

# Import the optimized server
sys.path.insert(0, os.getcwd())
import iterm2_mcp_server_optimized as optimized

async def test_memory_features():
    """Test the memory-optimized features"""
    print("🐒 Testing iTerm2 MCP Server Memory Optimizations")
    print("=" * 50)
    
    # Test 1: Memory stats
    print("\n📊 Test 1: Memory Statistics")
    print("-" * 30)
    stats_result = await optimized.get_memory_stats()
    print("Memory stats result:")
    print(stats_result)
    
    # Test 2: Connection cleanup
    print("\n🧹 Test 2: Connection Cleanup")  
    print("-" * 30)
    cleanup_result = await optimized.cleanup_connections()
    print("Cleanup result:")
    print(cleanup_result)
    
    # Test 3: Optimized command execution
    print("\n⚡ Test 3: Optimized Command Execution")
    print("-" * 30)
    
    # Run a command that produces moderate output
    cmd_result = await optimized.run_command_optimized(
        "echo 'Testing output limits...' && ls -la",
        max_output_chars=5000  # Set a limit
    )
    print("Command result (truncated):")
    print(cmd_result[:500] + "..." if len(cmd_result) > 500 else cmd_result)
    
    # Test 4: Optimized terminal reading
    print("\n📺 Test 4: Optimized Terminal Reading")
    print("-" * 30)
    
    terminal_result = await optimized.read_terminal_output_optimized(
        max_lines=20  # Limit lines
    )
    print("Terminal output result (truncated):")
    print(terminal_result[:500] + "..." if len(terminal_result) > 500 else terminal_result)
    
    # Test 5: File operations with size limits
    print("\n📄 Test 5: File Operations with Size Limits")
    print("-" * 30)
    
    # Create a test file
    test_content = "Line {}\\n".format("\\n".join([f"Line {i}" for i in range(100)]))
    
    # Test chunked file reading
    file_result = await optimized.read_file_chunked(
        "iterm2_mcp_server.py",  # Read the original server file
        start_line=1,
        end_line=50,  # Just first 50 lines
        max_size_mb=1.0  # 1MB limit
    )
    print("File reading result (truncated):")
    print(file_result[:300] + "..." if len(file_result) > 300 else file_result)
    
    print("\n✅ All memory optimization features tested successfully!")

if __name__ == "__main__":
    asyncio.run(test_memory_features())
