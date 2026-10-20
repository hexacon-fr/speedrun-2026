#!/usr/bin/env python3
"""
Custom CPU service.

A fictional CPU with sixteen 16-bit general-purpose registers and a 16-bit
address space. The player sends a raw program over the network; the CPU runs it
and answers with a disassembled execution trace (address, the two fetched bytes
and the decoded mnemonic for every executed instruction) plus any bytes the
program wrote to the output. On a fault, the CPU also dumps its register file
and the memory segment map.

The disassembly reveals what each opcode does, but the player still has to:
  - probe bytes to recover the instruction encoding (2 bytes / instruction),
  - build 16-bit values from 4-bit immediates with shl / add,
  - find the flag via the segment map printed on any fault,
  - cope with the memory permissions (writing into SECRET is a data abort),
  - fit inside a tiny code budget, so the flag has to be printed with a loop,
  - deal with taint: a register loaded from SECRET is poisoned (redacted in the
    register dump, illegal to store), so the flag can only leave through `out`,
  - print the *whole* flag and NUL-terminate it, else the output stays withheld.

Instruction encoding (2 bytes):

    byte0 = opcode (8 bits)        byte1 = [rd:4 | operand:4]

`rd` (high nibble of byte1) is the destination / primary register. `operand`
(low nibble of byte1) is a 4-bit immediate or a source-register index depending
on the opcode. Most of the 256 opcode values are unused -> ILLEGAL_INSTRUCTION.

Wire protocol (raw TCP, behind socat):
    -> 2 bytes  : big-endian program length N (0 < N <= MAX_PROGRAM)
    -> N bytes  : the program, loaded at CODE base (0x0000), PC starts at 0
    <- text     : execution report (UTF-8)
"""

import os
import socket
import socketserver
import sys

# --------------------------------------------------------------------------
# Machine configuration
# --------------------------------------------------------------------------

MEM_SIZE     = 0x10000      # 64 KiB, 16-bit address space, byte addressable
NUM_REGS     = 16           # R0..R15, each 16 bits
MAX_PROGRAM  = 0x80         # 128 bytes = 64 instructions: too small to unroll
                            # the whole flag, which forces a read/print loop
MAX_STEPS    = 20000        # anti-infinite-loop guard (also bounds the trace)
MAX_OUTPUT   = 4096         # cap bytes a program may emit

CODE_BASE    = 0x0000       # programs are loaded here, PC = 0


class Segment:
    """A mapped memory region with rwx permissions."""

    def __init__(self, name, start, end, perms):
        self.name  = name
        self.start = start
        self.end   = end                 # inclusive
        self.read  = perms[0] == "r"
        self.write = perms[1] == "w"
        self.exec  = perms[2] == "x"
        self.perms = perms

    def contains(self, addr):
        return self.start <= addr <= self.end


# Note: SECRET is readable but NOT writable -> writing into it is a data abort.
# The whole map is printed on every fault, which is how a player discovers
# where the flag lives.
SEGMENTS = [
    Segment("CODE",   0x0000, 0x0FFF, "r-x"),  # program image, executable
    Segment("DATA",   0x1000, 0x1FFF, "rw-"),  # scratch, read/write, no execute
    Segment("SECRET", 0x4000, 0x4FFF, "r--"),  # read-only, holds the flag
]

SECRET_BASE = 0x4000

# Initial register contents (R0..R15), printed by the demo program in client.py.
GREETING = b"WELCOME2HEXACON"


class CpuFault(Exception):
    """Raised when the CPU cannot continue. `addr` is the faulting data/fetch
    address when relevant (None otherwise)."""

    def __init__(self, reason, detail, addr=None):
        super().__init__(reason)
        self.reason = reason
        self.detail = detail
        self.addr   = addr


# --------------------------------------------------------------------------
# CPU core
# --------------------------------------------------------------------------

