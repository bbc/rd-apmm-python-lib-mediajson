# mediajson Changelog

## 1.1.1
- Only attempt to parse UUIDs when they comprise the entire string.

## 1.1.0
- Provide support for immutable mediatimestamp and default to mutable.
- Allow either mutable or immutable when encoding to JSON.

## 1.0.1
- Remove unused install command from tox.ini
- Add Jenkins build trigger to rebuild master every day.
- Allow build to run on a wider selection of agents.

## 1.0.0
- Initial version, porting json parsing components from nmos-common v.0.6.0.