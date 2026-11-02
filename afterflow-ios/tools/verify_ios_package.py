#!/usr/bin/env python3
"""Reject desktop or simulator binaries accidentally packaged as an iOS mod."""
import hashlib
import json
from pathlib import Path
import struct
import sys
from zipfile import ZipFile


def verify(path: Path) -> None:
    with ZipFile(path) as archive:
        if archive.testzip() is not None:
            raise ValueError("Corrupt ZIP member")
        metadata = json.loads(archive.read("mod.json"))
        if metadata["gd"] != {"ios": "2.2081"}:
            raise ValueError("Unexpected GD target")
        if metadata["id"] != "afterflow.prsevend":
            raise ValueError("Unexpected mod ID")
        name = metadata["id"] + ".ios.dylib"
        binaries = [p for p in archive.namelist() if p.endswith((".dll", ".dylib", ".so"))]
        if binaries != [name]:
            raise ValueError(f"Expected only {name}, got {binaries}")
        data = archive.read(name)
    if len(data) < 32:
        raise ValueError("Truncated Mach-O header")
    magic, cpu, subtype, filetype, commands, command_bytes, flags, reserved = struct.unpack_from("<8I", data)
    if magic != 0xFEEDFACF or cpu != 0x0100000C or filetype != 6:
        raise ValueError("Expected a thin ARM64 Mach-O dynamic library")
    if 32 + command_bytes > len(data):
        raise ValueError("Truncated load commands")
    position = 32
    ios = False
    for _ in range(commands):
        if position + 8 > 32 + command_bytes:
            raise ValueError("Truncated load command")
        command, size = struct.unpack_from("<II", data, position)
        if size < 8 or position + size > 32 + command_bytes:
            raise ValueError("Invalid load command size")
        if command == 0x32:  # LC_BUILD_VERSION
            if size < 24:
                raise ValueError("Invalid LC_BUILD_VERSION")
            platform = struct.unpack_from("<I", data, position + 8)[0]
            if platform != 2:  # PLATFORM_IOS; simulator is 7, macOS is 1
                raise ValueError(f"Wrong Apple platform: {platform}")
            ios = True
        elif command == 0x25:  # LC_VERSION_MIN_IPHONEOS
            if size < 16:
                raise ValueError("Invalid LC_VERSION_MIN_IPHONEOS")
            ios = True
        elif command in (0x24, 0x2F, 0x30):
            raise ValueError("Conflicting Apple platform command")
        position += size
    if position != 32 + command_bytes or not ios:
        raise ValueError("Missing iPhoneOS platform marker or invalid command table")
    print(f"PASS: {path.name}: ARM64 iPhoneOS, GD 2.2081, {metadata['version']}")
    print("SHA256:", hashlib.sha256(path.read_bytes()).hexdigest())


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: verify_ios_package.py MOD.geode")
    try:
        verify(Path(sys.argv[1]))
    except (ValueError, KeyError, OSError) as error:
        raise SystemExit(f"FAIL: {error}")
