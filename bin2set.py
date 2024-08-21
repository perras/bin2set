# /usr/bin/python3
# This script will take a bin file or python payload and turn it into a gdb set command. It is useful for emulating user input and behaviors with binary data while debugging ELF executables.
import sys
import binascii
if len(sys.argv) < 3:
         print("This script will take a binary or python payload and turn it into a gdb set command.\nUsage: ./bin2set.py example.bin 0xWHATEVER\nFile (example.bin) generated for testing.")
         
         # example shellcode using msfvenom -p linux/x64/exec cmd="id" -f py -v shellcode -b x00
         shellcode =  b""
         shellcode += b"\x48\xb8\x2f\x62\x69\x6e\x2f\x73\x68\x00\x99"
         shellcode += b"\x50\x54\x5f\x52\x66\x68\x2d\x63\x54\x5e\x52"
         shellcode += b"\xe8\x03\x00\x00\x00\x69\x64\x00\x56\x57\x54"
         shellcode += b"\x5e\x6a\x3b\x58\x0f\x05"

         trash = b"\x41"*11 # arbitrary trash. arbitrary length
         nops= b"\x90\x90\x90\x90" # no operation
         address = b"\xde\xad\xc0\xde" # arbitrary address
         payload = trash+nops+shellcode+address # arbitrary payload construction
         open('example.bin', 'wb').write(payload) # arbitrary binary file
         sys.exit(1)

xxd_output = binascii.hexlify(open(sys.argv[1], 'rb').read()).decode('utf-8') # does the same thing as xxd -p
address = sys.argv[2] # address at which there is desire to mimic user behavior/input

bytes_list = [xxd_output[i:i+2] for i in range(0, len(xxd_output), 2)]
gdb_formatted_bytes = ', '.join(f'0x{byte}' for byte in bytes_list)
gdb_command = f'set {{unsigned char[{len(bytes_list)}]}} {address} = {{{gdb_formatted_bytes}}}'
print(gdb_command)
