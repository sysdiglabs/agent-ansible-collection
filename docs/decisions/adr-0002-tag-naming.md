# ADR-0002 - Tag Naming

## Feature
N/A

## Status
Accepted

## Context
The release process defined in ADR-0001 relies on the existence and placement
of git tags. Those tags must be in a well-defined format so that tooling and
automation can be written to leverage those tags.

## Decision
Commits will be tagged in two cases:
* A new release candidate is being created, at which point a tag is placed on
  the desired commit on the appropriate release branch.
* A release candidate is being promoted to an official release, at which point
  a new tag is placed on the same commit as the latest validated release
  candidate.

The tag naming format will follow a subset of
[semantic versioning](https://semver.org/). As a result, the tag types will
follow these formats:
* Release candidates: `(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>rc(?:0|[1-9]\d*)*))$`
  * Ex. 1.2.3-rc1
* Releases: `(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)$`
