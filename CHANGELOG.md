# Changelog

All notable changes to this project are documented in this file.

## [Unreleased]

### Added

- n/a

### Changed

- n/a

### Fixed

- n/a

## [0.2.3]

### Changed

- Improved formatting in "README.md"
- Fault tolerant handling of blank lines in "del_attr"

## [0.2.2]

### Added

- Support for older Python versions; now 2.7+ is supported; thanks to Marc (https://github.com/marcfiu) for this

## [0.2.1] - 2020-11-11

### Fixed

- Initializing file with comment before interface section is handled properly again.

## [0.2.0] - 2020-11-10

### Added

- Added internal "_rawdata" section attribute.

### Changed

- Properly handle comments at begin and end of sections in line indices (this changes behavior of attributes "_index_firstline" and "_index_firstline" in these cases)

### Fixed

- Truncate WireGuard config files before writing changes.

## [0.1.4] - 2020-11-07

### Added

- Added simple module wrapping wg tool.

### Changed

- Create WireGuard config files without world readable permissions.
- Formatting improvements.

### Fixed

- README corrections.

## [0.1.3] - 2020-07-28

### Fixed

- Extended tests to detect wrong line offset when deleting peers.
- Fixed wrong line offset when deleting peers.

## [0.1.2] - 2020-07-11

### Added

- Prepared for first public release to PyPi.

## [0.1.1] - 2020-07-11

### Added

- First public release to Github.
