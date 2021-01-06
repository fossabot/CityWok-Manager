# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- New tests of the index View
- Index View of employee Module to show all employees - ***/employee***

### Changed
- Improve zh_name Field in EmployeeForm 

### Fixed
- Missing `nullable=False` in Employee model
- Typo in EmployeeForm

## [0.1.0] - 2021-01-04
### Added
- Base structure of the project
- This CHANGELOG file to track the developer of the project
- gitignore, README and LICENSE files
- Flask extensions
  - Flask-SQLAlchemy - database management
  - Flask-Babel - i18n
  - Config file
- Employee Module
  - Employee Model and Form
  - View to create employee - ***/employee/new***
  - Tests of create employee
