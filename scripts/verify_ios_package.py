"""Check the actual iOS package produced by CI before offering it for download."""

import json
from pathlib import Path
import struct
import sys
from zipfile import ZipFile


def verify(folder: Path, edition: str) -> None:
    if edition not in {"standard", "membership"}:
        raise ValueError("Expected standard or membership")
    packages = list(folder.glob("*.geode"))
    if len(packages) != 1:
        raise ValueError(f"Expected one .geode package, found {len(packages)}")
    source = Path(__file__).resolve().parents[1]
    expected = json.loads((source / "mod.json").read_text())
    with ZipFile(packages[0]) as archive:
        manifest = json.loads(archive.read("mod.json"))
        if manifest["id"] != expected["id"] or manifest["version"] != expected["version"]:
            raise ValueError("Package metadata does not match this source tree")
        binary_name = f'{manifest["id"]}.ios.dylib'
        data = archive.read(binary_name)
        # MH_MAGIC_64, CPU_TYPE_ARM64, MH_DYLIB: reject empty or wrong-platform output.
        if len(data) < 32 or struct.unpack_from("<I", data)[0] != 0xFEEDFACF:
            raise ValueError("Expected a 64-bit little-endian Mach-O binary")
        if struct.unpack_from("<I", data, 4)[0] != 0x0100000C:
            raise ValueError("Expected an arm64 binary")
        if struct.unpack_from("<I", data, 12)[0] != 6:
            raise ValueError("Expected a dynamic library")
        if f"versus-edition:{edition}".encode() not in data:
            raise ValueError("The binary does not contain the expected edition marker")
        for sound in (source / "resources/sounds").iterdir():
            if sound.is_file():
                name = f'resources/{manifest["id"]}/{sound.name}'
                if archive.read(name) != sound.read_bytes():
                    raise ValueError(f"Sound resource mismatch: {name}")
    print(f"Verified {packages[0].name}: arm64 iOS, {edition}, bundled sounds present")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: verify_ios_package.py OUTPUT_DIR standard|membership")
    verify(Path(sys.argv[1]), sys.argv[2])