class CPU:
    def __init__(self, flag=b""):
        self.mem = bytearray(MEM_SIZE)
        # 16-bit general registers R0..R15, pre-loaded with a greeting so the
        # demo program in client.py (out r0 .. out r15) prints something.
        self.R   = list(GREETING.ljust(NUM_REGS, b"\x00"))
        self.pc  = 0                  # 16-bit program counter
        self.zf  = 0                  # zero flag
        self.cf  = 0                  # carry flag
        self.halted = False
        self.prog_len = 0             # number of program bytes actually loaded

        self.output = bytearray()
        self.trace  = []              # list of (pc, byte0, byte1)
        self.fault_pc = 0             # address of the faulting instruction

        # Taint tracking: a register becomes tainted the moment it receives a
        # byte read out of SECRET, and STAYS tainted for the rest of the run.
        # Taint propagates through every ALU op and through mov. Tainted values
        # are redacted in the register dump and may not be stored to memory, so
        # the flag can only be revealed through the `out` sink.
        self.T = [False] * NUM_REGS

        # Plant the flag in the read-only SECRET segment, NUL-terminated.
        self.flag_len = len(flag)     # length of the flag itself (without NUL)
        flag = flag + b"\x00"
        self.mem[SECRET_BASE:SECRET_BASE + len(flag)] = flag

    # -- memory access with permission checks ------------------------------

    @staticmethod
    def _seg_for(addr):
        for seg in SEGMENTS:
            if seg.contains(addr):
                return seg
        return None

    def fetch(self, addr):
        seg = self._seg_for(addr)
        if seg is None:
            raise CpuFault("PREFETCH_ABORT", "fetch from unmapped memory", addr)
        if not seg.exec:
            raise CpuFault("PREFETCH_ABORT",
                           "fetch from non-executable segment %s" % seg.name, addr)
        # Only the bytes the player actually sent are valid code. Running past
        # them (e.g. a program with no hlt) is a fetch from uninitialized memory.
        if addr >= CODE_BASE + self.prog_len:
            raise CpuFault("UNINITIALIZED_FETCH",
                           "fetch beyond the loaded program", addr)
        return self.mem[addr]

    def load_byte(self, addr):
        seg = self._seg_for(addr)
        if seg is None:
            raise CpuFault("DATA_ABORT", "load from unmapped memory", addr)
        if not seg.read:
            raise CpuFault("DATA_ABORT",
                           "load from non-readable segment %s" % seg.name, addr)
        return self.mem[addr]

    def store_byte(self, addr, value):
        seg = self._seg_for(addr)
        if seg is None:
            raise CpuFault("DATA_ABORT", "store to unmapped memory", addr)
        if not seg.write:
            raise CpuFault("DATA_ABORT",
                           "store to read-only segment %s" % seg.name, addr)
        self.mem[addr] = value & 0xFF

    # -- helpers -----------------------------------------------------------

    def _set_reg(self, idx, value, tainted=False):
        self.R[idx] = value & 0xFFFF
        self.zf = 1 if self.R[idx] == 0 else 0
        # Taint is sticky: a tainted register never becomes clean again, and any
        # tainted input keeps it tainted.
        self.T[idx] = self.T[idx] or bool(tainted)

    # -- one instruction ---------------------------------------------------

    @staticmethod
    def _s8(value):
        """Interpret a byte as a signed 8-bit offset."""
        return value - 0x100 if value & 0x80 else value

    def execute(self, opcode, rd, arg, b1):
        """For most opcodes `arg` (low nibble of byte1) is a 4-bit immediate or a
        source-register index. For the branch opcodes, the whole second byte
        `b1` is a signed PC-relative offset (in bytes, relative to the next
        instruction).

        Taint propagation happens here: any op whose result depends on a tainted
        register yields a tainted result, and `_set_reg` keeps it sticky."""

        if opcode == 0x0:            # mov rd, imm
            self._set_reg(rd, arg)   # plain immediate: no new taint source
            self.zf = 0              # plain load: do not pretend to test

        elif opcode == 0x1:          # add rd, imm
            res = self.R[rd] + arg
            self.cf = 1 if res > 0xFFFF else 0
            self._set_reg(rd, res, self.T[rd])

        elif opcode == 0x2:          # sub rd, imm
            res = self.R[rd] - arg
            self.cf = 1 if res < 0 else 0
            self._set_reg(rd, res, self.T[rd])

        elif opcode == 0x3:          # shl rd, imm
            self._set_reg(rd, self.R[rd] << arg, self.T[rd])

        elif opcode == 0x4:          # shr rd, imm
            self._set_reg(rd, self.R[rd] >> arg, self.T[rd])

        elif opcode == 0x5:          # mov rd, rs
            self._set_reg(rd, self.R[arg], self.T[arg])
            self.zf = 0

        elif opcode == 0x6:          # add rd, rs
            res = self.R[rd] + self.R[arg]
            self.cf = 1 if res > 0xFFFF else 0
            self._set_reg(rd, res, self.T[rd] or self.T[arg])

        elif opcode == 0x7:          # xor rd, rs
            self._set_reg(rd, self.R[rd] ^ self.R[arg], self.T[rd] or self.T[arg])

        elif opcode == 0x8:          # and rd, rs
            self._set_reg(rd, self.R[rd] & self.R[arg], self.T[rd] or self.T[arg])

        elif opcode == 0x9:          # ld rd, [rs]
            addr    = self.R[arg]
            value   = self.load_byte(addr)
            seg     = self._seg_for(addr)
            # Tainted if the byte comes from SECRET, or the pointer itself was
            # tainted (so the flag can't be laundered through a crafted table).
            tainted = self.T[arg] or (seg is not None and seg.name == "SECRET")
            self._set_reg(rd, value, tainted)

        elif opcode == 0xA:          # st [rd], rs
            # Flag data must never leak out of a register via memory.
            if self.T[arg]:
                raise CpuFault("TAINT_VIOLATION",
                               "attempt to write from tainted register r%d" % arg,
                               self.R[rd])
            self.store_byte(self.R[rd], self.R[arg])

        elif opcode == 0xB:          # out rd
            if len(self.output) < MAX_OUTPUT:
                self.output.append(self.R[rd] & 0xFF)

        elif opcode == 0xC:          # bra rel  (PC = next_pc + offset)
            self.pc = (self.pc + self._s8(b1)) & 0xFFFF

        elif opcode == 0xD:          # brz rel  (branch if Z)
            if self.zf:
                self.pc = (self.pc + self._s8(b1)) & 0xFFFF

        elif opcode == 0xE:          # brnz rel (branch if !Z)
            if not self.zf:
                self.pc = (self.pc + self._s8(b1)) & 0xFFFF

        elif opcode == 0xF:          # hlt
            self.halted = True

        else:                        # most of the 256 opcode values are unused
            raise CpuFault("ILLEGAL_INSTRUCTION", "unknown opcode 0x%02X" % opcode)

    # -- run loop ----------------------------------------------------------

    def load_program(self, program):
        n = len(program)
        if n == 0:
            raise CpuFault("PREFETCH_ABORT", "empty program", 0)
        if n > MAX_PROGRAM:
            program = program[:MAX_PROGRAM]
            n = MAX_PROGRAM
        self.mem[CODE_BASE:CODE_BASE + n] = program
        self.prog_len = n
        self.pc = CODE_BASE

    def run(self):
        """Run until halt or fault. Returns the CpuFault on a fault, or None on
        a clean halt / step-limit stop."""
        steps = 0
        while not self.halted:
            if steps >= MAX_STEPS:
                self.fault_pc = self.pc
                return CpuFault("EXECUTION_LIMIT",
                                "exceeded %d instructions" % MAX_STEPS, self.pc)
            fetch_pc = self.pc
            try:
                if fetch_pc & 1:
                    raise CpuFault("UNALIGNED_FETCH",
                                   "PC is not 2-byte aligned", fetch_pc)
                b0 = self.fetch(fetch_pc)
                b1 = self.fetch((fetch_pc + 1) & 0xFFFF)
                opcode = b0                       # full 8-bit opcode
                rd     = b1 >> 4                  # destination register
                arg    = b1 & 0xF                 # immediate or source register
                self.trace.append((fetch_pc, b0, b1))
                self.pc = (self.pc + 2) & 0xFFFF
                self.execute(opcode, rd, arg, b1)
            except CpuFault as fault:
                # Report the address of the faulting instruction itself.
                self.fault_pc = fetch_pc
                return fault
            steps += 1
        return None


