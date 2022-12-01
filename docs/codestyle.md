# Documentation

## Code Style

### C++
`Clang style`.

This project uses the following style
for writing C++ code:
```
//
// Created by `user` on month/day/year.
//
#include "my/some.hpp"

#include "some/library.hpp"

#include <iostream>

struct some_struct_in_snake_case {};

enum enum_snake_case {
  some = 1, // with trailing , 
};

namespace my_namepsace_in_snake_case {
class some_class {
  auto some_function_in_snake_case() -> void {
    std::cout << "some_function_also_in_snake_case";
  }
  
  template<typename SomeTemplateInPascalCase>
  auto template_method() -> void {
    std::cout << "template_method";
  }
};
} // namespace my

auto main() -> int {
  my_namepsace_in_snake_case::some_class some_variable;
  
  some_variable.some_function_in_snake_case();
  some_variable.template_method<my::some_class>();
}
```

### Python
`PEP8`, `black`, `isort`, `flake8` are used.

#### Project Structure

- `/project`
  - `alembic`
    - `...`
  - `app`
    - `api`
      - `v1`
        - `routers`
          + `some.py`
        + `__init__.py`
        + `v1.py`
      + `api.py`
      + `__init__.py`
    - `core`
      + `config.py`
      + `depends.py`
      + `handlers.py`
      + `middlewares.py`
      + `tools.py`
    - `db`
      + `base.py`
      + `session.py`
    - `orm`
      - `some`
        + `__init__.py`
        + `some.py`
      + `__init__.py`
    - `schemas`
      + `__init__.py`
      + `some.py`
    - `store`
      - `some`
        + `accessor.py`
      + `__init__.py`
      + `base.py`
      + `store.py`
    - `structures`
      - `exceptions`
        - `some`
          + `errors.py`
        + `__init__.py`
      + `enums.py`
    - `utils`
      + `some.py`
    + `main.py`
  - `tests`
    - `...`
