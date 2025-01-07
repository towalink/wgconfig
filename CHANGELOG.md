# Changelog

All notable changes to this project are documented in this file.

## [Unreleased]

### Added

- n/a

### Changed

- n/a

### Fixed

- n/a

## [1.1.0] - 2025-01-07

### Added

- Support the use of file-like objects like StringIO (using write_to_fileobj and read_from_fileobj)

## [1.0.4] - 2024-07-16

### Fixed

- Package config file for automated tests in correct manner

## [1.0.3] - 2024-07-07

### Changed

- Package config file for automated tests

## [1.0.2] - 2024-05-25

### Added

- Packaging for Debian

### Changed

- Update package setup.py

## [1.0.1] - 2024-01-30

### Added

- More helpful exception output in case WireGuard tools are not installed but needed

## [1.0.0] - 2023-07-27

### Added

- Add method for flexibly returning the attributes and values of the interface section
- Add method for flexibly returning the peers and optionally the peers' data

### Changed

- Rework documentation in README.md
- Add a Jupityer Notebook as additional documentation

## [0.3.0] - 2022-11-19

### Added

- Add method to just retrieve the data of a single peer
- Add the capability to disable and enable peers (mainly contributed by "subs1stem")

### Fixed

- Tests no longer change internal data structures

### Changed

- Refactored tests to reduce code duplication

## [0.2.3] - 2022-08-22

### Changed

- Improved formatting in "README.md"
- Fault tolerant handling of blank lines in "del_attr"

## [0.2.2] - 2020-11-15

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