# --------------------------------------------------------------------------
# Disassembly
# --------------------------------------------------------------------------

def _s8(value):
    return value - 0x100 if value & 0x80 else value


def disasm(b0, b1, pc=0):
    """Render one 2-byte instruction as a clear mnemonic, e.g. 'mov r1, 0x1'.
    `pc` is the instruction's address, used to resolve relative branch targets."""
    op  = b0                  # opcode is the full first byte
    rd  = b1 >> 4
    arg = b1 & 0xF
    if op == 0x0:
        return "mov  r%d, 0x%X" % (rd, arg)
    if op == 0x1:
        return "add  r%d, 0x%X" % (rd, arg)
    if op == 0x2:
        return "sub  r%d, 0x%X" % (rd, arg)
    if op == 0x3:
        return "shl  r%d, %d" % (rd, arg)
    if op == 0x4:
        return "shr  r%d, %d" % (rd, arg)
    if op == 0x5:
        return "mov  r%d, r%d" % (rd, arg)
    if op == 0x6:
        return "add  r%d, r%d" % (rd, arg)
    if op == 0x7:
        return "xor  r%d, r%d" % (rd, arg)
    if op == 0x8:
        return "and  r%d, r%d" % (rd, arg)
    if op == 0x9:
        return "ld   r%d, [r%d]" % (rd, arg)
    if op == 0xA:
        return "st   [r%d], r%d" % (rd, arg)
    if op == 0xB:
        return "out  r%d.b" % rd
    if op in (0xC, 0xD, 0xE):
        off    = _s8(b1)
        target = (pc + 2 + off) & 0xFFFF
        mnem   = {0xC: "bra", 0xD: "brz", 0xE: "brnz"}[op]
        return "%-4s %+d -> 0x%04X" % (mnem, off, target)
    if op == 0xF:
        return "hlt"
    return "db   0x%02X, 0x%02X" % (b0, b1)      # unknown opcode


