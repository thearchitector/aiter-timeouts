# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - 2023-10-21

### Changed

- Rename `timeout` to `with_timeout` for clarity.

### Fixed

- Picklable custom exceptions ([I.#1](https://github.com/thearchitector/aiter-timeouts/issues/1))

## [1.0.0] - 2023-10-21

### Added

- The ability to wrap each step of, or all steps of, any arbitrary asynchronous iterator in a timeout.
- Custom exceptions to track when timeouts occur during specific steps of an iterator.
