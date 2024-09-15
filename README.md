# ThreadStackFinder

## Overview

`ThreadStackFinder` is a Python class designed to locate the thread stack base addresses of a specified process. It interfaces with Windows system APIs to enumerate processes and their threads, analyze stack memory regions, and identify addresses related to thread initialization.

## Features

- Enumerates processes and threads to find a specified target process.
- Supports both 32-bit and 64-bit processes.
- Calculates and reads memory from stack regions to identify specific thread stack locations.
- Finds and verifies addresses related to thread initialization in the `KERNEL32.dll` module.

## Requirements

- Python 3.x
- `windows` module (custom or third-party library for Windows API access)

## Usage

1. **Import the Class**

    ```python
    from thread_stack_finder import ThreadStackFinder
    ```

2. **Get Thread Stack Addresses**

    To find the Cheat Engine thread stack addresses for a process, call the `get_ce_thread_stack` method with the process name.

    ```python
    process_name = "target_process.exe"
    stack_addresses = ThreadStackFinder.get_ce_thread_stack(process_name)
    print(stack_addresses)
    ```

## Explanation

1. **Process Identification**: The code first identifies the target process by name from a list of all processes.

2. **Pointer and Stack Size**: Based on whether the process is 32-bit or 64-bit, the appropriate pointer size and stack size are set.

3. **Thread Enumeration**: For each thread in the target process, the base address of its stack is calculated and stored.

4. **Module Analysis**: The `KERNEL32.dll` module is examined to get the address of the `BaseThreadInitThunk` function.

5. **Memory Analysis**: The stack memory regions are read to find pointers that match or fall within the address range of `BaseThreadInitThunk`. These pointers are then used to identify thread stack addresses compatible with Cheat Engine.

## Notes

- Ensure the script is run with the necessary permissions to access process and memory information.
- The `windows` module must be properly installed and configured in your Python environment.
- The script assumes the presence of a specific library or module for Windows API interactions; adjust as necessary for your environment.
