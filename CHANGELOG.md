# Changelog

[← Back to README](./README.md)

All notable changes to this project will be documented in this file.


## [Beta 0.1.2]
### Added
- Main loop
  
### Changed
- `search()` function to accept argument and not use `input()` inside of it
- - Updated README to match new version

### Fixed
- Fixed a typo in `qpCore` ("lodaing database" -> "loading database")


## [Beta 0.1.1]
### Added
- `on_startup` - module with optional database update before search.
- Custom ANSI-colored answers format with HTML tag parsing and code block framing.

### Changed
- Updated README to match new version

## [Beta 0.1]
### Added 
- Initial MVP release of `SOCosineSearch`.
- Semantic search using `all-MiniLM-L6-v2` and Faiss.
- Stack Exchange api used for initial data collection with Duckdb as a storage.