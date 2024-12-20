## Exploit Development and Buffer Overflow Exploitation Walkthrough

**This document serves as a personal walkthrough for exploiting a binary using buffer overflow, ROP chains, and shellcode to retrieve the flag. I'll detail my journey step by step, discussing the observations, approaches, and techniques I used to bypass the security mechanisms and crack the binary.**

# Observations:

**1**: Check the Security Protocols of the Binary
First things first, it's essential to analyze the binary and determine what security protocols are enabled. To do this, I used the checksec tool:
    
    checksec --binary=<binary_file_name>

The output revealed the following:

1)Partial RELRO
2)No Canary Found
3) NX Disabled
4) No PIE

**Conclusion:**

1) ASLR (Address Space Layout Randomization): The No PIE indicates that ASLR is not enabled, which is beneficial for exploiting buffer overflows. This lack of randomness means that memory addresses remain predictable, allowing us to target specific regions.

2)Security Mechanisms: Despite the lack of PIE, the presence of Partial RELRO and NX Disabled (No execute bit) indicates that some protections are in place. However, given that NX is disabled, executing shellcode becomes easier, which is a potential exploit vector.

3) Randomness from the Kernel: Even though ASLR isn’t directly enabled, the kernel may still impose some randomness, potentially shifting the buffer overflow or payload position, causing issues like Segmentation Faults if the overflow overwrites an instruction that lies within the RELRO-protected region.

**2**: No Direct Function to Retrieve the Flag

The binary doesn't provide a direct function to retrieve the flag. Therefore, I had to resort to ROP (Return-Oriented Programming) to craft a custom chain of instructions that would allow me to access the flag by exploiting available gadgets.

**3**: Identifying a Useful Gadget  

     ROPgadget --binary ./vuln > gadgets.txt
     I discovered a useful gadget:   **jmp eax**

This gadget is simple but effective, as it can redirect execution to whatever is placed in the eax register.

**4**: Navigating to eax

I started by attempting to overwrite the EIP (Instruction Pointer) with the desired value using a buffer overflow. The offset to the EIP was found to be 28 bytes (using gef to examine the stack). However, this approach didn’t work immediately as expected.

I attempted to navigate to eax by chaining the jmp eax gadget at the end of the buffer.

The result? I couldn’t properly stitch the payload, and the program crashed.

**5**: Controlled Approach for Navigation

After some trial and error, I decided to refine my approach:

Instead of jumping directly, I introduced a **short jump (8 bytes)** after the **first 24 bytes**.
This restricted my payload’s randomness and helped maintain control over where execution would land.
Now I was able to control the flow better.

**6**: Overwriting eax and Using Shellcode

At this point, I successfully overflowed eax. However, when I tried to attach the shellcode to eax, it wasn't executing as expected.

I realized that eax has some restrictions (like it being a general-purpose register), so it was not working well for this case.

**7**: Redirecting Execution to ebx
I decided to overflow eax so much that the buffer would overflow into the adjacent ebx register instead. To facilitate this, I crafted a buffer of 500 C's after the jmp eax instruction to ensure I would land on ebx and not eax.
Now, with ebx holding my shellcode, I could successfully execute it.

**8**: Success! Flag Retrieved

After stitching the shellcode (specifically designed to read the flag) into the payload, I finally managed to exploit the vulnerability and retrieve the flag.

## FLAG RETRIEVED
**YES indeed the flag contained that "Chiranjeet was here" :_)
![RESULT](https://github.com/CHIRANJEET1729DAS/ROP-Reverse-Oriented-Programming-/blob/main/Results/cracked.png)



## HERE are the snapshots of intermediate steps

here, I set a breakpoint at **jmp eax**
![1](https://github.com/CHIRANJEET1729DAS/ROP-Reverse-Oriented-Programming-/blob/main/Payload/Immediate_steps/third.png)

here, I load the **payload** and run
![2](https://github.com/CHIRANJEET1729DAS/ROP-Reverse-Oriented-Programming-/blob/main/Payload/Immediate_steps/fourth.png)

here, I successfully navigated to **ebx** register 
![3](https://github.com/CHIRANJEET1729DAS/ROP-Reverse-Oriented-Programming-/blob/main/Payload/Immediate_steps/fifth.png)
