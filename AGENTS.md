# Versus 작업 규칙

- 변경 후 Windows 로컬 빌드와 Windows·Android32·Android64 합본을 검증한다.
- iOS 빌드는 사용자가 요청했으므로 CI에서 별도 아티팩트로 시도한다. macOS는 별도 요청 전까지 빌드하지 않는다.
- 최종 배포 파일은 항상 `dist/tipp7.versus-AllPlatform.geode`에 최신 빌드로 갱신한다.
- 위 파일명은 유지하되 현재 합본에는 Windows·Android32·Android64만 포함한다. iOS 빌드는 별도 아티팩트로 검증하며, 검증된 병합 지원 전에는 합본에 섞지 않는다.
- 버전별 보관 파일은 별도로 둘 수 있지만 사용자에게는 위 고정 경로를 안내한다.
