import pymem
import pymem.process
import time
import threading

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

def set_pointer_value(pm, base_address, offsets, new_value):
    try:
        address = pm.read_int(base_address)
        for offset in offsets[:-1]:
            address = pm.read_int(address + offset)
        final_address = address + offsets[-1]
        pm.write_int(final_address, new_value)
    except pymem.exception.MemoryWriteError as e:
        print(f"MemoryWriteError: Could not write memory. Exception: {str(e)}")
    except Exception as e:
        print(f"Error while writing pointer value: {e}")

def get_money_value(pm, base_address):
    try:
        offset_chain = [0x20, 0x18, 0x0, 0x18, 0xB0, 0x0, 0x0, 0x10]
        for offset in offset_chain:
            base_address = pm.read_uint(base_address) + offset
        money_value = pm.read_int(base_address)
        return money_value
    except pymem.exception.MemoryReadError as e:
        print(f"MemoryReadError: Could not read money value. Exception: {str(e)}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while reading money: {e}")
        return None

def set_money_value(pm, base_address, new_value):
    try:
        offset_chain = [0x20, 0x18, 0x0, 0x18, 0xB0, 0x0, 0x0, 0x10]
        for offset in offset_chain:
            base_address = pm.read_uint(base_address) + offset
        pm.write_int(base_address, new_value)
    except pymem.exception.MemoryWriteError as e:
        print(f"MemoryWriteError: Could not write money value. Exception: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred while writing money: {e}")

def get_health_value(pm, base_address, health_pointer, health_offsets):
    try:
        health_value = get_pointer_value(pm, base_address + health_pointer, health_offsets)
        return health_value
    except Exception as e:
        print(f"Error while reading health value: {e}")
        return None

def enable_god_mode(pm, base_address, health_pointer, health_offsets):
    while True:
        try:
            health_value = get_pointer_value(pm, base_address + health_pointer, health_offsets)
            if health_value != 20:
                set_pointer_value(pm, base_address + health_pointer, health_offsets, 21)
            time.sleep(1)
        except Exception as e:
            print(f"Error in God Mode loop: {e}")
            break

def display_menu(god_mode_enabled, current_health, current_money):
    print("\n==== Assassin's Creed 2 Memory Modifier ====")
    print("\nMade By Cr0mb.")
    print(f"Current Health: {current_health}")
    print(f"Current Money: {current_money}")
    if god_mode_enabled:
        print("1. Disable God Mode")
    else:
        print("1. Enable God Mode")
    print("2. Set Money Value")
    print("3. Exit")
    choice = input("Please choose an option (1-3): ")
    return choice

def main():
    process_name = "AssassinsCreedIIGame.exe"
    health_pointer = 0x01E0E9E8
    health_offsets = [0x168, 0x00, 0x74, 0x40, 0x10, 0x30, 0x40, 0x58]

    try:
        pm = pymem.Pymem(process_name)
        module = pymem.process.module_from_name(pm.process_handle, process_name)
        base_address = module.lpBaseOfDll

        god_mode_enabled = False
        god_mode_thread = None

        while True:
            current_health = get_health_value(pm, base_address, health_pointer, health_offsets)
            current_money = get_money_value(pm, base_address + 0x01E134B4)

            choice = display_menu(god_mode_enabled, current_health, current_money)

            if choice == '1':
                if god_mode_enabled:
                    print("Disabling God Mode...")
                    god_mode_thread = None
                    god_mode_enabled = False
                else:
                    print("Enabling God Mode...")
                    god_mode_thread = threading.Thread(target=enable_god_mode, args=(pm, base_address, health_pointer, health_offsets))
                    god_mode_thread.daemon = True
                    god_mode_thread.start()
                    god_mode_enabled = True

            elif choice == '2':
                try:
                    new_money = int(input("Enter the new money value: "))
                    set_money_value(pm, base_address + 0x01E134B4, new_money)
                except ValueError:
                    print("Invalid input. Please enter a valid number.")

            elif choice == '3':
                print("Exiting...")
                break

            else:
                print("Invalid choice, please choose between 1 and 3.")

    except Exception as e:
        print(f"An error occurred while processing the memory: {e}")

if __name__ == "__main__":
    main()
