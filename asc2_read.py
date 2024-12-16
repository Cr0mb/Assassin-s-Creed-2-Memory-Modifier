import pymem
import pymem.process

def get_pointer_value(pm, base_address, offsets):
    try:
        address = pm.read_int(base_address)
        for offset in offsets[:-1]:
            address = pm.read_int(address + offset)
        final_value = pm.read_int(address + offsets[-1])
        return final_value
    except pymem.exception.MemoryReadError:
        return None
    except Exception as e:
        print(f"Error while reading pointer value: {e}")
        return None

def get_money_value(pm, base_address):
    try:
        offset_chain = [0x20, 0x18, 0x0, 0x18, 0xB0, 0x0, 0x0, 0x10]
        
        for offset in offset_chain:
            base_address = pm.read_uint(base_address) + offset

        money_value = pm.read_int(base_address)
        return money_value

    except pymem.exception.MemoryReadError as e:
        print(f"MemoryReadError: Could not read memory. Exception: {str(e)}")
    except pymem.exception.WinAPIError as e:
        print(f"WinAPIError: Could not read memory. Error code: {e.error_code}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    process_name = "AssassinsCreedIIGame.exe"
    health_pointer = 0x01E0E9E8
    health_offsets = [0x168, 0x00, 0x74, 0x40, 0x10, 0x30, 0x40, 0x58]

    try:
        pm = pymem.Pymem(process_name)
        module = pymem.process.module_from_name(pm.process_handle, process_name)
        base_address = module.lpBaseOfDll

        health_base = base_address + health_pointer
        health_value = get_pointer_value(pm, health_base, health_offsets)
        if health_value is not None:
            print(f"Health: {health_value}")
        else:
            print("Failed to read health value.")

        money_value = get_money_value(pm, base_address + 0x01E134B4)
        if money_value is not None:
            print(f"Your current money value is: {money_value}")
        else:
            print("Failed to retrieve money value.")

    except Exception as e:
        print(f"An error occurred while processing the memory: {e}")

if __name__ == "__main__":
    main()
