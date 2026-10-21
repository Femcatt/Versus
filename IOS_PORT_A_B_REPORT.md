# Versus iOS port — build checkpoint

The user requested an iOS build. This branch applies the Phase A/B configuration
to the existing Versus v0.5.4 sources and prepares an actual iOS compilation.
It is not yet a device-tested release.

## Changes

- Select arm64 before CMake initializes the iOS toolchain.
- Build Standard and Membership separately on a macOS GitHub Actions runner.
- Use Geode 5.7.1 from mod.json and a pinned official build action revision.
- Run on pushes to main and codex/ios-port, or by workflow_dispatch.
- Validate the package: matching mod ID/version, arm64 Mach-O dylib,
  edition marker, and byte-for-byte bundled sound resources.
- Upload separate iOS artifacts for 14 days. Windows/Android packaging remains
  in its existing workflow; its fixed combined release does not include iOS.

## Previous connection blocker (resolved before upload)

The connected GitHub account is Femcatt, which owns Femcatt/Versus.
The GitHub integration returned HTTP 403 Resource not accessible by integration
when creating the proposed tree. Its installation list is empty. No repository
changes were saved and no CI build was started. The installation is now visible for Femcatt and upload is being attempted again.

## Validation before the first CI attempt

- All src, tests and sound resource files match repository base commit
  69cfb4f2e7b39f426797a0a3d7d4389f63dac755.
- Six existing C++ checks compiled and passed on Linux with GCC 13.3:
  runner, map_cache, battle_progress, random_map, edition_standard,
  edition_membership. The random-map program reports 261197 checks.
- The existing Python packaging suite passed all 10 tests.
- Membership/room_score tests need mat-json and were not run here.
- Full Windows and Android builds will be attempted by the existing CI.
- This Linux environment has no Xcode/iOS SDK; the iOS build must run in CI.
- Firebase emulator tests and an iPhone runtime test have not run.

## Runtime checks required after a successful build

Check mod startup, room creation/joining with two clients, map and audio downloads,
both players' readiness, gameplay synchronization, spectating, rematch/forfeit,
and Membership cosmetics on the intended Geometry Dash/Geode iPhone setup.

Both editions use tipp7.versus: install only one edition at a time.
