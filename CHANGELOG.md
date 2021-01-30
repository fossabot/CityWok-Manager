# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- enable CSRF protection
- Employee Module
  - Functionality to update employee's information - ***/employee/<employee_id>/update***
  - Functionality to inactivate/activate employees - ***/employee/<employee_id>/activate(inactivate)***
  - More testes
  - coerce in Employee Model to process from obj to form

### Updated
- ***layout.html*** to provide access to different views

## [0.2.0] - 2021-01-28
### Added
- Bootstrap Icon
- Employee Module
  - Detail View of employee Module - ***/employee/<employee_id>***
  - Index View of employee Module to show all employees - ***/employee***
  - Tests of the Index and Detail View
  - `full_name` property in Employee Model

### Changed
- Improve `zh_name` Field in EmployeeForm 

### Fixed
- Chinese Name not showing by using `chinese_name` instead `zh_name`
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