# --------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------

def render_report(cpu, fault):
    lines = []
    lines.append("=== EXECUTION TRACE ===")
    for (pc, b0, b1) in cpu.trace:
        lines.append("PC=%04X [%02X %02X] %s" % (pc, b0, b1, disasm(b0, b1, pc)))

    lines.append("")
    lines.append("=== OUTPUT ===")
    out = bytes(cpu.output)
    if len(out) < cpu.flag_len and out.rstrip(b"\x00") != GREETING:
        # Fewer bytes emitted than the flag is long: can't be the whole flag.
        # (The demo greeting is exempt so client.py's example shows something.)
        lines.append("[need more bytes, out_size:%d min_size:%d]" % (len(out), cpu.flag_len))
    else:
        lines.append(repr(out.decode("latin-1")))

    lines.append("")
    if fault is None:
        lines.append("=== HALTED ===")
        lines.append("CPU halted normally.")
    else:
        lines.append("=== CPU EXCEPTION ===")
        lines.append("Reason: %s (%s)" % (fault.reason, fault.detail))
        lines.append("Faulting PC:   0x%04X" % cpu.fault_pc)
        if fault.addr is not None:
            lines.append("Faulting addr: 0x%04X" % fault.addr)
        lines.append("")
        lines.append("--- Registers ---")
        def _regcell(j):
            # Redact tainted registers so the flag can't be read off the dump.
            return "R%-2d: %s" % (j, "<TAINTED>" if cpu.T[j] else "0x%04X" % cpu.R[j])
        for i in range(0, NUM_REGS, 4):
            row = "   ".join(_regcell(j) for j in range(i, min(i + 4, NUM_REGS)))
            lines.append(row)
        lines.append("FLAGS: Z=%d C=%d" % (cpu.zf, cpu.cf))
        lines.append("")
        lines.append("--- Memory map ---")
        for seg in SEGMENTS:
            lines.append("%-7s 0x%04X - 0x%04X  %s"
                         % (seg.name, seg.start, seg.end, seg.perms))

    return ("\n".join(lines) + "\n").encode("utf-8")


