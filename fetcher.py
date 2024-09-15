import windows

class ThreadStackFinder:

    @staticmethod
    def get_ce_thread_stack(process_name: str):
        target_process = None
        stack_base_list = []
        pointer_size = None
        stack_size = None
        base_thread_init_thunk_address = None
        cheat_engine_thread_stack_list = []
        
        process_list = windows.system.enumerate_processes()
        for process in process_list:
            if process.name == process_name:
                target_process = process
                break

        if target_process.bitness == 64:
            pointer_size = 8
            stack_size = 4096 * 2
        else:
            pointer_size = 4
            stack_size = 4096

        thread_list = target_process.threads

        for thread in thread_list:
            teb = thread.teb_base
            if target_process.is_wow_64:
                teb += 0x2000
            
            stack_base_address = teb + pointer_size
            stack_base = target_process.read_ptr(stack_base_address)
            stack_base_list.append(stack_base)

        modules_list = target_process.peb.modules
        for module in modules_list:
            if module.pe.export_name == "KERNEL32.dll":
                base_thread_init_thunk_address = module.pe.exports['BaseThreadInitThunk']
                break

        for stack_top in stack_base_list:
            buffer = target_process.read_memory(stack_top - stack_size, stack_size)
            index = 0
            byte_counter = 0
            temp_pointer = 0
            for byte in buffer:
                temp_pointer ^= (byte << 8 * byte_counter)
                byte_counter += 1
                if byte_counter == pointer_size:
                    if target_process.is_wow_64:
                        if base_thread_init_thunk_address == temp_pointer:
                            cheat_engine_thread_stack_list.append(hex(stack_top - stack_size + pointer_size * index))
                    else:
                        if base_thread_init_thunk_address <= temp_pointer <= base_thread_init_thunk_address + 0x100:
                            cheat_engine_thread_stack_list.append(hex(stack_top - stack_size + pointer_size * index))
                    index += 1
                    byte_counter = 0
                    temp_pointer = 0
        
        return cheat_engine_thread_stack_list