def run_program(program, flag=b""):
    """Convenience entry point for tests/solvers: returns (report_bytes, cpu, fault)."""
    cpu = CPU(flag=flag)
    cpu.load_program(program)
    fault = cpu.run()
    return render_report(cpu, fault), cpu, fault


# --------------------------------------------------------------------------
# Network front-end
# --------------------------------------------------------------------------

def _load_flag():
    here = os.path.dirname(os.path.abspath(__file__))
    for path in (os.path.join(os.getcwd(), "flag.txt"),
                 os.path.join(here, "flag.txt")):
        try:
            with open(path, "rb") as fh:
                return fh.read().strip()
        except OSError:
            continue
    return os.environ.get("FLAG", "HEXACON{example_flag}").encode()


BANNER = (
    "== CUSTOM CPU SERVICE ==\n"
    "Send a program and the CPU will run it.\n"
    # "Protocol: 2 bytes big-endian length, then that many program bytes.\n"
    "Max program size: %d bytes.\n\n" % MAX_PROGRAM
)


def _build_response(program, flag):
    """Run a program and return the full report (or an error line)."""
    if len(program) == 0:
        return b"ERROR: empty program.\n"
    try:
        report, _, _ = run_program(program, flag=flag)
        return report
    except CpuFault as exc:
        cpu = CPU(flag=flag)
        return render_report(cpu, exc)


def serve_session(read_exact, write_all, flag):
    """One request/response cycle over an abstract byte transport."""
    write_all(BANNER.encode())
    header = read_exact(2)
    if len(header) < 2:
        write_all(b"ERROR: could not read 2-byte length header.\n")
        return
    length = int.from_bytes(header, "big")
    if length == 0 or length > MAX_PROGRAM:
        write_all(("ERROR: program length must be 1..%d.\n" % MAX_PROGRAM).encode())
        return
    program = read_exact(length)
    if len(program) < length:
        write_all(b"ERROR: truncated program.\n")
        return
    write_all(_build_response(program, flag))


def _serve_socket(host, port, flag):
    class Handler(socketserver.BaseRequestHandler):
        def handle(self):
            conn = self.request
            conn.settimeout(15)

            def read_exact(n):
                buf = b""
                while len(buf) < n:
                    try:
                        chunk = conn.recv(n - len(buf))
                    except OSError:
                        break
                    if not chunk:
                        break
                    buf += chunk
                return buf

            try:
                serve_session(read_exact, conn.sendall, flag)
            except OSError:
                pass

    class Server(socketserver.ThreadingTCPServer):
        allow_reuse_address = True
        daemon_threads = True

    with Server((host, port), Handler) as srv:
        sys.stderr.write("customcpu listening on %s:%d\n" % (host, port))
        sys.stderr.flush()
        srv.serve_forever()


def _serve_stdio(flag):
    stdin, stdout = sys.stdin.buffer, sys.stdout.buffer

    def read_exact(n):
        buf = b""
        while len(buf) < n:
            chunk = stdin.read(n - len(buf))
            if not chunk:
                break
            buf += chunk
        return buf

    def write_all(data):
        stdout.write(data)
        stdout.flush()

    serve_session(read_exact, write_all, flag)


def main(argv):
    flag = _load_flag()
    if "--stdio" in argv:                          # one shot over stdin/stdout
        _serve_stdio(flag)
        return
    args = [a for a in argv[1:] if not a.startswith("-")]
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "1337"))
    if len(args) == 1:
        port = int(args[0])
    elif len(args) >= 2:
        host, port = args[0], int(args[1])
    _serve_socket(host, port, flag)


if __name__ == "__main__":
    main(sys.argv)
